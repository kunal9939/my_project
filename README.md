# Expense Tracker Web Application

#### Video Demo:  [https://youtu.be/cn8637Cfev4?si=Vrtj3kVRmiqTbup6]

#### Description

This project is a full-featured **Expense Tracker Web Application** developed using **Flask** and **SQLite3**, focused on enabling users to record, manage, and analyze their personal expenses. The application supports user registration, secure login, data entry for daily expenses, and dynamic search and filtering of expense history. The interface is clean and responsive, thanks to integration with **Bootstrap 5**, and it includes a custom logo design for a personalized touch.

This tracker was designed keeping in mind simplicity and effectiveness. Whether you want to log one expense or get an overview of your monthly or yearly spending, this application is structured to support flexible, clear, and efficient expense tracking.

---

## Features

* User authentication (register, login, logout)
* Add expenses with:

  * Category
  * Description
  * Date (day/month/year)
* Filter and search expenses using:

  * Category
  * Specific Date (day/month/year)
  * Month only
  * Year only
* Backend and frontend validation
* Dynamic flash messages using Bootstrap
* Summarized total expenses
* Clean, responsive UI design
* Custom logo with pattern-based lettering and selected color palette

---

## Technologies Used

* **Backend**: Python 3, Flask
* **Database**: SQLite3
* **Frontend**: HTML5, CSS3, Bootstrap 5
* **Templating Engine**: Jinja2
* **Session Management**: Flask-Session

---

## Project Structure and File Description

```
project/
├── __pycache__/                   
├── flask_session/                
├── static/
│   ├── logo1.png                 
│   └── styles.css                
├── templates/
│   ├── apology.html              
│   ├── index.html               
│   ├── layout.html               
│   ├── login.html                
│   ├── register.html             
│   ├── search.html               
│   ├── table1.html               
│   └── table2.html               
├── app.py                        
├── expense.db                    
├── helpers.py                    
└── README.md                     
```

---

## Database Schema

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL,
    hash TEXT NOT NULL
);

CREATE TABLE expense (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INTEGER NOT NULL,
    day INTEGER,
    month TEXT,
    year INTEGER,
    category TEXT NOT NULL,
    description TEXT,
    amount INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id)
);
```

---

## Design Decisions and Validations

### Routing & Logic (in `app.py`)

* Used method checks (`GET`, `POST`) to control rendering and form submission.
* Implemented dynamic SQL queries for search using user input combinations.
* Avoided redundant validations: if frontend regex ensures year validity, backend skip additional parsing unless necessary.
* Used Python `datetime` module for robust validation of dates (when day and month are both present).

### Flash Messages

Implemented using Bootstrap's `alert` component with smooth fading effect:

```javascript
setTimeout(() => {
    const alert = document.getElementById("flash_message");
    if(alert) {
        alert.classList.remove("show");
        alert.addEventListener('transitionend', () => { alert.remove(); });
    }
}, 8000);
```

### Dynamic Expense Filtering

Search route is designed to handle various filtering combinations based on the user's inputs:

* Only Year
* Year + Category
* Year + Month
* Year + Day
* Year + Month + Day
* Year + Month + Category
* Year + Month + Day + Category

It builds the SQL query dynamically and calculates total expenditure using the result rows.

### Design Consistency

* Ensured reusable template blocks via `layout.html`.
* Used semantic tags (`<main>`, `<nav>`, etc.) for accessibility.
* Used `loop.index` in Jinja2 templates to auto-increment row numbers in tables.

### Logo Design

The logo `logo1.png` is designed  with colored polygon fragments representing each character. 

---

## Potential Improvements

* Visual representation of expenses using charts (e.g., bar, pie)
* Export data  PDF
* Password recovery mechanism

---

## Final Thoughts

This project began as a simple idea to track expenses but evolved into a flexible and well-validated application. Multiple combinations of filters were debated, and the decision to support day input without requiring month came from real-world scenarios where exact month isn't always needed. The use of `params` with unpacking (`*params`) in SQL queries ensures clean and secure execution.

Every piece of code was written with user experience in mind—from smooth UI transitions to helpful error feedback.

---

## Credits

Developed and designed by **Kunal Kumar** as a personal and educational project.

---

## License

This project is provided for personal, educational, and non-commercial use.
