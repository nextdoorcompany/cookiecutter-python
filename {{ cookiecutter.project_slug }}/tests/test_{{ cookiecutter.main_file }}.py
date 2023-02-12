import {{ cookiecutter.project_name}}.{{ cookiecutter.main_file }} as f


def test_func():
    result = f.func()

    two = 2
    assert result == two
