from flask import Flask, render_template, request, redirect

todo = Flask(__name__)

def read_tasks():
    try:
        with open("tasks.txt", "r") as file:
            return [line.strip().split("|") for line in file]
    except FileNotFoundError:
        return []

def write_tasks(tasks):
    with open("tasks.txt", "w") as file:
        for t in tasks:
            file.write("|".join(t) + "\n")

@todo.route("/")
def front():
    tasks = read_tasks()
    return render_template("front.html", tasks=tasks)

@todo.route("/add", methods=["POST"])
def add_task():
    task = request.form.get("task")
    review = request.form.get("review")
    if task:
        with open("tasks.txt", "a") as file:
            file.write(f"0|{task}|{review}\n")   # 0 = not completed
    return redirect("/")

@todo.route("/toggle/<int:index>")
def toggle_task(index):
    tasks = read_tasks()
    if 0 <= index < len(tasks):
        tasks[index][0] = "1" if tasks[index][0] == "0" else "0"
        write_tasks(tasks)
    return redirect("/")

@todo.route("/delete/<int:index>")
def delete_task(index):
    tasks = read_tasks()
    if 0 <= index < len(tasks):
        tasks.pop(index)
        write_tasks(tasks)
    return redirect("/")

if __name__ == "__main__":
    todo.run(debug=True)
