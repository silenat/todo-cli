import json

import pytest

from todo.cli import main
from todo.core import TodoList


@pytest.fixture
def path(tmp_path):
    return tmp_path / "todo.json"


def test_add_and_persist(path):
    todos = TodoList(path)
    task = todos.add("  buy milk ")
    assert task.id == 1 and task.text == "buy milk"
    assert [t.text for t in TodoList(path).list()] == ["buy milk"]


def test_empty_text_rejected(path):
    with pytest.raises(ValueError):
        TodoList(path).add("   ")


def test_ids_increment_and_stay_unique(path):
    todos = TodoList(path)
    todos.add("a")
    todos.add("b")
    todos.add("c")
    todos.remove(2)
    assert todos.add("d").id == 4
    assert len({t.id for t in todos.list()}) == 3


def test_complete_and_filter(path):
    todos = TodoList(path)
    todos.add("a")
    todos.add("b")
    todos.complete(1)
    assert [t.text for t in todos.list(show_done=False)] == ["b"]
    assert len(todos.list()) == 2


def test_clear_done(path):
    todos = TodoList(path)
    todos.add("a")
    todos.add("b")
    todos.complete(1)
    assert todos.clear_done() == 1
    assert [t.text for t in todos.list()] == ["b"]


def test_missing_id(path):
    with pytest.raises(KeyError):
        TodoList(path).complete(99)


def test_corrupt_file(path):
    path.write_text("{not json")
    with pytest.raises(ValueError):
        TodoList(path)


def test_cli_roundtrip(path, monkeypatch, capsys):
    monkeypatch.setenv("TODO_FILE", str(path))
    assert main(["add", "write", "tests"]) == 0
    assert main(["done", "1"]) == 0
    assert main(["list", "--all"]) == 0
    out = capsys.readouterr().out
    assert "[x]   1  write tests" in out
    assert json.loads(path.read_text())[0]["done"] is True


def test_cli_error_exit_code(path, monkeypatch, capsys):
    monkeypatch.setenv("TODO_FILE", str(path))
    assert main(["done", "5"]) == 1
    assert "No task with id 5" in capsys.readouterr().err
