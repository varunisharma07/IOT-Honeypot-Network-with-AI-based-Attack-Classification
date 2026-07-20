
from flask import jsonify
import sqlite3

DATABASE = "database/honeypot.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def register_routes(app):

    @app.route("/api/stats")
    def stats():

        conn = get_db()
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM attacks")
        total = cur.fetchone()[0]

        cur.execute("SELECT COUNT(DISTINCT src_ip) FROM attacks")
        ips = cur.fetchone()[0]

        cur.execute("""
            SELECT COUNT(*)
            FROM attacks
            WHERE username IS NOT NULL
            AND username != ''
        """)
        logins = cur.fetchone()[0]

        cur.execute("""
            SELECT COUNT(*)
            FROM attacks
            WHERE command IS NOT NULL
            AND command != ''
        """)
        commands = cur.fetchone()[0]

        conn.close()

        return jsonify({
            "total": total,
            "ips": ips,
            "logins": logins,
            "commands": commands
        })


    @app.route("/api/attacks")
    def attacks():

        conn = get_db()

        cur = conn.cursor()

        cur.execute("""
            SELECT *
            FROM attacks
            ORDER BY id DESC
            LIMIT 25
        """)

        rows = [dict(r) for r in cur.fetchall()]

        conn.close()

        return jsonify(rows)