import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Configure secret key for sessions
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Database configuration for Railway
database_url = os.getenv("DATABASE_URL")

# Some providers give connection strings that start with 'postgres://'.
# psycopg and many libs prefer 'postgresql://'
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

# Fallback to sqlite for local dev
db = SQL(database_url or "sqlite:///expense.db")

CATEGORY = [
    "Food",
    "Travel",
    "Bills",
    "Shopping",
    "Grocery",
    "Stationary",
    "Cosmetics",
    "Borrowings",
    "Lendings",
    "Others"
]

MONTHS = [
    "January", 
    "February", 
    "March", 
    "April", 
    "May", 
    "June",
    "July", 
    "August", 
    "September", 
    "October", 
    "November", 
    "December"
]

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET","POST"])
@login_required
def index():
    user_id = session["user_id"]

    if request.method == "POST":
        day = int(request.form.get("day"))
        month = request.form.get("month")
        year = int(request.form.get("year"))

        categories = request.form.get("categry")
        if categories not in CATEGORY:
            return apology("Please enter a valid input!!", 400)
        description = request.form.get("description")

        try:
            amount = int(request.form.get("expense"))
        except (ValueError, TypeError):
            return apology("Please enter a valid input!!", 400)
        
        if amount < 1:
            return apology("Please enter a valid amount!!", 400)
        
        db.execute("INSERT INTO expense(user_id, day, month, year, category, description, amount) VALUES(?, ?, ?, ?, ?, ?, ?)", user_id, day, month, year, categories, description, amount)

        flash("Expense Inserted!!")
        return redirect("/")
    else:
        return render_template("index.html", category=CATEGORY, months=MONTHS)

@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    user_id = session["user_id"]

    if request.method == "POST":
        categories = request.form.get("categry")
        day = request.form.get("day")
        month = request.form.get("months")
        year = request.form.get("year")
        query = "SELECT * FROM expense WHERE user_id = ? "
        params = [user_id,]
        
        if categories:
            if categories not in CATEGORY:
                return apology("Invalid Category!!", 400)
            query += " AND category = ?"
            params.append(categories)

        if year:
            try:
                year = int(year)
                query +=" AND year = ?"
                params.append(year)
            except ValueError:
                return apology("Invalid year!!", 400)
        
        if month:
            if month not in MONTHS:
                return apology("Invalid month Name!!", 400)
            else:
                query += " AND month = ?"
                params.append(month)

        if day:
            try:
                day = int(day)
                if day < 1 or day > 31:
                    return apology("Invalid day!!", 400)
            except ValueError:
                return apology("Invalid day!!", 400)
            
            if month:
                try:
                    month_num = MONTHS.index(month) + 1
                    datetime(year, month_num, day)
                except (ValueError, TypeError):
                    return apology("Invalid date!!", 400)
            
            query += " AND day = ?"
            params.append(day)

        if year and not categories and not day and not month:
            data = db.execute(query, *params)
            monthly_expenses = {}
            elements = []
            expenditure = 0

            for row in data:
                mon = row["month"]
                amount = row["amount"]

                if mon in monthly_expenses:
                    monthly_expenses[mon] += amount
                else:
                    monthly_expenses[mon] = amount
            
            for mont, expense in monthly_expenses.items():
                elements.append({"month" : mont, "expense": expense})

            expenditure = sum(monthly_expenses.values())

            return render_template("table1.html", elements = elements, expense = expenditure)
        
        else:
            data = db.execute(query, *params)
            expenditure = 0
            for row in data:
                expenditure += row["amount"]
            
            return render_template("table2.html", data = data, expense = expenditure)

    else:
        return render_template("search.html", category=CATEGORY, months=MONTHS)

@app.route("/delete", methods=["POST"])
@login_required
def delete():
    id = request.form.get("id")
    db.execute("DELETE FROM expense WHERE id = ?", id)

    flash("Expense Deleted!!")
    return redirect("/search")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    username = request.form.get("username")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")

    if request.method == "POST":
        if not username:
            return apology("Provide a name.", 400)

        if not password:
            return apology("Provide a password.", 400)

        if  confirmation != password:
            return apology("Password did not match.", 400)

        try:
            db.execute("INSERT INTO users( username, hash) VALUES( ?, ?)", username, generate_password_hash(password))
        except ValueError:
            return apology("Username already exists.", 400)

        return redirect("/login")

    else:
        return render_template("register.html")

# Railway deployment configuration
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)