from invoke import run, task


@task
def build(default=True):
    run('sass --watch craptobuy/static/sass:craptobuy/static/css')


@task
def watch():
    run('sass --compass --watch craptobuy/static/sass:craptobuy/static/css')
