from invoke import task, run


@task(default=True)
def test():
    # yeah, I could just `import nose` but then I'd have to mess with path
    run('ENVIRONMENT=test nosetests')
