from invoke import run, task


@task(default=True)
def repl():
    """Open an ipython session with all the models preloaded."""
    run("ipython -i -c 'from craptobuy.models import *'", pty=True)
