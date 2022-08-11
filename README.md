# FastAPIHomework

## Description
### Welcome! This is 2022 MVCLab Summer training homework, it simulates a company's employee database, and supports finding the best available employee at the moment

### Setup Guide
* **How to run**
    * **Step 1: Install Python Packages**
        * > pip install -r requirements.txt
    * **Step 2: Run by uvicorn (Localhost)**
        * > uvicorn main:app --reload
        * Default host = 127.0.0.1, port = 8000
    * **Step 3: Test your API using Swagger UI**
        * http://127.0.0.1:8000/docs

## API Documentation
### GET Methods
    * > /list-employee
        * List all the employees data registered in server
    * > /get-employee-from-username
        * Find the employee name from its username
    * > /get-best-available-employee
        * Find the available employees with highest rating
### POST Methods
    * > /Update-Availability
        * Update registered employees availability, set to true for available
    * > /upload
        * Upload a file to the server
