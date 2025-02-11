document.addEventListener("DOMContentLoaded", function () {
    const scheduleTable = document.getElementById("schedule-table").getElementsByTagName("tbody")[0];

    const times = ["08:00am", "09:00am", "10:00am", "11:00am", "12:00pm", "01:00pm", "02:00pm", "03:00pm", "04:00pm", "05:00pm", "06:00pm"];
    times.forEach(time => {
        let row = scheduleTable.insertRow();
        row.insertCell(0).textContent = time;
        for (let i = 1; i <= 7; i++) {
            let cell = row.insertCell(i);
            cell.setAttribute("data-day", i);
            cell.setAttribute("data-time", time);
            cell.addEventListener("click", removeClass);
        }
    });

    // 🔥 Function to Remove a Class and Enable Undo
    function removeClass(event) {
        let cell = event.target;
        if (cell.textContent) {
            let confirmDelete = confirm(`Remove "${cell.textContent}" from the schedule?`);
            if (confirmDelete) {
                cell.textContent = "";
                cell.style.backgroundColor = "";
                cell.removeAttribute("data-class");
            }
        }
    }

});


