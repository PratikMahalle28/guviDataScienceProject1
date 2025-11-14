# guviDataScienceProject1
Client Query Management System: Organizing, Tracking, and Closing Support Queries
Problem Statement:
The Client Query Management System aims to provide a real-time interface for clients to submit queries and for support teams to manage them efficiently. The system uses a CSV dataset to simulate initial query logs, stores them in MySQL, and displays/query/modify them using Streamlit dashboards. The primary goal is to enhance communication between clients and support agents, improve query resolution speed, and track query status and performance metrics.
Business Use Cases:
Query Submission Interface: Allow clients to submit new queries in real-time.


Query Tracking Dashboard: Enable support teams to monitor and manage open/closed queries.


Service Efficiency: Measure how quickly support queries are resolved.


Customer Satisfaction: Faster query response leads to improved satisfaction.


Support Load Monitoring: Identify the most common types of queries and backlogs.
Approach:
🔐 1. Login System (Client & Support Team)
Each user (Client or Support) must register and log in to access the respective interface.
Credentials are stored in an SQL-compatible database (e.g., SQLite, MySQL, etc.).


Passwords are hashed securely using hashlib  or bcrypt (e.g., SHA-256) before storing in the database.



Login Flow:
User inputs: Username, Password, and Role (Client / Support).


The password is hashed using hashlib.sha256(password.encode()).hexdigest() before storing.


The users table contains:


username (TEXT),


hashed_password (TEXT),


role (TEXT).


Data is inserted using SQL queries like:





Login Flow:
User provides: Username and Password.


The password is hashed with the same hashing function.


The system checks for matching username and hashed_password in the database.

If authenticated:


If the role is Client → Redirect to Client Query Page.


If the role is Support → Redirect to Support Dashboard.




2. Query Insertion Page (Client Side)
Inputs:


Email ID


Mobile Number


Query Heading


Query Description


On Submission:


query_created_time is auto-generated using datetime.now()


status is marked as "Open" by default


query_closed_time remains NULL



3. Query Management Page (Support Team Side)
Support team can:


View and filter queries by status (Open/Closed) and category


Select and close an open query


On Closure:


status is updated to "Closed"


query_closed_time is auto-set using datetime.now()









Results: 
Fully functional web dashboard with:


Live query intake


Real-time monitoring and status updating


Insight into query trends, resolution times, and support load.
Project Evaluation metrics:
✅ Maintainable Code


✅ Portable Across Environments


✅ Public GitHub Repository


✅ Well-Documented README


✅ Streamlit UI with Forms and Tables


✅ Uses datetime and proper SQL Querying

Technical Tags:
Languages: Python
 Database: MySQL (using mysql-connector-python,SQL lite, no SQLAlchemy)
 Visualization Tools: Streamlit
 Libraries: Pandas, datetime, MySQL Connector
Data Set:
DataSet


Data Set Explanation:
CSV file with the following columns:
query_id


mail_id


mobile_number


query_heading


query_description


status (Open/Closed)


query_created_time


query_closed_time
Project Deliverables:
MySQL database containing cleaned query data


Python scripts for:


Inserting and updating MySQL using cursor-based SQL


Frontend via Streamlit


Streamlit app with 2 pages:


Client Submission Page


Support Team Dashboard
