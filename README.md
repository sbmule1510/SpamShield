# SpamShield – Email Spam Classifier

## Project Overview

SpamShield is a web-based Email Spam Detection System developed using Django and MongoDB. It allows users to register, log in, and detect whether an email is Spam or Safe using Regex Pattern Analysis and predefined spam keywords. Users can also upload text files for batch email detection, view detection history, check statistics, and access the REST API.

## Features

- User Registration
- User Login & Logout
- Email Spam Detection
- Regex Pattern Analysis
- URL Detection
- ALL CAPS Detection
- Batch Email File Upload (.txt)
- Detection History
- Delete History
- Statistics Dashboard (Total, Spam, Safe)
- User Profile
- REST API (DRF)

## Technologies Used

### Frontend
- HTML
- CSS
- Bootstrap
### Backend
- Python
- Django
### Database
- MongoDB
### Python Concepts
- Lists
- Dictionary
- String Methods
- Functions
- OOP (Email, SpamRule, SpamClassifier)
- Regex
- Threading
- Exception Handling
- File I/O
### API
- Django REST Framework (DRF)
### IDE
- Visual Studio Code
### Version Control
- Git
- GitHub

## Software Requirements

- Python 3.13 (or above)
- Django
- MongoDB
- Visual Studio Code
- Git (Optional)

## How to Run the Project
### Step 1
Download or clone the project from GitHub.
### Step 2
Open the project in Visual Studio Code.
### Step 3
Create and activate the virtual environment.
### Step 4
Install the required packages.
### Step 5
Start MongoDB Server.
### Step 6
Run the Django server.
### Step 7
Open the application in your browser.
Example:
http://127.0.0.1:8000/
### Step 8
Register a new account.
### Step 9
Login using your credentials.
### Step 10
Enter the Email Subject and Message or upload a `.txt` file.
### Step 11
Click **Check Spam** to classify the email.
### Step 12
View Detection History, Statistics, or Delete History as required.

## Database
MongoDB is used to store:

- User Information
- Email Detection History

### Collections

- users
- history
