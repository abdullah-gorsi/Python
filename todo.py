# Beginner To-Do List App

tasks = []

while True:
    print("\n===== TO-DO LIST APP =====")
    print("1. Add a task")
    print("2. View tasks")
    print("3. Delete a task")
    print("4. Exit")

    choice = input("Enter your choice (1-4): ")

    # Add a task
    if choice == "1":
        task = input("Enter your task: ").strip()

        if task:
            tasks.append(task)
            print("Task added successfully!")
        else:
            print("Task cannot be empty.")

    # View all tasks
    elif choice == "2":
        print("\nYour Tasks:")

        if not tasks:
            print("No tasks available.")
        else:
            for i, task in enumerate(tasks, start=1):
                print(f"{i}. {task}")

    # Delete a task
    elif choice == "3":
        if not tasks:
            print("There are no tasks to delete.")
        else:
            for i, task in enumerate(tasks, start=1):
                print(f"{i}. {task}")

            try:
                number = int(input("Enter task number to delete: "))

                if 1 <= number <= len(tasks):
                    removed_task = tasks.pop(number - 1)
                    print(f"Deleted: {removed_task}")
                else:
                    print("Invalid task number.")

            except ValueError:
                print("Please enter a valid number.")

    # Exit the app
    elif choice == "4":
        print("Thank you for using the To-Do List App!")
        break

    else:
        print("Invalid choice. Please select 1-4.")
