from {{ cookiecutter.project_name}}.{{ cookiecutter.main_file}} import run

__version__ = "0.0.1"


def main():
    run()


if __name__ == "__main__":
    main()
