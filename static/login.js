let mode = "login";

const formTitle = document.getElementById("form-title");
const submitBtn = document.getElementById("submit-btn");
const switchText = document.getElementById("switch-text");
const switchLink = document.getElementById("switch-link");
const repeatPassword = document.getElementById("repeat-password");
const errorMsg = document.getElementById("error-msg");

switchLink.addEventListener("click", (e) => {
    e.preventDefault();

    if (mode === "login") {
        mode = "register";
        formTitle.textContent = "Sign up";
        submitBtn.textContent = "Sign up";
        switchText.textContent = "Already have an account?";
        switchLink.textContent = "Sign in";
        repeatPassword.style.display = "block";
    } else {
        mode = "login";
        formTitle.textContent = "Sign in";
        submitBtn.textContent = "Sign in";
        switchText.textContent = "Don't have an account?";
        switchLink.textContent = "Sign up";
        repeatPassword.style.display = "none";
    }

    errorMsg.textContent = "";
});

document.getElementById("auth-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const login = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const repeat = repeatPassword.value;

    if (mode === "register" && password !== repeat) {
        errorMsg.textContent = "Passwords do not match";
        return;
    }

    const url = mode === "login" ? "/api/login" : "/api/register";

    const res = await fetch(url, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({login, password})
    });

    if (!res.ok) {
        errorMsg.textContent = res.status + ":" + res.statusText;
        return;
    }

    if (window.socket && window.socket.connected) {
        window.socket.disconnect();
        window.socket.connect();
    }

    const data = await res.json();

    window.location.href = "/";
});
