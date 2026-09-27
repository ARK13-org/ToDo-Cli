""" To-Do entry point for the application """

# todo/__main__.py
from todo import cli , __app_name__

def main() :
    """main entry point for the application"""
    cli.app(prog_name=__app_name__)

if __name__ == "__main__":
    main()