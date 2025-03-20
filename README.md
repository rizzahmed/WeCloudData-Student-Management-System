# WeCloudData-Student-Management-System
Assessment Codebase for WeCloudData


## Overview
A full-stack Student Management System built using FastAPI and HTML/CSS/Javascript. This project allows users to manage students, courses, and enrollments with a dashboard for data visualization.

---


## Features

Dashboard: Visualize data such as student distributions across courses.
Student Management: Create, read, update, and delete students.
Course Management: Create, read, update, and delete courses.
Enrollments (Upcoming): Manage student enrollments in courses.

---


## Tech Stack

Backend
Framework: FastAPI (for creating RESTful APIs)
Database: MySQL (Store Procedure)
Data Validation: Pydantic
Authentication & Authorization: (Planned for future updates)
Frontend (HTML/CSS/Javascript)
Dashboard: Data visualizations using Chart.js

---


## Deployment
Docker & Docker Compose for containerized deployment. (Not Deployed, Still in Progress)

---


Getting Started
1. Clone the Repository
2. Setup a Virtual Environment (Optional but Recommended)
3. Install Dependencies (through requirements.txt)
4. Set Up Environment Variables

Create a .env file in the project root and configure the database settings:
5. Run Database Migrations
    This will create the required tables in the database. (Find Database file in repo)

6. Start the FastAPI Server
    The API will be available at:

The interactive API documentation can be accessed at:
7. (Optional) Run Using Docker

---


## Future Improvements
✅ Add Authentication & Authorization
✅ Improve UI with React Dashboard
✅ Add Enrollment CRUD Operations (Now Implemented!)
✅ Implement Unit Tests for API Endpoints
✅ Enhance API Logging & Error Handling

---


## Contributing
Contributions are welcome! If you’d like to contribute:

Fork the repository.
Create a new branch (feature-branch-name).
Commit your changes and push to your fork.
Open a pull request.

---


## License
This project is licensed under the MIT License.

---


## Contact
If you have any questions, feel free to reach out at rizahmd789@gmail.com or create an issue in the repository.