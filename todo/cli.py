"""Command-line interface for todo-cli."""

from __future__ import annotations

import argparse
import sys

from . import __version__
from .core import TodoList


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="todo", description="A tiny command-line todo manager.")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="add a task")
    p_add.add_argument("text", nargs="+", help="task description")

    p_list = sub.add_parser("list", help="list tasks")
    p_list.add_argument("-a", "--all", action="store_true", help="include completed tasks")

    p_done = sub.add_parser("done", help="mark a task as done")
    p_done.add_argument("id", type=int)

    p_rm = sub.add_parser("rm", help="remove a task")
    p_rm.add_argument("id", type=int)

    sub.add_parser("clear", help="remove all completed tasks")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        todos = TodoList()
        if args.command == "add":
            task = todos.add(" ".join(args.text))
            print(f"Added #{task.id}: {task.text}")
        elif args.command == "list":
            tasks = todos.list(show_done=args.all)
            if not tasks:
                print("Nothing to do. 🎉")
            for t in tasks:
                mark = "x" if t.done else " "
                print(f"[{mark}] {t.id:>3}  {t.text}")
        elif args.command == "done":
            task = todos.complete(args.id)
            print(f"Completed #{task.id}: {task.text}")
        elif args.command == "rm":
            task = todos.remove(args.id)
            print(f"Removed #{task.id}: {task.text}")
        elif args.command == "clear":
            print(f"Cleared {todos.clear_done()} completed task(s).")
    except (KeyError, ValueError) as exc:
        message = exc.args[0] if exc.args else str(exc)
        print(f"error: {message}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
