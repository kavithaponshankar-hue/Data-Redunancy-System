from flask import Flask, render_template, request, redirect, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "cloudproject"

DATABASE = "database.db"


# -----------------------------
# Create Database
# -----------------------------

def init_db():

    if not os.path.exists(DATABASE):

        conn = sqlite3.connect(DATABASE)

        with open("schema.sql") as f:
            conn.executescript(f.read())

        conn.commit()
        conn.close()


# -----------------------------
# Database Connection
# -----------------------------

def get_connection():

    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    return conn


# -----------------------------
# Home Page
# -----------------------------

@app.route("/")

def home():

    conn = get_connection()

    users = conn.execute(
        "SELECT * FROM users ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template("index.html", users=users)


# -----------------------------
# Add Record
# -----------------------------

@app.route("/add", methods=["GET", "POST"])

def add():

    if request.method == "POST":

        name = request.form["name"].strip()

        email = request.form["email"].strip().lower()

        phone = request.form["phone"].strip()

        conn = get_connection()

        duplicate = conn.execute(

            """
            SELECT * FROM users
            WHERE email=? OR phone=?
            """,

            (email, phone)

        ).fetchone()

        if duplicate:

            flash("Duplicate record found! Data was not added.", "danger")

            conn.close()

            return redirect("/")

        conn.execute(

            """
            INSERT INTO users(name,email,phone)
            VALUES(?,?,?)
            """,

            (name, email, phone)

        )

        conn.commit()

        conn.close()

        flash("Unique record added successfully.", "success")

        return redirect("/")

    return render_template("add.html")


# -----------------------------
# Search
# -----------------------------

@app.route("/search", methods=["POST"])

def search():

    keyword = request.form["keyword"]

    conn = get_connection()

    users = conn.execute(

        """
        SELECT * FROM users

        WHERE

        name LIKE ?

        OR

        email LIKE ?

        OR

        phone LIKE ?
        """,

        (

            "%" + keyword + "%",

            "%" + keyword + "%",

            "%" + keyword + "%"

        )

    ).fetchall()

    conn.close()

    return render_template("records.html", users=users)


# -----------------------------
# Delete Record
# -----------------------------

@app.route("/delete/<int:id>")

def delete(id):

    conn = get_connection()

    conn.execute(

        "DELETE FROM users WHERE id=?",

        (id,)

    )

    conn.commit()

    conn.close()

    flash("Record deleted successfully.", "warning")

    return redirect("/")


# -----------------------------
# Run Application
# -----------------------------

if __name__ == "__main__":

    init_db()

    app.run(debug=True)