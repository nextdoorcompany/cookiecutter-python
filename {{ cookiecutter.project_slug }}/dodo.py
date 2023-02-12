import re
import subprocess
from pathlib import Path

from {{ cookiecutter.project_name }}.__main__ import __version__

DOIT_CONFIG = {
    "default_tasks": [
        "isort",
        "black",
        "lint",
        "flake8",
        "test",
        "ruff",
        "coverage_with_fail_under",
        "vulture",
    ],
    "continue": True,
    "num_process": 4,
    "par_type": "thread",
}


cwd = Path(".")
test_files = list((cwd / "tests").glob("test*.py"))
python_files = (
    list(cwd.glob("*.py")) + list((cwd / "{{ cookiecutter.project_name }}").glob("*.py")) + test_files
)


def task_flake8():
    for f in python_files:
        yield {
            "name": f.name,
            "actions": [
                [
                    "env/{{ cookiecutter.scripts_or_bin }}/python",
                    "-m",
                    "flake8",
                    "--max-complexity",
                    "7",
                    f,
                ]
            ],
            "file_dep": [f],
        }


def task_lint():
    for f in python_files:
        yield {
            "name": f.name,
            "actions": [
                [
                    "env/{{ cookiecutter.scripts_or_bin }}/python",
                    "-m",
                    "pylint",
                    "--output-format=parseable",
                    "--rcfile",
                    "pyproject.toml",
                    f,
                ]
            ],
            "file_dep": [f],
        }


def task_test():
    for f in test_files:
        yield {
            "name": f.name,
            "actions": [["env/{{ cookiecutter.scripts_or_bin }}/python", "-m", "pytest", f]],
            "file_dep": [f],
        }


def task_isort():
    for f in python_files:
        yield {
            "name": f.name,
            "actions": [
                [
                    "env/{{ cookiecutter.scripts_or_bin }}/python",
                    "-m",
                    "isort",
                    "--profile",
                    "black",
                    "--check",
                    f,
                ]
            ],
            "file_dep": [f],
        }


def task_black():
    for f in python_files:
        yield {
            "name": f.name,
            "actions": [
                [
                    "env/{{ cookiecutter.scripts_or_bin }}/python",
                    "-m",
                    "black",
                    "--check",
                    "--quiet",
                    f,
                ]
            ],
            "file_dep": [f],
        }


def task_coverage():
    return {
        "actions": [
            ["env/{{ cookiecutter.scripts_or_bin }}/coverage", "run", "--source={{ cookiecutter.project_name }}", "-m", "pytest", "tests"],
            ["env/{{ cookiecutter.scripts_or_bin }}/coverage", "report"],
        ],
        "uptodate": [False],
        "verbosity": 2,
    }


def task_coverage_with_fail_under():
    return {
        "actions": [
            ["env/{{ cookiecutter.scripts_or_bin }}/coverage", "run", "--source={{ cookiecutter.project_name }}", "-m", "pytest", "tests"],
            ["env/{{ cookiecutter.scripts_or_bin }}/coverage", "report"],
        ],
        "uptodate": [False],
    }


def task_vulture():
    return {
        "actions": [
            ["env/{{ cookiecutter.scripts_or_bin }}/vulture", "{{ cookiecutter.project_name }}"],
        ],
        "uptodate": [False],
    }


def task_build():
    def python_build():
        build_folder = Path("build")
        if not build_folder.exists():
            build_folder.mkdir()
        subprocess.call(
            [
                "env/{{ cookiecutter.scripts_or_bin }}/python",
                "-m",
                "pip",
                "wheel",
                "--wheel-dir",
                "build",
                "--no-deps",
                ".",
            ]
        )
        return True

    return {"actions": [python_build]}


def task_upgrade_deps():
    def python_upgrade_deps():
        subprocess.call(
            [
                "env/{{ cookiecutter.scripts_or_bin }}/python",
                "-m",
                "pip",
                "install",
                "-r",
                "requirements-bootstrap.txt",
                "-U",
            ]
        )
        subprocess.call(
            [
                "env/{{ cookiecutter.scripts_or_bin }}/pip-compile",
                "--quiet",
                "--upgrade",
                "--output-file",
                "requirements.txt",
                "--generate-hashes",
                "--resolver",
                "backtracking",
                "pyproject.toml",
            ]
        )
        subprocess.call(
            [
                "env/{{ cookiecutter.scripts_or_bin }}/pip-compile",
                "--quiet",
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
        subprocess.call(
            [
                "env/{{ cookiecutter.scripts_or_bin }}/pip-sync",
                "requirements.txt",
                "requirements-dev.txt",
            ]
        )
        return True

    return {"actions": [python_upgrade_deps]}


SEMVER = """MAJOR version when you make incompatible API changes
MINOR version when you add functionality in a backwards compatible manner
PATCH version when you make backwards compatible bug fixes"""


def task_tbump():
    def run_tbump():
        print(SEMVER)  # noqa: T201
        print(f"Current: {__version__}")  # noqa: T201
        pattern = r"(?P<major>\d+).(?P<minor>\d+).(?P<patch>\d+)"
        m = re.fullmatch(pattern, __version__)
        if m:
            patch = int(m.group("patch"))
            new_patch = patch + 1
            candidate = f"{m.group('major')}.{m.group('minor')}.{new_patch}"
        else:
            candidate = "???"
        new_version = input(f"Enter new version [{candidate}]: ")
        if not new_version:
            new_version = candidate
        t = subprocess.run(
            [
                r"env/{{ cookiecutter.scripts_or_bin }}/tbump",
                "--non-interactive",
                "--no-push",
                new_version,
            ],
            capture_output=True,
            check=False,
            text=True,
        )
        print(t.stdout, t.stderr)  # noqa: T201

    return {"actions": [run_tbump], "uptodate": [False], "verbosity": 2}


def task_ruff():
    for f in python_files:
        yield {
            "name": f.name,
            "actions": [
                [
                    r"env/{{ cookiecutter.scripts_or_bin }}/ruff",
                    f,
                ]
            ],
            "file_dep": [f],
        }
