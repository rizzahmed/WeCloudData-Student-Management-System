try:
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from starlette.responses import HTMLResponse
    from starlette.templating import Jinja2Templates
    from starlette.requests import Request  # Add this import
    from fastapi.staticfiles import StaticFiles  # Import StaticFiles
    from fastapi.responses import JSONResponse, RedirectResponse
    import uvicorn
    
    from pydantic import BaseModel, EmailStr, Field, StringConstraints
    from typing import Optional, Annotated
    from datetime import date
    
    import common as comm
    from db_management import DBManager
except Exception as e:
    print(f"Error in Modules: {e}")
    
   
 
# ------------------- Server Configuration -------------------
app = FastAPI(debug=True) #For testing
# app = FastAPI() #For testing


# Enable CORS for all routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


static_dir = comm.getDirectoryPath("static")
templates_dir = comm.getDirectoryPath("templates")

# Mount the static directory
app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=templates_dir)
config = comm.ReadConfig()
PORT = config['ServerPort']
db = DBManager()


class DataModel(BaseModel):
    variable: Optional[str]


# Define ID with a specific pattern
StudentID = Annotated[str, StringConstraints(pattern=r"^\d{3}-\d{4}$")]

class StudentCreate(BaseModel):
    id: Optional[str]
    studentid: StudentID = Field(..., description="Student ID must be in the format '000-0000'")
    name: str = Field(..., min_length=1, description="Name cannot be empty")
    email: EmailStr = Field(..., description="Must be a valid email address")
    dob: date = Field(..., description="Date of Birth cannot be empty")
    

@app.get("/")
async def home(request: Request):
    return RedirectResponse(url="/students")


# Pages -----------------------------------------------------
@app.get("/students")
async def students(request: Request):
    try:
        tableHeadings, studentsData = await db.Read_Student() # Read All Students
        return templates.TemplateResponse("students.html", {"request": request, "key" : "StudentData", "tableHeadings": tableHeadings, "tableData": studentsData})
    except Exception as e:
        return templates.TemplateResponse("error.html", {"request": request, "error": str(e)}, status_code=500)

            
@app.get("/courses")
async def courses(request: Request):
    try:
        tableHeadings, courseData = await db.Read_Course() # Read All Courses
        return templates.TemplateResponse("courses.html", {"request": request, "key" : "CourseData", "tableHeadings": tableHeadings, "tableData": courseData})
    except Exception as e:
        return templates.TemplateResponse("error.html", {"request": request, "error": str(e)}, status_code=500)
            
            
@app.get("/enrollments")
async def enrollments(request: Request):
    try:
        enrollmentData = await db.Read_Student() # Read All Enrollments
        return templates.TemplateResponse("content.html", {"request": request})
    except Exception as e:
        return templates.TemplateResponse("error.html", {"request": request, "error": str(e)}, status_code=500)

       
            
# APIs ----------------------------------------------------- Graph
@app.get("/readBarData")
async def readBarData(request: Request):
    try:
        data = await db.Read_Bar_Chart()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/readPieData")
async def readPieData(request: Request):
    try:
        data = await db.Read_Pie_Chart()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# APIs ----------------------------------------------------- Student
@app.post("/searchStudent")
async def searchStudent(request: Request):
    try:
        req_body = await request.json()
        data = await db.Search_Student(req_body)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.post("/saveStudent")
async def saveStudent(request: Request, student: StudentCreate):
    try:
        req_body = student.dict()
        data = await db.Save_Student(req_body)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/deleteStudent/{ID}")
async def deleteStudent(ID: str):
    try:
        data = await db.Delete_Student(ID)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")



# APIs ----------------------------------------------------- Course
@app.post("/searchCourse")
async def searchCourse(request: Request):
    try:
        req_body = await request.json()
        data = await db.Search_Course(req_body)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.post("/saveCourse")
async def saveCourse(request: Request, student: StudentCreate):
    try:
        req_body = student.dict()
        data = await db.Save_Student(req_body)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/deleteStudent/{ID}")
async def deleteStudent(ID: str):
    try:
        data = await db.Delete_Student(ID)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


        
if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=PORT)

    