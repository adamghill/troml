import typer

from troml.commands.check import app as check_app
from troml.commands.hypothesize import app as hypothesize_app
from troml.commands.matrix import app as matrix_app
from troml.commands.suggest import app as suggest_app

app = typer.Typer()

app.add_typer(check_app)
app.add_typer(suggest_app)
app.add_typer(hypothesize_app)
app.add_typer(matrix_app)


if __name__ == "__main__":
    app()
