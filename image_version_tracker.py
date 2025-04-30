# image_version_tracker.py

import os
import json
from datetime import datetime
from flask import Flask, request, jsonify
import docker
import psycopg2

app = Flask(__name__)

# PostgreSQL config
DB_NAME = "image_tracker"
DB_USER = "image_user"
DB_PASSWORD = "password"
DB_HOST = "localhost"
DB_PORT = "5432"

# Docker client
client = docker.from_env()

def connect_db():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

def init_db():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS image_versions (
            id SERIAL PRIMARY KEY,
            image_name TEXT,
            tag TEXT,
            version TEXT,
            commit_hash TEXT,
            timestamp TIMESTAMP
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def extract_image_metadata(image_name):
    try:
        image = client.images.pull(image_name)
        version = image.id
        tag = image_name.split(":")[1] if ":" in image_name else "latest"
        labels = image.labels or {}
        commit_hash = labels.get("org.opencontainers.image.revision", "unknown")

        return {
            "image_name": image_name.split(":")[0],
            "tag": tag,
            "version": version,
            "commit_hash": commit_hash,
            "timestamp": datetime.utcnow()
        }
    except Exception as e:
        print(f"Error pulling image: {e}")
        return None

def log_to_postgres(metadata):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO image_versions (image_name, tag, version, commit_hash, timestamp)
        VALUES (%s, %s, %s, %s, %s);
    """, (
        metadata["image_name"],
        metadata["tag"],
        metadata["version"],
        metadata["commit_hash"],
        metadata["timestamp"]
    ))
    conn.commit()
    cur.close()
    conn.close()

@app.route('/log-image', methods=['POST'])
def log_image():
    data = request.get_json()
    image_name = data.get("image_name")
    storage = data.get("storage", "postgresql")

    if not image_name:
        return jsonify({"error": "Missing 'image_name' field"}), 400

    metadata = extract_image_metadata(image_name)
    if not metadata:
        return jsonify({"error": "Failed to extract image metadata"}), 500

    if storage == "postgresql":
        log_to_postgres(metadata)
    else:
        return jsonify({"error": "Only 'postgresql' storage is supported in this version"}), 400

    return jsonify({
        "message": "Image version data logged successfully.",
        "version": metadata["version"],
        "tag": metadata["tag"]
    }), 200

@app.route('/get-images', methods=['GET'])
def get_images():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT image_name, tag, version, commit_hash, timestamp FROM image_versions ORDER BY timestamp DESC;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    results = []
    for row in rows:
        results.append({
            "image_name": row[0],
            "tag": row[1],
            "version": row[2],
            "commit_hash": row[3],
            "timestamp": row[4].isoformat() if row[4] else None
        })

    return jsonify(results), 200

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

