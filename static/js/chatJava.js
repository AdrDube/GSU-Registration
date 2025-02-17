document.addEventListener("DOMContentLoaded", function() {
    let btn = document.querySelector(".menu-btn"); 
    let menu = document.querySelector(".menu-list"); 
    
    btn.addEventListener("click", function(event) {
        console.log("button clicked")
        event.stopPropagation();
        menu.classList.toggle("show");
    });

    document.addEventListener("click", function(event) {
        console.log("clicked outside")
        if (!btn.contains(event.target) && !menu.contains(event.target)) {
            menu.classList.remove("show");
        }
    });
});

/* JavaScript for choosing the classes */
document.addEventListener("DOMContentLoaded", function () {
    console.log("Script Loaded");
    const form = document.getElementById("schedule-form");
    const classSelect = document.getElementById("class-select");
    const timeSelect = document.getElementById("time-select");
    const submitBtn = document.getElementById("submit-btn");
    const removeSelect = document.getElementById("remove-select");
    const removeBtn = document.getElementById("remove-btn");
    const scheduleTable = document.querySelector(".schedule-table table").getElementsByTagName("tbody")[0];
    

    
    let classSchedule = {}; 

    submitBtn.addEventListener("click", function () {
        console.log("Submit button clicked!");
        const selectedClass = classSelect.value;
        const DateTime = timeSelect.value.split(" ");
        const days = DateTime[0].split(""); 
        const startTime = DateTime[1];
        console.log('class name: ${selectedClass}')
       
        const dayMap = { "M": 1, "T": 2, "W": 3, "R": 4, "F": 5 };

    
        const timeMap = {
            "08:00": 0, "09:00am": 1, "10:00am": 2, "11:00am": 3, "12:00pm": 4,
            "01:00pm": 5, "02:00pm": 6, "03:00pm": 7, "04:00pm": 8, "05:00pm": 9, "06:00pm": 10
        };

        let row = timeMap[startTime];
        let indices = [];

        console.log(row)

        days.forEach(day => {            
            let col = dayMap[day]; 
            console.log(`Row: ${row}, Column: ${col}`);
            indices.push([row, col]); 

             
            let cell = scheduleTable.rows[row].cells[col]; // Adjust for zero-based index
            console.log(`Updating cell at Row: ${row}, Col: ${col}`, cell);
            if (cell.innerHTML.trim() !== "") {
                // The cell already has content
                alert("Conflict")
                console.log("Cell is not empty!");
            } else {
                // The cell is empty, proceed with setting innerHTML
                cell.innerHTML = `<div class="class-entry">
                    ${selectedClass} <br>  
                    ${DateTime[0]} <br>
                    ${DateTime.slice(1).join(" ")}
                </div>`;
            }
                
        

            classSchedule[selectedClass] = indices;
            updateRemoveDropdown();
        }        
    );


    function updateRemoveDropdown() {
        removeSelect.innerHTML = '<option value="">-- Select a Class --</option>';
        Object.keys(classSchedule).forEach(className => {
            let option = document.createElement("option");
            option.value = className;
            option.textContent = className;
            removeSelect.appendChild(option);
        });
    }

    removeBtn.addEventListener("click", function () {
        const selectedClass = removeSelect.value;
        if (selectedClass) {
            removeClass(selectedClass);
        }
    });

    function removeClass(className) {
        if (classSchedule[className]) {
            classSchedule[className].forEach(([row, col]) => {
                let cell = scheduleTable.rows[row].cells[col];
                cell.innerHTML = "";
            });
            delete classSchedule[className];
            updateRemoveDropdown();
        }
    }
    }) 
})
