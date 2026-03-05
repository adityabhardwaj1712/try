const token = localStorage.getItem("access");

if (!token) {
    window.location.href = "login.html";
}

function logout() {
    localStorage.removeItem("access");
    window.location.href = "login.html";
}

function showCreateForm() {
    document.getElementById("create-form").classList.toggle("hidden");
}

async function loadProjects() {
    const response = await fetch("http://localhost:8000/api/projects/", {
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    const data = await response.json();

    const container = document.getElementById("project-list");
    container.innerHTML = "";

    data.forEach(project => {
        container.innerHTML += `
            <div class="card">
                <h3>${project.name}</h3>
                <p>${project.description}</p>
            </div>
        `;
    });
}

async function createProject() {
    const name = document.getElementById("project-name").value;
    const description = document.getElementById("project-desc").value;

    const response = await fetch("http://localhost:8000/api/projects/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({
            name,
            description
        })
    });

    if (response.ok) {
        loadProjects();
        document.getElementById("create-form").classList.add("hidden");
    }
}

loadProjects();