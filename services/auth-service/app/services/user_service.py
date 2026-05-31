import psycopg2

from app.core.database import get_db_connection
from app.core.logging_config import logger


def create_user(username: str, email: str):
    try:
        logger.info(f"Creating user: {username}")

        connection = get_db_connection()
        cursor = connection.cursor()

        query = """
        INSERT INTO users (username, email)
        VALUES (%s, %s)
        RETURNING id, username, email;
        """

        cursor.execute(query, (username, email))

        user = cursor.fetchone()

        connection.commit()

        logger.info(f"User created successfully: {username}")

        return {
            "id": user[0],
            "username": user[1],
            "email": user[2]
        }

    except psycopg2.errors.UniqueViolation:
        connection.rollback()

        logger.error(f"Duplicate user attempted: {username}")

        return {
            "error": "User already exists"
        }

    finally:
        cursor.close()
        connection.close()
