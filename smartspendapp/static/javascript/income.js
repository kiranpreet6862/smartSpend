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

function updateSlider() {
    let value = slider.value;

    
    localStorage.setItem("savingsRate", value);
    localStorage.setItem("projectedSavings", savings);

   
    document.getElementById("savings_rate_input").value = value;
}


slider.addEventListener("change", function () {
    document.getElementById("savings_form").submit();
});