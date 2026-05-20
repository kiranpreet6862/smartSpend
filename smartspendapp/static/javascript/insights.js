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





document.addEventListener("DOMContentLoaded", function () {
    var options = {
            series: [{ name: "Avg Spend", data: dailyPattern }],
            chart: {
                height: 230,
                type: 'bar',
                toolbar: { show: false }
            },
            plotOptions: {
                bar: {
                    borderRadius: 6,
                    columnWidth: '50%',
                    distributed: true
                }
            },
            colors: dailyPattern.map(function(val, index) {
                return (index === 5 || index === 6) ? '#ef4444' : '#16a085';
            }),
            legend: { show: false },
            dataLabels: { enabled: false },
            xaxis: {
                categories: dayNames,
                labels: { style: { fontSize: '13px' } }
            },
            yaxis: {
                min: 0,
                labels: {
                    style: { fontSize: '13px' },
                    formatter: function(val) {
                        return "₹" + (val / 1000).toFixed(0) + "k";
                    }
                }
            },
            grid: {
                borderColor: '#f1f1f1',
                strokeDashArray: 4
            },
            tooltip: {
                y: {
                    formatter: function(val) {
                        return "₹" + val.toLocaleString('en-IN');
                    }
                }
            }
        };

        var chart = new ApexCharts(document.querySelector("#dailyChart"), options);
        chart.render();
    });


// 

const itemCost = document.getElementById("itemCost");

const hoursWorked = document.getElementById("hoursWorked");

itemCost.addEventListener("input", function () {

    let amount = parseFloat(itemCost.value) || 0;

    let hourlyRate = 200;

    let hours = amount / hourlyRate;

    hoursWorked.innerText = hours.toFixed(1);

});

const editGoal = document.getElementById("edit_goal");
const cancelBtn = document.querySelector(".cancel_btn");
const goalDisplay = document.getElementById("card8");
const goalForm = document.getElementById("card8_edit");

editGoal.addEventListener("click", function() {
    goalDisplay.style.display = "none";
    goalForm.style.display = "block";  
});



cancelBtn.addEventListener("click", function() {
    goalDisplay.style.display = "block";
    goalForm.style.display = "none";  
});
