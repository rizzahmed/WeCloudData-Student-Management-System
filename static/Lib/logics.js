

// -------------------------- Universal Function -------------------------------

function getURL(path) {
    try {
        return `http://localhost:${window.location.port}/${path}`
    } catch(error) {
        console.error(error);
        return `http://localhost:${window.location.port}`
    }
}


function getRandomColor(existingColors) {
    let color;
    do {
        color = `rgb(${Math.floor(Math.random() * 256)}, 
                    ${Math.floor(Math.random() * 256)}, 
                    ${Math.floor(Math.random() * 256)})`;
    } while (existingColors.has(color)); // Ensure uniqueness

    existingColors.add(color); // Add color to the set to avoid duplicates
    return color;
}


async function getCall(apiUrl) {
    try {
        const response = await fetch(apiUrl, {
            method: "GET",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
            }
        });
    
        if (response.ok) {
            const data = await response.json();
            return data;
        } else
            throw new Error(`Get API Call failed! ${response}`);
    } catch(error) {
        throw new Error(`HTTP error! ${error}`);
    }
}


async function postCall(apiUrl, Obj) {
    try {
        const response = await fetch(apiUrl, {
            method: "POST",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
            },
            body: JSON.stringify(Obj),
        });
    
        if (response.ok) {
            const data = await response.json();
            return data;
        } else
            throw new Error(`Post API Call failed! ${response}`);
    } catch(error) {
        throw new Error(`HTTP error! ${error}`);
    }
}

function showErrorPopup(customMessage) {

    function closeErrorPopup(popup) {
        popup.classList.remove('show');
        setTimeout(function () {
          popup.remove();
        }, 300);
    }

    var errorPopup = document.createElement("div");
    errorPopup.className = "error-popup show";
    errorPopup.innerHTML = `
      <h3>Error</h3>
      <p>${customMessage}</p>
    `;
  
    var ErrorMessage = document.getElementById("ErrorMessage");

    ErrorMessage.insertBefore(errorPopup, ErrorMessage.firstChild);
  
    // Automatically close the popup after 3 seconds
    setTimeout(function () {
      closeErrorPopup(errorPopup);
    }, 3000); 
}


async function ReadGraphData(path) {
    try {
        let coursesName = [];
        let NumberOfStudents = [];
        apiURL = getURL(path);
        response = await getCall(apiURL);
        response.forEach(Obj => {
            coursesName.push(Obj.CourseName);
            NumberOfStudents.push(Obj.StudentCount);
        });
    
        return {"coursesName" : coursesName, "NumberOfStudents": NumberOfStudents}
    } catch(error) {
        showErrorPopup("Unable to Load Graph");
        console.error(error);
    }

}


function getRandomColor() {
    const r = Math.floor(Math.random() * 256);
    const g = Math.floor(Math.random() * 256);
    const b = Math.floor(Math.random() * 256);
    return `rgb(${r}, ${g}, ${b})`;
}


function generateUniqueColors(count) {
    const colors = new Set();
    while (colors.size < count) {
        colors.add(getRandomColor());
    }
    return Array.from(colors);
}


function resetForm() {
    element = document.getElementById("Model");
    element.innerHTML = '';
    element.classList.remove('model-active');
    currentStudentID = null
    // document.querySelector("form").reset();
}


// -------------------------- Student Function -------------------------------
let debounceStudentTimer;
function fetchStudents(query) {
    (async () => {

        const apiURL = getURL('searchStudent')
        Obj = {'params': query.trim()}
        data = await postCall(apiURL, Obj)
        renderStudentTable(data);

    })();
}

function debounceStudentSearch(event) {
    clearTimeout(debounceStudentTimer);
    debounceStudentTimer = setTimeout(() => {
        fetchStudents(event.target.value);
    }, 500); // 500ms debounce time
}

function renderStudentTable(data) {
    const tableBody = document.getElementById("studentTableBody");
    tableBody.innerHTML = "";

    data.forEach(student => {
        const row = `<tr>
            <td>${student.StudentID}</td>
            <td>${student.Name}</td>
            <td>${student.Email}</td>
            <td>${student.DOB}</td>
            <td class="editBtn tooltip">
            ...
                <div class="tooltiptext">
                    <span id="toolTipEditBtn" onclick="EditCourse(this)" data-ID="${student.ID }">Edit</span>
                    <span id="toolTipDeleteBtn"  onclick="DeleteStudent(this)" data-ID="${student.ID }">Delete</span>
                </div>
            </td>
        </tr>`;
        tableBody.innerHTML += row;
    });
}

function OpenStudentForm(){

    formCode = `
    <form action="#" method="POST">

        <h3 class="formHeading">Add New Student</h3>
        <div class="row">
            <label for="studentid">ID:</label>
            <input type="text" id="studentid" name="studentid" required>
        </div>

        <div class="row">
            <label for="name">Name:</label>
            <input type="text" id="name" name="name" required>
        </div>

        <div class="row">
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" required>
        </div>

        <div class="row">
            <label for="dob">DOB:</label>
            <input type="date" id="dob" name="dob" required>
        </div>

        <!-- Button Group: Submit & Cancel -->
        <div class="button-group">
            <button type="button" id="formCancelBtn" class="cancel-btn" onclick="resetForm()">Cancel</button>
            <button type="submit" class="submit-btn" onclick="saveStudent()">Submit</button>
        </div>
    </form>`

    element = document.getElementById("Model");
    element.innerHTML = '';
    element.innerHTML = formCode;

    element.classList.add('model-active');
}

function OpenStudentEditForm(payload){

    formCode = `
    <form action="#" method="POST">

        <h3 class="formHeading">Update Student</h3>
        <div class="row">
            <label for="studentid">ID:</label>
            <input type="text" id="studentid" name="studentid" required value="${payload.studentid}">
        </div>

        <div class="row">
            <label for="name">Name:</label>
            <input type="text" id="name" name="name" required value="${payload.name}">
        </div>

        <div class="row">
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" required value="${payload.email}">
        </div>

        <div class="row">
            <label for="dob">DOB:</label>
            <input type="date" id="dob" name="dob" required value="${payload.dob}">
        </div>

        <!-- Button Group: Submit & Cancel -->
        <div class="button-group">
            <button type="button" id="formCancelBtn" class="cancel-btn" onclick="resetForm()">Cancel</button>
            <button type="submit" class="submit-btn" onclick="saveStudent()">Submit</button>
        </div>
    </form>`

    element = document.getElementById("Model");
    element.innerHTML = '';
    element.innerHTML = formCode;

    element.classList.add('model-active');
}

function saveStudent(){
    event.preventDefault();
    
    // Disable the buttons
    // const button = event.target;
    // button.disabled = true;
    
    // formCancelBtn = document.getElementById("formCancelBtn");
    // formCancelBtn.disabled = true;
    
    const formData = {
        id: currentStudentID,
        studentid: document.getElementById("studentid").value,
        name: document.getElementById("name").value,
        email: document.getElementById("email").value,
        dob: document.getElementById("dob").value
    };

    (async () => {

        const apiURL = getURL('saveStudent')
        data = await postCall(apiURL, formData)
        if (data.status != true)
            showErrorPopup(data.message);
        else {
            console.log(data.message);
            location.reload();  
        }
           
        // button.disabled = false;
        // formCancelBtn.disabled = false;
    })();

}

var currentStudentID = null;
function EditStudent(element) {
    try {
        const studentID = element.getAttribute("data-ID");
        if (studentID.trim() == '')
            showErrorPopup('Invalid ID');
        else {

            // (async () => {

            let row = element.closest("tr");
            
            currentStudentID = studentID;
            const formData = {
                studentid: row.cells[0].innerText,
                name: row.cells[1].innerText,
                email: row.cells[2].innerText,
                dob: row.cells[3].innerText
            };
            OpenStudentEditForm(formData)
            
        }
    } catch (error) {
        
    }
}

function DeleteStudent(element) {
    try {

        const studentID = element.getAttribute("data-ID");
        if (studentID.trim() == '')
            showErrorPopup('Invalid ID');
        else {

            (async () => {

                const apiURL = getURL(`deleteStudent/${studentID}`)
                data = await getCall(apiURL)
                if (data.status != true)
                    showErrorPopup(data.message);
                else {
                    console.log(data.message);
                    location.reload();  
                }
                   
            })();
              
        }

        
    } catch (error) {

    }
}


// -------------------------- Course Function -------------------------------
let debounceCourseTimer;
function fetchCourses(query) {
    (async () => {

        const apiURL = getURL('searchCourse')
        Obj = {'params': query.trim()}
        data = await postCall(apiURL, Obj)
        renderCourseTable(data);

    })();
}

function debounceCourseSearch(event) {
    clearTimeout(debounceCourseTimer);
    debounceCourseTimer = setTimeout(() => {
        fetchCourses(event.target.value);
    }, 500); // 500ms debounce time
}

function renderCourseTable(data) {
    const tableBody = document.getElementById("courseTableBody");
    tableBody.innerHTML = "";

    data.forEach(course => {
        const row = `<tr>
            <td>${course.CourseName}</td>
            <td>${course.CourseCode}</td>
            <td>${course.Instructor}</td>
            <td>${course.Credits}</td>
            <td class="editBtn tooltip">
            ...
                <div class="tooltiptext">
                    <span id="toolTipEditBtn" onclick="EditCourse(this)" data-ID="${course.ID }">Edit</span>
                    <span id="toolTipDeleteBtn"  onclick="DeleteCourse(this)" data-ID="${course.ID }">Delete</span>
                </div>
            </td>
        </tr>`;
        tableBody.innerHTML += row;
    });
}

function OpenCourseForm(){

    formCode = `
    <form action="#" method="POST">

        <h3 class="formHeading">Add New Course</h3>
        <div class="row">
            <label for="studentid">ID:</label>
            <input type="text" id="studentid" name="studentid" required>
        </div>

        <div class="row">
            <label for="name">Name:</label>
            <input type="text" id="name" name="name" required>
        </div>

        <div class="row">
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" required>
        </div>

        <div class="row">
            <label for="dob">DOB:</label>
            <input type="date" id="dob" name="dob" required>
        </div>

        <!-- Button Group: Submit & Cancel -->
        <div class="button-group">
            <button type="button" id="formCancelBtn" class="cancel-btn" onclick="resetForm()">Cancel</button>
            <button type="submit" class="submit-btn" onclick="saveCourse()">Submit</button>
        </div>
    </form>`

    element = document.getElementById("Model");
    element.innerHTML = '';
    element.innerHTML = formCode;

    element.classList.add('model-active');
}

function OpenCourseEditForm(payload){

    formCode = `
    <form action="#" method="POST">

        <h3 class="formHeading">Update Course</h3>
        <div class="row">
            <label for="CourseName">Course Name:</label>
            <input type="text" id="CourseName" name="studentid" required value="${payload.CourseName}">
        </div>

        <div class="row">
            <label for="CourseCode">Course Code:</label>
            <input type="text" id="CourseCode" name="CourseCode" required value="${payload.CourseCode}">
        </div>

        <div class="row">
            <label for="Instructor">Instructor:</label>
            <input type="text" id="Instructor" name="Instructor" required value="${payload.Instructor}">
        </div>

        <div class="row">
            <label for="Credits">Credits:</label>
            <input type="text" id="Credits" name="Credits" required value="${payload.Credits}">
        </div>

        <!-- Button Group: Submit & Cancel -->
        <div class="button-group">
            <button type="button" id="formCancelBtn" class="cancel-btn" onclick="resetForm()">Cancel</button>
            <button type="submit" class="submit-btn" onclick="saveCourse()">Submit</button>
        </div>
    </form>`

    element = document.getElementById("Model");
    element.innerHTML = '';
    element.innerHTML = formCode;

    element.classList.add('model-active');
}

function saveCourse(){
    event.preventDefault();
    
    const formData = {
        id: currentCourseID,
        studentid: document.getElementById("studentid").value,
        name: document.getElementById("name").value,
        email: document.getElementById("email").value,
        dob: document.getElementById("dob").value
    };

    (async () => {

        const apiURL = getURL('saveCourse')
        data = await postCall(apiURL, formData)
        if (data.status != true)
            showErrorPopup(data.message);
        else {
            console.log(data.message);
            location.reload();  
        }
           
    })();

}


var currentCourseID = null;
function EditCourse(element) {
    try {
        const courseID = element.getAttribute("data-ID");
        if (courseID.trim() == '')
            showErrorPopup('Invalid ID');
        else {

            let row = element.closest("tr");
            
            currentCourseID = courseID;
            const formData = {
                CourseName: row.cells[0].innerText,
                CourseCode: row.cells[1].innerText,
                Instructor: row.cells[2].innerText,
                Credits: row.cells[3].innerText
            };
            OpenCourseEditForm(formData)
            
        }
    } catch (error) {
        
    }
}

function DeleteStudent(element) {
    try {

        const studentID = element.getAttribute("data-ID");
        if (studentID.trim() == '')
            showErrorPopup('Invalid ID');
        else {

            (async () => {

                const apiURL = getURL(`deleteStudent/${studentID}`)
                data = await getCall(apiURL)
                if (data.status != true)
                    showErrorPopup(data.message);
                else {
                    console.log(data.message);
                    location.reload();  
                }
                   
            })();
              
        }

        
    } catch (error) {

    }
}

// document.addEventListener("DOMContentLoaded", () => {
//     let storedValue = localStorage.getItem("activeMenu") || null;

//     fetch("/fetch", {
//         method: "POST",
//         headers: {
//             "Content-Type": "application/json"
//         },
//         body: JSON.stringify({ variable: storedValue })
//     })
//     .then(response => response.text()) // Get the HTML response
//     .then(html => {
//         document.open();
//         document.write(html); // Replace the page with the server-rendered template
//         document.close();
//     })
//     .catch(error => console.error("Error:", error));
// });


// document.addEventListener("DOMContentLoaded", function () {


    
//     // Select all images with the class "icons"
//     const icons = document.querySelectorAll(".icons");

//     icons.forEach(icon => {
//         icon.addEventListener("click", function () {
//             // Remove "active-menu" class from all icons
//             icons.forEach(i => i.classList.remove("active-menu"));

//             // Add "active-menu" class to the clicked icon
//             this.classList.add("active-menu");

//             // Update localStorage with the active menu
//             localStorage.setItem("activeMenu", this.alt);
//         });
//     });

//     // Load active menu from localStorage on page reload
//     const activeMenu = localStorage.getItem("activeMenu");
//     if (activeMenu) {
//         icons.forEach(icon => {
//             if (icon.alt === activeMenu) {
//                 icon.classList.add("active-menu");
//             }
//         });
//     }
// });

function navigatePage(url) {
    window.history.pushState({}, "", url); // Update URL without reloading
    window.location.href = url;  // Navigate to the new page
}









// async function SaveGpFigureConfig() {
//     // Update Figure Config
//     const currentPort = window.location.port;
//     const apiUrl = `http://localhost:${currentPort}/update-figure-config`;
//     const response = await fetch(apiUrl, {
//         method: "POST",
//         headers: {
//             Accept: "application/json",
//             "Content-Type": "application/json",
//         },
//         body: JSON.stringify({config: GpFigureDataset, figure: "Gp"}),
//     });

//     if (response.ok) {
//         const data = await response.json();
//         console.log(data);
//         showSuccessPopup("Gp Figure Config Updated!");
//         return data;
//     } else {
//         showErrorPopup("Can't Update Gp Figure Config");
//         throw new Error(`HTTP error! Status: ${response.status}`);
    
    

//     // Fetch Figuer Config from DB
//     const currentPort = window.location.port;
//     const apiUrl = `http://localhost:${currentPort}/read-figure-config`;
//     const response = await fetch(apiUrl, {
//         method: "GET",
//         headers: {
//             Accept: "application/json",
//             "Content-Type": "application/json",
//         }
//     });

//     if (response.ok) {
//         const data = await response.json();
//         // console.log(data)
//         return data;
//     } else {
//         showErrorPopup("Can't Load Figure Config");
//         throw new Error(`HTTP error! Status: ${response.status}`);
//     }
// }