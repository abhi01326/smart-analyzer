const API = "http://127.0.0.1:8000/api/tasks";
document.getElementById("task-form").onsubmit = async (e) => {
    e.preventDefault();
    const payload = {
        title: document.getElementById("title").value.trim(),
        due_date: document.getElementById("due_date").value,
        estimated_hours: parseFloat(document.getElementById("hours").value),
        importance: parseInt(document.getElementById("importance").value),
        dependencies: document.getElementById("dependencies").value
            ? document.getElementById("dependencies").value.split(",").map(x=>parseInt(x.trim()))
            : []
    };

    await fetch(`${API}/create/`, {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify(payload)
    })
    .then(res => res.json())
    .then(data => console.log(data))
    .catch(err => console.log(err))
    ;
    
    document.getElementById("title").value = "";
    document.getElementById("due_date").value = "";
    document.getElementById("hours").value = "";
    document.getElementById("importance").value = "";
    document.getElementById("dependencies").value = "";
    loadTasks();
    
};

async function loadTasks() {
    const res = await fetch(`${API}/list/`);
    const data = await res.json();
    display(data.tasks);
}

document.getElementById("analyze-btn").onclick = async () => {
    const mode = document.getElementById("mode").value;

    const res = await fetch(`${API}/analyze/?mode=${mode}`, { method: "POST" });
    const data = await res.json();
    display(data.tasks);
};

function display(tasks) {
    const div = document.getElementById("results");
    div.innerHTML = "";

    tasks.forEach(task => {
        const box = document.createElement("div");
        box.className = "task-card";

        box.innerHTML = `
            <div>
            <div class="task-title">${task.title}</div>
            <p id="score">Score: ${task.score ?? ""}</p>
            <p>Due: ${task.due_date}</p>
            </div>
            <div class="task-info-2">
            <p>Importance: ${task.importance}</p>
            <p>Hours: ${task.estimated_hours}</p>
            <p>Dependencies: ${task.dependencies.join(", ")}</p>
            </div>
        `;

        div.appendChild(box);
    });
}

// AUTO LOAD TASKS
window.addEventListener("DOMContentLoaded", loadTasks);
