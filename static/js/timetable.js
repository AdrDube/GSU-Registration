
document.addEventListener("DOMContentLoaded", function () {
     const schedule = JSON.parse('{{ schedule | safe }}');
     const dayMap = { "M": 1, "T": 2, "W": 3, "R": 4, "F": 5 };
     const timeMap = {
         "08": 0, "09": 1, "10": 2, "11": 3, "12": 4,
         "13": 5, "14": 6, "15": 7, "16": 8, "17": 9, "18": 10
         };
    const scheduleTable = document.getElementById("scheduleTable");
    const classSchedule = {};

     function createTimeTable(schedule) {
         // Iterate over each subject in the schedule
         for (const [id, details] of Object.entries(schedule)) {
             const startTime = details.converted_time[0]; // Extract starting time
             const time= details.time
             const subject = details.subject;
             const days = details.days;
             const hours = startTime.split(":")[0];

            let row = timeMap[hours];
            let indices = [];

            days.split("").forEach(day => {            
                let col = dayMap[day]; 
                indices.push([row, col]); 
                let cell = scheduleTable.rows[row].cells[col];

                // Check to see if cell already has content
                if (cell.innerHTML.trim() !== "") {
                    alert("Conflict")
                } else {
                    // The cell is empty, proceed with setting innerHTML
                    cell.innerHTML = `<div class="class-entry">
                        ${id} <br>  
                        ${subject} <br>
                        ${time}
                        </div>`;
                    }
            classSchedule[id] = indices;
        });
    };
}
    createTimeTable(schedule);
});