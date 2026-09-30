# 📝 CLI To-Do App

A modular **command-line task manager** built with **Python and Typer**, featuring JSON persistence, configuration management, and automated testing with pytest.

## ✨ Features

* ➕ Add tasks with priorities
* 📋 List tasks in a formatted table
* ✅ Mark tasks as complete
* 🗑️ Remove individual tasks
* 🧹 Clear all tasks
* 💾 Persistent JSON storage
* ⚙️ User-specific configuration
* 🎨 Coloured terminal output
* 🧪 Automated tests with pytest
* 🏷️ Application version command

## 🛠️ Tech Stack

* **Python 3**
* **Typer** — CLI framework
* **JSON** — data persistence
* **pytest** — automated testing
* **pathlib** — cross-platform file handling
* **configparser** — configuration management
* **Type hints** — structured and maintainable code

## 🏗️ Architecture

```text
todo/
├── todo/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   ├── config.py
│   ├── database.py
│   └── todo.py
├── tests/
│   └── test_todo.py
├── requirements.txt
└── README.md
```

The project separates **CLI interaction, business logic, data persistence, and configuration** into independent modules.

## 🚀 Getting Started

### Install dependencies

```bash
pip install -r requirements.txt
```

### Initialize the application

```bash
python -m todo init
```

### Add a task

```bash
python -m todo add "Clean the house" -p 1
```

### List tasks

```bash
python -m todo list
```

### Complete a task

```bash
python -m todo complete 1
```

### Remove a task

```bash
python -m todo remove 1
```

### Run tests

```bash
pytest
```

## 💻 Example

```text
$ python -m todo add "Clean the house" -p 1
Todo : Clean the house. with priority 1 added successfully.

$ python -m todo add "Wash the car" -p 2
Todo : Wash the car. with priority 2 added successfully.

$ python -m todo list

Todo List:

ID. | Priority | Done  | Description
-----------------------------------
1.  |    1     | False | Clean the house.
2.  |    2     | False | Wash the car.
-----------------------------------

$ python -m todo complete 1
Todo # 1 "Clean the house." completed.

$ python -m todo remove 2
Are you sure you want to delete todo #2 'Wash the car.'? [y/N]: y
Todo # 2 "Wash the car." removed.
```

## 🧪 Testing

The project includes automated tests using **pytest** and Typer's **CliRunner**.

Tests cover:

* Adding tasks with different priorities
* Reading persisted data
* CLI version output
* JSON database operations
* Temporary test data using pytest fixtures

Run the test suite with:

```bash
pytest
```

## 🧠 What I Explored

* Building CLI applications with **Typer**
* Designing modular Python packages
* Separating CLI, business, and data layers
* JSON-based data persistence
* Configuration management
* Type hints and structured responses
* Error handling
* Automated testing with **pytest** and **CliRunner**
* Cross-platform file handling with `pathlib`

## 🔮 Future Improvements

* 📅 Due dates and reminders
* 🏷️ Tags and categories
* 🔍 Search and filtering
* 📤 CSV or Markdown export
* 📦 Standalone executable with PyInstaller

---

**Built by ARK13** — a Python project exploring CLI development, modular architecture, persistence, and automated testing.
