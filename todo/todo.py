#todo/todo.py

from pathlib import Path
from typing import Any , NamedTuple , Dict , List
from todo.database import DatabaseHandler
from todo import DB_READ_ERROR , ID_ERROR

class CurrentTodo(NamedTuple):
    """ A Named Tuple to represent the current todo item """
    todo : Dict[str , Any]
    error : int

class Todoer :
    def __init__(self, db_path: Path) -> None:
        self.db_handler = DatabaseHandler(db_path)

    def add (self, description: List[str], priority: int = 2) -> CurrentTodo :
        """ Add a new todo item to the database """
        description_text = ' '.join(description)
        if not description_text.endswith('.'):
            description_text += '.'
        todo = {
            "Description": description_text,
            "Priority": priority,
            "Done": False
        }
        read = self.db_handler.read_todos()
        if read.error == DB_READ_ERROR:
            return CurrentTodo(todo, read.error)
        read.todo_list.append(todo)
        write = self.db_handler.write_todos(read.todo_list)
        return CurrentTodo(todo, write.error)

    def get_todos_list(self) -> CurrentTodo :
        """ Get the list of todo items from the database """
        read = self.db_handler.read_todos()
        if read.error == DB_READ_ERROR:
            return []
        return read.todo_list

    def set_done(self, todo_id: int) -> CurrentTodo :
        """ Set a todo item as done """
        read = self.db_handler.read_todos()
        if read.error:
            return CurrentTodo({}, read.error)
        try :
            todo = read.todo_list[todo_id - 1]
        except IndexError :
            return CurrentTodo({}, ID_ERROR)
        todo["Done"] = True
        write = self.db_handler.write_todos(read.todo_list)
        return CurrentTodo(todo, write.error)

    def remove(self, todo_id: int) -> CurrentTodo :
        """ Remove a todo item from the database """
        read = self.db_handler.read_todos()
        if read.error:
            return CurrentTodo({}, read.error)
        try :
            todo = read.todo_list[todo_id - 1]
        except IndexError :
            return CurrentTodo({}, ID_ERROR)
        read.todo_list.remove(todo)
        write = self.db_handler.write_todos(read.todo_list)
        return CurrentTodo(todo, write.error)

    def remove_all(self) -> None :
        """" Remove All Todos """
        write = self.db_handler.write_todos([])
        return CurrentTodo({} , write.error)