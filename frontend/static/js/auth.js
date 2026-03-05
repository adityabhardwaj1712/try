async function login() {

const email = document.getElementById("username").value;
const password = document.getElementById("password").value;

const response = await fetch("/login/", {
method: "POST",
headers: {
"Content-Type": "application/json"
},
body: JSON.stringify({
email: email,
password: password
})
});

if (response.ok) {
window.location.href = "/";
} else {
document.getElementById("error").innerText = "Invalid login";
}

}