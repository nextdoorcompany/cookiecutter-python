import subprocess

subprocess.run(["{{cookiecutter.python_exe}}", "-m", "venv", "env"])

subprocess.run(
    [
        "env/{{cookiecutter.scripts_or_bin}}/python",
        "-m",
        "pip",
        "install",
        "-r",
        "requirements-bootstrap.txt",
        "-U",
    ]
)

subprocess.run(
    [
        "env/{{cookiecutter.scripts_or_bin}}/pip-compile",
        "--upgrade",
        "--extra",
        "dev",
        "--output-file",
        "requirements-dev.txt",
        "--generate-hashes",
        "--resolver",
        "backtracking",
        "pyproject.toml",
    ]
)

subprocess.run(
    [
        "env/{{cookiecutter.scripts_or_bin}}/pip-sync",
        "requirements-dev.txt",
    ]
)

subprocess.run(
    [
        "git",
        "init",
        "-b",
        "trunk",
    ]
)

subprocess.run(
    [
        "env/{{cookiecutter.scripts_or_bin}}/black",
        "-v",
        "tests/",
        "{{ cookiecutter.project_name }}",
        "dodo.py",
    ]
)

subprocess.run(
    [
        "cat",
        "readme.org",
    ]
)
