import typer

from ser import cbb

app = typer.Typer()

app.add_typer(cbb.app, name="cbb")

app()
