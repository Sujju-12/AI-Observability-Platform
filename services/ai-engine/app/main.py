import os, json, re
import httpx
from fastapi import FastAPI
from kubernetes import client, config

NAMESPACE=os.getenv("TARGET_NAMESPACE","aiops")
PROMETHEUS_URL=os.getenv("PROMETHEUS_URL","http://prometheus-server.aiops-observability.svc.cluster.local:9090")
OLLAMA_URL=os.getenv("OLLAMA_URL","http://host.docker.internal:11434")
OLLAMA_MODEL=os.getenv("OLLAMA_MODEL","qwen2.5:3b")

app=FastAPI(title="AI Observability Engine",version="1.0.0")
try:
    config.load_incluster_config()
except Exception:
    config.load_kube_config()
core=client.CoreV1Api()

def kubernetes_evidence():
    pods=core.list_namespaced_pod(NAMESPACE).items
    events=core.list_namespaced_event(NAMESPACE).items
    return {
      "pods":[{"name":p.metadata.name,"phase":p.status.phase,"restarts":sum(c.restart_count or 0 for c in (p.status.container_statuses or [])),
               "waiting":[c.state.waiting.reason for c in (p.status.container_statuses or []) if c.state and c.state.waiting]}
              for p in pods],
      "events":[{"reason":e.reason,"message":e.message,"object":getattr(e.involved_object,"name",None)}
                for e in sorted(events,key=lambda x:x.last_timestamp or x.event_time or x.first_timestamp or "")[-30:]]
    }

async def prometheus(query):
    try:
        async with httpx.AsyncClient(timeout=5) as h:
            r=await h.get(PROMETHEUS_URL+"/api/v1/query",params={"query":query})
            return r.json()
    except Exception as e:
        return {"error":str(e)}

async def ask_ollama(prompt):
    try:
        async with httpx.AsyncClient(timeout=60) as h:
            r=await h.post(OLLAMA_URL+"/api/generate",json={"model":OLLAMA_MODEL,"prompt":prompt,"stream":False})
            if r.status_code==200:
                return r.json().get("response")
    except Exception:
        return None

def deterministic_rca(e):
    s=json.dumps(e).lower()
    if "oomkilled" in s or "137" in s:
        return {"category":"OOMKilled","root_cause":"Container exceeded its memory limit.","confidence":"high","recommendation":"Inspect memory growth and Kubernetes requests/limits."}
    if "imagepullbackoff" in s or "errimagepull" in s:
        return {"category":"ImagePullBackOff","root_cause":"Kubernetes cannot pull the configured image.","confidence":"high","recommendation":"Verify image tag, registry access and imagePullSecrets."}
    if "crashloopbackoff" in s:
        return {"category":"CrashLoopBackOff","root_cause":"Container starts and repeatedly exits.","confidence":"medium","recommendation":"Inspect previous logs, exit code, events and dependencies."}
    if "pending" in s or "insufficient" in s:
        return {"category":"Scheduling","root_cause":"Pod cannot be scheduled onto a suitable node.","confidence":"medium","recommendation":"Inspect scheduler events, resource requests, taints and node capacity."}
    return {"category":"Unknown","root_cause":"No known failure signature detected.","confidence":"low","recommendation":"Correlate Kubernetes events, logs, metrics and traces."}

@app.get("/health")
def health():
    return {"status":"healthy","service":"ai-engine"}

@app.get("/api/v1/evidence")
async def evidence():
    e=kubernetes_evidence()
    e["cpu"]=await prometheus('sum(rate(container_cpu_usage_seconds_total{namespace="aiops"}[5m])) by (pod)')
    e["memory"]=await prometheus('sum(container_memory_working_set_bytes{namespace="aiops"}) by (pod)')
    return e

@app.post("/api/v1/analyze")
async def analyze():
    e=await evidence()
    r=deterministic_rca(e)
    prompt="You are an SRE troubleshooting agent. Analyze only the supplied Kubernetes evidence. Return JSON with category, root_cause, evidence, confidence and recommendation. Do not invent evidence. EVIDENCE="+json.dumps(e,default=str)
    ai=await ask_ollama(prompt)
    if ai:
        try:
            m=re.search(r"\{.*\}",ai,re.S)
            if m: r.update(json.loads(m.group(0)))
            else: r["ai_analysis"]=ai
            r["source"]="ollama"
        except Exception:
            r["ai_analysis"]=ai
            r["source"]="ollama"
    else:
        r["source"]="deterministic-rules"
    return {"incident":r,"evidence":e}
