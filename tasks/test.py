from invoke import task, run


@task(pre=['test.reset'], default=True)
def test():
    """Run testrunner. Remember to `inv test.resetdb` the first time."""
    # yeah, I could just `import nose` but then I'd have to mess with path
    run('ENVIRONMENT=test nosetests -s', pty=True)


@task
def reset():
    """Reset the persistent test DB."""
    from os import environ

    environ['ENVIRONMENT'] = 'test'
    from .db import drop, create
    drop()
    create()


@task
def resetdb():
    """Re-make the persistent test DB."""
    from os import environ

    environ['ENVIRONMENT'] = 'test'
    from .db import dropdb, createdb
    dropdb()
    createdb()
