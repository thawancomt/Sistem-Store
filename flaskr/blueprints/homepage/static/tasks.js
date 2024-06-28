
const task_panel = document.getElementById("task_panel");
const task_show_btn = document.getElementById("show_tasks_btn");


function active_task_panel() {
    if (!task_panel.hasAttribute('hidden')) {
        task_panel.setAttribute('hidden', true);
        task_show_btn.innerHTML = "Show Tasks"
    } else {
        task_panel.removeAttribute('hidden');
        task_show_btn.innerHTML = "Hide Tasks"
    }
}

task_show_btn.addEventListener('click', active_task_panel)