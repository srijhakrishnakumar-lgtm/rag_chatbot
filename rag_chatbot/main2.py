from fastapi import FastAPI
from pydantic import BaseModel,EmailStr
app=FastAPI()
students={}
class details(BaseModel):
    name:str
    age:int
    email:EmailStr
    department: str
    cgpa:float

@app.get("/detailsforsignup")
def details_for_signup(student:details):
    if student.email in students:
        return{"message":"student with this email id already exist"}
    students[student.email]={
        "name":student.name,
        "age":student.age,
        "Email":student.email,
        "Depaertment":student.department,
        "cgpa":student.cgpa
    }
    return {"student details added successfully"}
gsk_3CADm3aqzXtn15uYE6l8WGdyb3FYcf1P5e8Mz0pkv3HhQ0AWqmSrgsk_3CADm3aqzXtn15uYE6l8WGdyb3FYcf1P5e8Mz0pkv3HhQ0AWqmSr

