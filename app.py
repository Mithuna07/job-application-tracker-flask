import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# ---------------- DATABASE CONFIG ----------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(BASE_DIR, "jobtracker.db")




def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            role TEXT NOT NULL,
            location TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


# ---------------- ROUTES ----------------

@app.route("/")
def index():
    conn = get_db_connection()
    jobs = conn.execute("SELECT * FROM jobs").fetchall()
    conn.close()
    return render_template("index.html", jobs=jobs)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        company = request.form["company"]
        role = request.form["role"]
        location = request.form["location"]
        status = request.form["status"]

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO jobs (company, role, location, status) VALUES (?, ?, ?, ?)",
            (company, role, location, status)
        )
        conn.commit()
        conn.close()

        return redirect(url_for("index"))

    return render_template("add.html")


@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    new_status = request.form.get("status")

    conn = get_db_connection()
    conn.execute(
        "UPDATE jobs SET status = ? WHERE id = ?",
        (new_status, id)
    )
    conn.commit()
    conn.close()

    return redirect(url_for("index"))


@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM jobs WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for("index"))


# ---------------- MAIN ----------------
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
