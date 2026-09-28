""" This Module Provides The To-Do Cli  """

# todo/cli.py

from typing import List, Optional
from pathlib import Path
import typer
from todo import __version__ , __app_name__ , ERRORS, config, database , todo

app = typer.Typer()

@app.command()
def init(
    db_path: str = typer.Option(
        str(database.DEFULT_DB_FILE_PATH),
        "--db-path",
        "-d",
        prompt="Path to the database file",
    ),
) -> None :
    app_init_error = config.init_app(db_path)
    if app_init_error :
        typer.secho(
            f"Creating congiguration file failed '{ERRORS[app_init_error]}'",
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    db_init_error = database.init_database(Path(db_path))
    if db_init_error :
        typer.secho(
            f"Creating database file failed '{ERRORS[db_init_error]}'",
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else :
        typer.secho(
            f"Application initialized successfully at '{db_path}'",
            fg=typer.colors.GREEN
        )

def get_todoer() -> todo.Todoer:
    """ Get the Todoer instance """
    if config.CONFIG_PATH.exists() :
        db_path = database.get_database_path(config.CONFIG_PATH)
    else :
        typer.secho(
            "Configuration file not found. Please run 'todo init' first.",
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    if db_path.exists() :
        todoer = todo.Todoer(db_path)
        return todoer
    else :
        typer.secho(
            "Database file not found. Please run 'todo init' first.",
            fg=typer.colors.RED
        )
        raise typer.Exit(1)

@app.command()
def add(
    description: List[str] = typer.Argument(..., help="Description of the todo item"),
    priority: int = typer.Option(2, "--priority", "-p", help="Priority of the todo item (1-3)" , min=1 , max=3),
) -> None:
    """ Add a new todo item """
    todoer = get_todoer()
    todo , error = todoer.add(description, priority)
    if error :
        typer.secho(
            f"Adding todo item failed '{ERRORS[error]}'",
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else :
        typer.secho(
            f"Todo : {todo['Description']} with priority {todo['Priority']} added successfully.",
            fg=typer.colors.GREEN
        )


@app.command('list')
def list_all() -> None:
    """ List all todo items """
    todoer = get_todoer()
    todo_list = todoer.get_todos_list()
    if len(todo_list) == 0:
        typer.secho(
            "No todo items found.",
            fg=typer.colors.YELLOW
        )
        raise typer.Exit(0)
    typer.secho(
        "\nTodo List:\n",
        fg=typer.colors.BLUE,
        bold=True
    )
    columns = (
        "ID.",
        "| Priority",
        "| Done ",
        "| Description",
    )
    headers = " ".join(columns)
    typer.secho(
        headers,
        fg=typer.colors.BLUE,
        bold=True
    )
    typer.secho(
        "-" * len(headers),
        fg=typer.colors.BLUE,
    )
    for id , todo in enumerate(todo_list, start=1):
        desc , priority , done = todo.values()
        typer.secho(
            f"{id}.  |    {priority}     | {done} | {desc}",
            fg=typer.colors.BLUE,
        )
    typer.secho(
        "-" * len(headers) + "\n",
        fg=typer.colors.BLUE,
    )

@app.command(name="complete")
def set_done(
    todo_id: int = typer.Argument(..., )) -> None:
    """ Mark a todo item as done """
    todoer = get_todoer()
    todo , error = todoer.set_done(todo_id)
    if error :
        typer.secho(
            f"Setting todo item as done failed '{ERRORS[error]}'",
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else :
        typer.secho(
            f"""Todo # {todo_id} "{todo['Description']}" completed.""",
            fg=typer.colors.GREEN
        )

@app.command()
def remove(
    todo_id: int = typer.Argument(..., ),
    force: bool = typer.Option(False, "--force", "-f", help="Force removal without confirmation"),
    ) -> None:
    """ Remove a todo item """
    todoer = get_todoer()
    def _remove():
        todo , error = todoer.remove(todo_id)
        if error :
            typer.secho(
                f"Removing todo #{todo_id} failed '{ERRORS[error]}'",
                fg=typer.colors.RED
            )
            raise typer.Exit(1)
        else :
            typer.secho(
                f"""Todo # {todo_id} "{todo['Description']}" removed.""",
                fg=typer.colors.GREEN
            )
    if force:
        _remove()
    else:
        todo_list = todoer.get_todos_list()
        try:
            todo = todo_list[todo_id - 1]
        except IndexError:
            typer.secho(
                f"Todo #{todo_id} not found.",
                fg=typer.colors.RED
            )
            raise typer.Exit(1)
        delete = typer.confirm(
            f"Are you sure you want to delete todo #{todo_id} '{todo['Description']}'?")
        if delete:
            _remove()
        else:
            typer.secho(
                f"Todo #{todo_id} '{todo['Description']}' not removed.",
                fg=typer.colors.YELLOW
            )

@app.command(name='clear')
def remoove_all(
    force : bool = typer.Option(
        ...,
        prompt= 'are you sure that you want to clear all todos?',
        help= 'Force remove all tasks without confimation',
    ),
) -> None :
    """ Remove all tasks from the to-do list. """
    todoer = get_todoer()
    if force :
        error = todoer.remove_all().error
        if error :
            typer.secho(
                f"removing all tasks failed with '{ERRORS[error]}'",
                fg= typer.colors.RED,
            )
            raise typer.Exit(1)
        else :
            typer.secho("All tasks removed" , fg= typer.colors.GREEN)
    else :
        typer.secho(
            "Operation Canceled" ,
            fg= typer.colors.YELLOW,
        )


def __version_callback(value : bool) -> None:
    """ Print the version of the application and exit """
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()

@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        is_eager=True,
        callback=__version_callback,
    )
    ) -> None:
    """ A Simple To-Do Application """
    return