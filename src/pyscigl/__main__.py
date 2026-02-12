import typer
from .dot_product import run as run_dot
from .learning import run as run_learning

app = typer.Typer(help="The PySciGL CLI")

@app.command()
def dot() -> None:
    """Run the dot product demo."""
    run_dot()

@app.command()
def learning() -> None:
    """Run the dot product demo."""
    run_learning()


@app.command()
def hello(name: str, age: int = 2) -> None:
    """Say hello world"""
    print(f"Hello World {name}, {age}")

if __name__ == "__main__":
    app()
