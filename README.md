# todo-cli

A tiny command-line todo manager. Zero dependencies, tasks stored in a plain JSON file.

## Install

```bash
git clone https://github.com/silenat/todo-cli.git
cd todo-cli
pip install -e .
```

Or run without installing: `python -m todo --help`

## Usage

```bash
todo add buy milk          # Added #1: buy milk
todo add write README
todo list                  # open tasks only
todo done 1                # mark #1 complete
todo list --all            # include completed tasks
todo rm 2                  # delete a task
todo clear                 # delete all completed tasks
```

Tasks are saved to `~/.todo.json`. Point somewhere else with the `TODO_FILE` environment variable:

```bash
TODO_FILE=./project-todos.json todo list
```

## Development

```bash
pip install -e ".[dev]"
pytest
```

## Project layout

```
todo/
  core.py   # Task + TodoList (storage and logic)
  cli.py    # argparse interface
tests/
  test_todo.py
```

## License

MIT
