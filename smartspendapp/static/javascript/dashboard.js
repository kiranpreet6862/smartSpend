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

    const maxVal = weeklyTotals.length > 0 ? Math.max(...weeklyTotals) : 10000;
    const yMax = maxVal + Math.round(maxVal * 0.15);

    var options = {
        series: [{
            name: "Spending",
            data: weeklyTotals
        }],
        chart: {
            height: 220,
            type: 'area',
            toolbar: { show: false }
        },
        stroke: {
            curve: 'smooth',
            width: 3
        },
        markers: {
            size: 5
        },
        colors: ['#16a085'],
        fill: {
            type: 'gradient',
            gradient: {
                opacityFrom: 0.4,
                opacityTo: 0.1
            }
        },
        xaxis: {
            categories: weeks,
            labels:{
                style:{
                    fontSize:'13px'
                }
            }
        },
        yaxis: {
            min: 0 ,
            max: yMax,
            labels: {
                style:{
                    fontSize:'13px'
                },
                formatter: function (val) {
                    return "₹" + (val / 1000).toFixed(0) + "k";
                }
            }
        },
        dataLabels: {
            enabled: false,
            style: {
                fontSize: '8px'   
            }
        },
        tooltip: {
            y:{
                formatter: function (val){
                    return "₹" + val.toLocaleString('en-IN');
                }
            }
        }

    };

    var chart = new ApexCharts(document.querySelector("#chart1"), options);
    chart.render();

});



document.addEventListener("DOMContentLoaded", function () {

    const scoreColor = healthScore >= 80 ? '#22c55e' :   // green — Excellent
                   healthScore >= 60 ? '#3b82f6' :   // blue  — Good  
                   healthScore >= 40 ? '#f59e0b' :   // amber — Fair
                                       '#ef4444';   // red   — Poor

    var options = {
        series: [healthScore],  

        chart: {
            height: 250,
            type: 'radialBar'
        },

        plotOptions: {
            radialBar: {
                hollow: {
                    size: '70%'
                },
                track: {
                    background: '#e5e7eb'
                },
                dataLabels: {
                    name: {
                        show: false
                    },
                    value: {
                        fontSize: '25px',
                        fontWeight: 600,
                        offsetY: 5,
                        formatter: function (val) {
                            return Math.round(val);  
                        }
                    }
                }
            }
        },

        colors: [scoreColor],  

        stroke: {
            lineCap: 'round'
        }

    };

    var chart = new ApexCharts(document.querySelector("#chart2"), options);
    chart.render();

});

document.addEventListener("DOMContentLoaded", function () {

    var options = {
        series: categoryData.map(item => item.total),

        chart: {
            type: 'donut',
            height: 170
        },

        labels: categoryData.map(item => item.category),

        colors: categoryData.map(item => item.color),

        legend: {
            show: false   
        },

        dataLabels: {
            enabled: false
        },

        stroke: {
            width: 2
        }

    };

    var chart = new ApexCharts(document.querySelector("#donutChart"), options);
    chart.render();

});

function togglemenu() {
    document.querySelector(".body_container").classList.toggle("active");
}