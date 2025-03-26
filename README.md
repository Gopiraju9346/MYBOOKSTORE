Bookstore Management System

Project Overview

The Bookstore Management System is a web-based application developed using Flask (Python Web Framework) and MySQL as the database. It allows users to browse, purchase books, and manage their accounts, while administrators can manage products and orders efficiently.

Hosted Version

You can access the live version of this project here:
👉 Bookstore Management System

Features

User Features:

User Signup & Login (with OTP verification)

Browse Available Books

Add Books to Shopping Cart

Manage Cart Items (Add, Remove, Update)

Place Orders

View Order History

Reset Password (OTP-based verification)

Admin Features:

Admin Login

Add New Books (With details like name, genre, price, quantity, and image)

Manage Books (Edit, Delete books)

View and Manage Orders

Technologies Used

Backend: Flask (Python Framework)

Frontend: HTML, CSS, JavaScript

Database: MySQL (using pymysql library)

Email Services: SMTP (for OTP verification and password reset)

Hosting: Deployed on PythonAnywhere

Project Structure

📁 bookstore_project/
├── 📁 templates/         # HTML templates for frontend pages
├── 📁 static/            # Static files (CSS, JavaScript, Images)
├── app.py               # Main Flask application file
├── requirements.txt      # Required dependencies
├── README.md            # Project Documentation

Pages Created

User Pages

user_home.html

user_login.html

user_orders.html

user_signup.html

shopping_cart.html

otpverify.html

forgot_password.html

forgot_password1.html

forgot_password2.html

errorpage.html

update_users.html

Admin Pages

admin_login.html

admin_dashboard.html

admin_addproducts.html

admin_manageproducts.html

Installation & Setup

Clone the Repository

git clone https://github.com/yourusername/bookstore.git
cd bookstore

Create a Virtual Environment (Optional but Recommended)

python -m venv venv
source venv/bin/activate   # For Windows: venv\Scripts\activate

Install Dependencies

pip install -r requirements.txt

Setup MySQL Database

Create a database named bookstore in MySQL.

Update the db_config details in app.py.

Run the Application Locally

python app.py

Future Enhancements

Implement a payment gateway

Add user profile management features

Author

Gopi Raju Dodda
