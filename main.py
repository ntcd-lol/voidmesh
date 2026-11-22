# VoidMesh Prototype. Version: Alpha 0.0.1.0+indev. License: MIT. By ntcd_lol :3

import textwrap
import rich
import argparse
from rich_argparse import RawDescriptionRichHelpFormatter
from pathlib import Path
from flask import Flask
import sqlite3
import chess

ChessEngineWeb: Flask = Flask("VoidMesh")
_script_dir = Path(__file__).resolve().parent

# Aliases
web = ChessEngineWeb
Page = str

class CachedFolder:
    def __init__(self, path: Path):
        self._path = path
        self._files = {}
        for item in path.iterdir():
            name = item.stem.replace("-", "_")
            if item.is_dir():
                self.__dict__[name] = CachedFolder(item)
            elif item.is_file():
                self._files[name] = item

    def __getattr__(self, name: str):
        if name in self._files:
            content = self._files[name].read_text(encoding="utf-8")

            self.__dict__[name] = content
            return content

        raise AttributeError(f"File or dir '{name}' not found in {self._path}")

class PagesRender:
    def __init__(self, pages: Path, static: Path):
        self._pages_dir: Path = pages
        self._stc_dir: Path = static
        self.pages = CachedFolder(self._pages_dir)
        self.static = CachedFolder(self._stc_dir)

@web.route('/')
def root() -> Page:
    return "<h1>Hello, World!</h1>"

def start(web: Flask, pages: Path, static: Path) -> None:
    _page_ren = PagesRender(pages, static)
    web.config["STARTED"] = True

def main() -> int:
    web.run()
    return 0

if __name__ == "__main__":
    RawDescriptionRichHelpFormatter.styles["argparse.prog"] = "bold white"       # Имя программы
    RawDescriptionRichHelpFormatter.styles["argparse.groups"] = "bold yellow"    # Заголовки секций (options:)
    RawDescriptionRichHelpFormatter.styles["argparse.args"] = "underline bold red"        # Флаги (-h, --help)
    RawDescriptionRichHelpFormatter.styles["argparse.metavar"] = "italic bright_black"# Параметры (FILE, NUMBER)
    RawDescriptionRichHelpFormatter.styles["argparse.help"] = "white"            # Текст описания
    RawDescriptionRichHelpFormatter.styles["argparse.default"] = "dim italic"    # Значения по умолчанию


    parser = argparse.ArgumentParser(
        prog="VoidMesh - Prototype 0.0.1.0+indev.",
        description=textwrap.dedent("""\
            [yellow bold]VoidMesh[/yellow bold] - The chess engine, that created from 0, with a high level of customization.
            Creator - [bold]ntcd_lol[/bold] [italic](GitHub: [link=https://github.com/ntcd-lol]ntcd_lol[/link], Telegram: [link=https://t.me/NTheCuteDrone]NTheCuteDrone[/link])[/italic].

            [yellow]│[/yellow] [italic bold red]Changes:[/]
            [yellow]│[/yellow] Now in development. You're still on Prototype.

            GitHub: [link=https://github.com/ntcd-lol/voidmesh]https://github.com/ntcd-lol/voidmesh[/link]
        """),
        formatter_class=RawDescriptionRichHelpFormatter,
        add_help=False
    )
    parser.add_argument("-h", "--help", action="help", default=argparse.SUPPRESS, help="This help page.")
    parser.add_argument("-c", "--config", type=str, default=f"{_script_dir}config.toml", help="Config of VoidMesh.") # пошел нахуй ваня с требованием создания мессенджера anix. - ntcd_prime.
    parser.add_argument("-H", "--home", type=str, default=_script_dir, help="Home directory of VoidMesh.")
    parser.add_argument("-P", "--pagdir", type=str, default=f"{_script_dir}pages/", help="Directory of pages VoidMesh.")
    parser.add_argument("-S", "--stcdir", type=str, default=f"{_script_dir}static/", help="Directory of static VoidMesh.")

    args = parser.parse_args()
    home = args.home
    pages = Path(args.pagdir)
    static = Path(args.stcdir)
    main()
