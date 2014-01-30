from invoke import run, task


@task(default=True)
def repl():
    """Open an ipython session with all the models preloaded."""
    # for some reason, invoke.run craps out on sending quoted text
    run("ipython -i -c 'from crapforsale.models import *'", pty=True)
