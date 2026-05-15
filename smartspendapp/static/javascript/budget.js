function togglemenu() {
    document.querySelector(".body_container").classList.toggle("active");
}

function darkmode(){

    document.body.classList.toggle("dark");

    const modeText = document.querySelector(".mode-text");

    if(document.body.classList.contains("dark")){
        localStorage.setItem("theme", "dark");
        modeText.innerText = "Light Mode";
    } 
    else{
        localStorage.setItem("theme", "light");
        modeText.innerText = "Dark Mode";
    }
}

window.onload = function(){

    const modeText = document.querySelector(".mode-text");

    if(localStorage.getItem("theme") === "dark"){
        document.body.classList.add("dark");
        modeText.innerText = "Light Mode";
    }

}

const editBtn = document.getElementById("edit_btn");
const editBtn2 = document.getElementById("edit_btn2");
const budgetDisplay = document.getElementById("budget_display");
const budgetForm = document.querySelector("#budget_form");
const cancelBtn = document.querySelector(".cancel_btn");

editBtn.addEventListener("click", function() {
    budgetDisplay.style.display = "none";
    budgetForm.style.display = "block";
});
editBtn2.addEventListener("click", function() {
    budgetDisplay.style.display = "none";
    budgetForm.style.display = "block";
});

cancelBtn.addEventListener("click", function() {
    budgetDisplay.style.display = "flex";
    budgetForm.style.display = "none";
    
});