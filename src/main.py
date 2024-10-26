import sys
import subprocess
import re


#region data_structures

class Task:
    def __init__(self, name, dependencies=None, actions=None, is_private=False):
        self.name = name
        self.dependencies = dependencies or []
        self.actions = actions or []
        self.is_private = is_private

    def execute(self, executed_tasks, shortcuts_dif):
        # Execute dependencies first
        for dep_name in self.dependencies:
            # Get the Task object corresponding to the dependency name
            dep_task = executed_tasks.get(dep_name, None)

            if dep_task is None:
                # If the dependency task is not executed yet, fetch it from the tasks dictionary
                dep_task = build_system.tasks[dep_name]  # Assuming build_system is accessible
                dep_task.execute(executed_tasks, shortcuts_dif)
                # After executing, add it to the executed tasks
                executed_tasks[dep_name] = dep_task

        # Execute task actions
        if self.name not in executed_tasks:
            #print(f"Executing {self.name}...")
            for action in self.actions:
                # Replace shortcuts in actions
                action = replace_shortcuts(action, shortcuts_dif)
                run_command(action)
            executed_tasks[self.name] = self


class BuildSystem:
    def __init__(self, tasks, shortcuts):
        self.tasks = tasks
        self.shortcuts = shortcuts

    def run_task(self, task_name):
        if task_name not in self.tasks:
            print(f"Task '{task_name}' not found.")
            sys.exit(1)

        executed_tasks = {}
        task = self.tasks[task_name]
        if task.is_private:
            print(f"Task '{task_name}' is private!")
            sys.exit(2)
        task.execute(executed_tasks, self.shortcuts)

#endregion


def run_command(command):
    """Runs a shell command"""
    #print(f"Running: {command}")
    subprocess.run(command, shell=True, check=True)


def replace_shortcuts(action, shortcuts):
    """Replace all $(shortcut) with their values in the action"""
    for key, value in shortcuts.items():
        action = action.replace(f"$({key})", value)
    return action


def parse_build_file(build_file_path):
    tasks = {}
    shortcuts = {}
    current_task = None

    with open(build_file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):  # Ignore empty lines and comments
                continue

            # Handle shortcuts (e.g., GCC = gcc main.c -o main)
            if "=" in line:
                key, value = map(str.strip, line.split("=", 1))
                shortcuts[key] = value
                continue

            # Handle task definitions (e.g., build(clean):)
            task_match = re.match(r'(private\s+)?(\w+)\((.*?)\):', line)
            if task_match:
                is_private = bool(task_match.group(1))
                task_name = task_match.group(2)
                dependencies = [dep.strip() for dep in task_match.group(3).split(",") if dep.strip()]
                current_task = Task(task_name, dependencies, is_private=is_private)
                tasks[task_name] = current_task
                continue

            # Handle task actions
            if current_task and line:
                current_task.actions.append(line)

    return tasks, shortcuts


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python build.py <buildfile> <task>")
        sys.exit(1)

    build_file_path = sys.argv[1]
    task_name = sys.argv[2]

    tasks, shortcuts = parse_build_file(build_file_path)
    build_system = BuildSystem(tasks, shortcuts)
    build_system.run_task(task_name)
