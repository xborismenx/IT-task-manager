# Task Manager

A Django-based web application for managing tasks and workers. This application includes features for task creation, assignment, updating, and deletion, as well as worker management.

## Features

- User authentication and authorization
- Task creation, updating, and deletion
- Worker creation, updating, and deletion
- Task assignment to workers
- Task categorization by type
- Priority setting for tasks
- Task filtering and sorting
- Pagination for task and worker lists
Installation

1. **Clone the repository:**
    ```sh
    git clone [https://github.com/yourusername/task-manager.git](https://github.com/xborismenx/IT-task-manager.git)
    cd task-manager
    ```

2. **Create and activate a virtual environment:**
    ```sh
    python3 -m venv .venv
    source env/bin/activate
    ```

3. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Apply migrations:**
    ```sh
    python manage.py migrate
    ```

5. **Create a superuser:**
    ```sh
    python manage.py createsuperuser
    ```

6. **Run the development server:**
    ```sh
    python manage.py runserver
    ```
