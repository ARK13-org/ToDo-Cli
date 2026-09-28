#test/todo_test.py

import json
import pytest
from typer.testing import CliRunner
from todo import cli , __app_name__ , __version__ , SUCCESS , DB_READ_ERROR , todo

runner = CliRunner()

@pytest.fixture
def mock_json_file(tmp_path):
    """ Create a mock JSON file for testing """
    todo = [
        {
            "Description": "Get Some Milk",
            "Priority": 2,
            "Done": False
        },
    ]
    db_file = tmp_path / "test_todo.json"
    with db_file.open('w') as db:
        json.dump(todo, db , indent=4)
    return db_file

test_data1 = [
    {
        "description": ['Clean' , 'The' , 'House'],
        "priority": 1,
        "todo": {
            "Description": "Clean The House",
            "Priority": 1,
            "Done": False
        }
    },
]

test_data2 = [
    {
        "description": ['Whash The Car'],
        "priority": 2,
        "todo": {
            "Description": "Whash The Car",
            "Priority": 2,
            "Done": False
        }
    },
]

@pytest.mark.parametrize(
    "description, priority, expected_todo",
    [
        pytest.param(test_data1["description"], test_data1["priority"], (test_data1["todo"], SUCCESS)),
        pytest.param(test_data2["description"], test_data2["priority"], (test_data2["todo"], SUCCESS)),
    ]
)

def test_add(description, priority, expected_todo, mock_json_file):
    """ Test the add command """
    todoer = todo.Todoer(mock_json_file)
    assert todoer.add(description, priority) == expected_todo
    read = todoer.db_handler.read_todos()
    assert len(read.todo_list) == 2

def test_version() -> None:
    """ Test the version of the application """
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}" in result.stdout