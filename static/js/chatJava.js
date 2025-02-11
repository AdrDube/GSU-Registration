document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("schedule-form");
    const classSelect = document.getElementById("class-select");
    const timeSelect = document.getElementById("time-select");
    const submitBtn = document.getElementById("submit-btn");
    const undoBtn = document.getElementById("undo-btn"); 
    const scheduleTable = document.getElementById("schedule-table").getElementsByTagName("tbody")[0];

    let lastRemoved = null; // 🔥 Store the last removed class

    const times = ["08:00am", "09:00am", "10:00am", "11:00am", "12:00pm", "01:00pm", "02:00pm", "03:00pm", "04:00pm", "05:00pm", "06:00pm"];
    times.forEach(time => {
        let row = scheduleTable.insertRow();
        row.insertCell(0).textContent = time;
        for (let i = 1; i <= 7; i++) {
            let cell = row.insertCell(i);
            cell.setAttribute("data-day", i);
            cell.setAttribute("data-time", time);
            cell.addEventListener("click", removeClass); // 🔥 Click to remove
        }
    });

    submitBtn.addEventListener("click", function () {
        const selectedClass = classSelect.value;
        const selectedTime = timeSelect.value;
        const [days, timeRange] = selectedTime.split(" ");
        const [startTime] = timeRange.split("-");

        let timeIndex = times.indexOf(startTime);
        if (timeIndex !== -1) {
            const dayMapping = { "MWF": [2, 4, 6], "TTh": [3, 5] };
            const daysArray = dayMapping[days] || [];

            daysArray.forEach(day => {
                let cell = scheduleTable.rows[timeIndex].cells[day];

                if (cell.textContent) {
                    alert("This time slot is already occupied! Remove it first.");
                    return;
                }

                cell.textContent = selectedClass;
                cell.style.backgroundColor = "#d3d3d3";
                cell.setAttribute("data-class", selectedClass);
            });
        }
    });

    // 🔥 Function to Remove a Class and Enable Undo
    function removeClass(event) {
        let cell = event.target;
        if (cell.textContent) {
            lastRemoved = {
                className: cell.textContent,
                day: cell.getAttribute("data-day"), 
                time: cell.getAttribute("data-time")
            };

            let confirmDelete = confirm(`Remove "${cell.textContent}" from the schedule?`);
            if (confirmDelete) {
                cell.textContent = "";
                cell.style.backgroundColor = "";
                cell.removeAttribute("data-class");

                undoBtn.disabled = false; // 🔥 Enable Undo button
            }
        }
    }

    // 🔥 Undo Function: Restore Last Removed Class
    undoBtn.addEventListener("click", function () {
        if (lastRemoved) {
            let { className, day, time } = lastRemoved;
            let rowIndex = times.indexOf(time);
            let cell = scheduleTable.rows[rowIndex].cells[day];

            if (!cell.textContent) { // Only restore if cell is still empty
                cell.textContent = className;
                cell.style.backgroundColor = "#d3d3d3";
                cell.setAttribute("data-class", className);
            }

            lastRemoved = null; // 🔥 Clear last removed record
            undoBtn.disabled = true; // 🔥 Disable Undo button again
        }
    });

    undoBtn.disabled = true; // 🔥 Initially disable Undo button
});


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

