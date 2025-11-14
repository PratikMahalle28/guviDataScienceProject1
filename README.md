# guviDataScienceProject1
Client Query Management System: Organizing, Tracking, and Closing Support Queries
Problem Statement:
The Client Query Management System aims to provide a real-time interface for clients to submit queries and for support teams to manage them efficiently. The system uses a CSV dataset to simulate initial query logs, stores them in MySQL, and displays/query/modify them using Streamlit dashboards. The primary goal is to enhance communication between clients and support agents, improve query resolution speed, and track query status and performance metrics.

Description:-
This project is a web-based application for managing client query management support organizing, tracking and closing support queries. It is built using the Streamlit framework for the front end and utilizes a MySQL database for data persistence. The application provides distinct interfaces for Clients (submitting issues) and Support Team members (managing and resolving tickets).

Table of Contents
1.Features
2.Prerequisites
3.Installation and Setup
 1. Database Configuration
 2. Project Dependencies
 3. Running the Application
4.Usage Guide
 i.  User Authentication
 ii. Client Workflow
 iii.Support Workflow
5.Technical Details 

1.Features
 i.Secure Authentication: User registration and login using role-based access control (Client vs. Support). Passwords are securely hashed using SHA-256 before storage.
 ii.Query Submission: A dedicated interface for clients to submit new support tickets with contact email, contact details, categories, headings, and descriptions.
 iii.Support Dashboard: A comprehensive dashboard for support agents to view, filter (by status and category), and manage open queries.
 iv.Automatic Tracking: Automated tracking of query creation and closure timestamps.
 v.Query Assignment: Tickets are automatically assigned to the support agent who closes them.
 
2.Prerequisites
 Ensure you have the following installed before proceeding:
  i.Python 3.8 or higher.
  ii.MySQL Database
  iii.VSCODE

3.Installation and Setup
 i. Database Configuration
    The application is configured to connect to a MySQL database named querysystem.
    Ensure your MySQL service is active.
    Create the required database using your MySQL client:
     sql 
     CREATE DATABASE IF NOT EXISTS querysystem; 
     Use code with caution.
     Update Connection Credentials: You must modify the get_db_connection() function within the provided Python code (app.py) to match your local MySQL username and password:
     python
     def get_db_connection():
     # ...
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="YOUR_MYSQL_PASSWORD_HERE", # <-- UPDATE THIS LINE
            database='querysystem',
            autocommit=True
        )
      # ... 
  ii. Project Dependencies
  Install the necessary Python libraries using pip:
  "
  pip install streamlit mysql-connector-python pandas
  "
  iii. Running the Application
       Save all the provided Python source code into a single file named app.py.
       Launch the application from your terminal using the Streamlit CLI:
       "
        streamlit run app.py
       "
      The application will automatically open in your default web browser (usually http://localhost:8501).
      
4.Usage Guide
  Upon the first run, the database tables (users and queries) will be automatically created.
  i.User Authentication
       Use the sidebar navigation to switch between Login and Register pages.
       Register at least one user with the Client role and one with the Support role to explore all system features.
  ii.Client Workflow
       Log in using a Client account.
       The interface redirects you to the Submit a New Query page.
       Fill out the required information (Email, Mobile, Category, Title, Details).
       Click Submit Query. The ticket is created with Status: Open.
  iii.Support Workflow
       Log in using a Support account.
       The interface redirects you to the Support Dashboard.
       Use the filters to view queries.
       Select a query and click the Close Query button to mark it as resolved. The system records your user ID and the closing time automatically.
       
5.Technical Details
  The application follows a modular structure:
  Database Management Functions: Handled by the mysql-connector-python library (get_db_connection, setup_database, etc.).
  Authentication Logic: Implements hashlib.sha256 for secure password handling.
  UI/UX: Managed entirely by the Streamlit framework, providing a responsive web interface without complex HTML/CSS/JS.



















