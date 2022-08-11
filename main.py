'''
First, please install all the required packages
    > pip install -r requirements.txt
Then, run the server using uvicorn
    > uvicorn main:app --reload
'''

import os #for file path format
import json #json parsing
import shutil #fast file processing

#required packages for fastAPIs
from fastapi import FastAPI, HTTPException, UploadFile, Request
from fastapi.responses import JSONResponse
from typing import  Union
from pyquery import PyQuery
from pydantic import BaseModel
from uuid import uuid4 # Universally Unique Identifier

#pydantic BaseModel Class (Employee Data)
class Employee(BaseModel):
    username:str
    jobdesk: Union[str, None] = None #None means a trainee, no job yet
    rating: float #perfomance rating
    available_now: bool #whether available or not at the moment

app = FastAPI() #current FastAPI Object

#Exception when employee index not exist
class NoEmployee(Exception):
    def __init__(self, username:int):
        self.username = username

#Exception when data not exist from username
@app.exception_handler(NoEmployee)
def username_not_exist(request:Request, exc: NoEmployee):
    return JSONResponse (
        status_code= 401,
        content= {
            'Message' : f'Fault ! {exc.username} username not exist! Check again employee username!'
        }
    )

#Exception when file upload fails
class FileUploadFail(Exception):
    def __init__(self, filename: str):
        self.filename = filename

#Exception when data not exist from username
@app.exception_handler(FileUploadFail)
def file_upload_fail(request:Request, exc: FileUploadFail):
    return JSONResponse (
        status_code= 402,
        content= {
            'Message' : f'Fault ! {exc.filename} upload fail!'
        }
    )

#Load existing json data (if available)
dataName = 'Employees.json'
EmployeeData = []
my_file_names = []

#load json data
if os.path.exists(dataName):
    with open(dataName, "r") as file:
        EmployeeData = json.load(file)

#load all file names, to avoid future duplicate
for curPath in os.listdir():
    # check if current path is a file
    if os.path.isfile(curPath):
        my_file_names.append(curPath)

#Basic GET, welcome message
@app.get('/')
def root():
    return {"message": "Welcome! This API let you track our available employee at the moment!"}

#GET, return employee data JSON
@app.get('/list-employee')
def list_employee():
    if len(EmployeeData):
        return {"Employees": EmployeeData}
    else:
        return {"Message": "No Employee in JSON"}


#GET, return data of expected employee from his/her ID
@app.get('/get-employee-ID')
def get_employee_from_username(employee_username: str = "" ):
    if len(EmployeeData):
        for idx, obj in enumerate(EmployeeData):
            if(obj["username"] == employee_username):
                return{"employee data":obj}
        raise NoEmployee(username = employee_username)
    else:
        raise NoEmployee(username = employee_username)

#GET, return the best available employee username with highest rating
@app.get('/get-best-available')
def get_best_available():
    username = None
    current_rate = -1
    for idx, obj in enumerate(EmployeeData):
        if(obj["available_now"] and obj["rating"] > current_rate):
            current_rate = obj["current_rate"]
            username = obj["username"]
    
    if(username != None and current_rate > -1):
        return {"message", f"{username} is the best available employee at the moment!"}
    else:
        raise HTTPException(403, "No Employee Available!")

#POST, update an employee's availability from his/her username
@app.post('/Update-Available')
def update_available(employee_username: str = "", is_available : bool = True):
    if len(EmployeeData):
        for idx, obj in enumerate(EmployeeData):
            if(obj["username"] == employee_username):
                EmployeeData[idx]["available_now"] = is_available
                return
        raise NoEmployee(username = employee_username)
    else:
        raise NoEmployee(username = employee_username)

@app.post('/New-Employee', response_model = Employee)
def new_Employee(employee: Employee):
    employee_dict = employee.dict()

    #check for duplicate username
    for obj in EmployeeData:
        if(employee.username == obj["username"]):
            raise HTTPException(405, "Employee username already exist! Use another")
    
    #generate UUID with HEX
    employee_id = uuid4().hex
    employee_dict.update({"id": employee_id})
    EmployeeData.append(employee_dict)

    #update local JSON
    with open(dataName, "w") as f: 
        json.dump(EmployeeData, f, indent = 4)
    return employee_dict

#Upload file to the server
#need to install python-multipart and import shutil for saving
@app.post('/upload')
def upload_File(file: Union[UploadFile, None] = None):
    if not file: return {"message" : "No file upload"}
    try:
        filepath = './' + file.filename
        with open(filepath, "wb") as currentFile:
            shutil.copyfileobj(file.file, currentFile)
            file.close()
        my_file_names.append(file.filename)
        return {"Result" : "File upload success"}
    except:
        raise FileUploadFail(file.filename)