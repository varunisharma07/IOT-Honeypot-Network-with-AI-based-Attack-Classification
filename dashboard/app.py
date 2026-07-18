
from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

DATABASE = "database/honeypot.db"


@app.route("/")
def index():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM attacks
        ORDER BY id DESC
    """)

    attacks = cursor.fetchall()

    conn.close()

    return render_template("index.html", attacks=attacks)


if __name__ == "__main__":
    app.run(debug=True)