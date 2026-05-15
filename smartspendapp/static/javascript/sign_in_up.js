document.addEventListener("DOMContentLoaded", function () {

    const signInForm = document.querySelector(".sign-in-form");
    const signUpForm = document.querySelector(".sign-up-form");

    const title = document.querySelector(".right-container h1");
    const text = document.querySelector(".right-container > p");

    function switchToSignUp() {
        signInForm.style.display = "none";
        signUpForm.style.display = "block";
        if (title) title.innerText = "Create Account";
        if (text) text.innerText = "Start tracking your finances in seconds.";
        document.querySelectorAll(".sign-in-btn").forEach(b => b.classList.remove("active-btn"));
        document.querySelectorAll(".sign-up-btn").forEach(b => b.classList.add("active-btn"));
    }

    function switchToSignIn() {
        signUpForm.style.display = "none";
        signInForm.style.display = "block";
        if (title) title.innerText = "Welcome Back!";
        if (text) text.innerText = "Sign in to access your financial dashboard.";
        document.querySelectorAll(".sign-up-btn").forEach(b => b.classList.remove("active-btn"));
        document.querySelectorAll(".sign-in-btn").forEach(b => b.classList.add("active-btn"));
    }

    document.querySelectorAll(".sign-up-btn").forEach(btn => {
        btn.addEventListener("click", function (e) {
            e.preventDefault();
            switchToSignUp();
        });
    });

    document.querySelectorAll(".sign-in-btn").forEach(btn => {
        btn.addEventListener("click", function (e) {
            e.preventDefault();
            switchToSignIn();
        });
    });

    
    const formType = document.body.getAttribute("data-form");
    if (formType === "signup") switchToSignUp();
    else switchToSignIn(); 
});

