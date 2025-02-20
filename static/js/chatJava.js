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