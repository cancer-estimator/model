import typer

from cancer_estimator_model import models

app = typer.Typer()


@app.command()
def train():
    """
    Train model and save artifacts
    """
    model = models.train()
    models.save(model)


if __name__ == "__main__":
    app()
