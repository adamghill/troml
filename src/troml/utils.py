from collections.abc import Iterable

import typer


def echo_classifiers(title: str, classifiers: Iterable) -> None:
    typer.secho(title, fg=typer.colors.BLUE)

    typer.echo("classifiers = [")

    for classifier in classifiers:
        typer.echo(f'  "{classifier}",')

    typer.echo("]")
