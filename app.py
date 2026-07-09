from flask import Flask, jsonify
from flask_cors import CORS
import os
import logging
import psycopg2

app = Flask(__name__)
CORS(app)

APP_NAME = os.getenv("APP_NAME", "ShopEasy")
SERVICE_NAME = os.getenv("SERVICE_NAME", "order-service")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
PORT = int(os.getenv("PORT", "5001"))

DB_HOST = os.getenv("DB_HOST", "postgres-service")
DB_NAME = os.getenv("DB_NAME", "shopeasy")
DB_USER = os.getenv("DB_USERNAME", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "admin123")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


@app.route("/", methods=["GET"])
def home():
    return jsonify(
        {
            "service": SERVICE_NAME,
            "environment": ENVIRONMENT,
            "message": f"Welcome to {APP_NAME} Order Service"
        }
    )


@app.route("/api/orders", methods=["GET"])
def get_orders():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT order_id, product_id, quantity
            FROM orders
            ORDER BY order_id
            """
        )

        rows = cursor.fetchall()

        orders = []

        for row in rows:
            orders.append(
                {
                    "order_id": row[0],
                    "product_id": row[1],
                    "quantity": row[2]
                }
            )

        cursor.close()
        conn.close()

        return jsonify(orders)

    except Exception as e:
        logging.error(f"Database error: {e}")

        return jsonify(
            {
                "error": str(e)
            }
        ), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify(
        {
            "status": "UP",
            "service": SERVICE_NAME,
            "environment": ENVIRONMENT
        }
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=PORT
    )