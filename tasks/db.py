from __future__ import print_function

import urlparse

from invoke import run, task


MODELS = [
    'Comparison',
    'AmazonProduct',
    'PriceHistory',
    'Item',
]


# register schemes
urlparse.uses_netloc.append('postgresql')


def connect_bits(db):
    assert db['database']  # set your env variables!

    bits = []
    if db['user']:
        bits.extend(['-U', db['user']])
    if db['password']:
        # TODO
        pass
    if db['host']:
        bits.extend(['-h', db['host']])
    if db['port']:
        bits.extend(['-p', str(db['port'])])
    return bits


def pg_command(command, meta):
    args = connect_bits(meta)
    bits = [command] + args
    command = ' '.join(bits)
    return '{} {}'.format(command, meta['database'])


@task
def createdb():
    """Create database."""
    from craptobuy.config import DATABASE

    # create database
    run(pg_command('createdb', DATABASE), echo=True)

    # turn on HSTORE cuz i don't have a template
    run('echo "CREATE EXTENSION hstore;" | ' + pg_command('psql', DATABASE), echo=True)


@task
def create():
    """Create the tables."""
    # make some models. ugh.
    from craptobuy import models
    for model_name in MODELS:
        getattr(models, model_name).create_table()


@task
def drop():
    """Drop all tables."""
    from craptobuy import models
    for model_name in reversed(MODELS):
        # should I cascade=True ?
        getattr(models, model_name).drop_table(fail_silently=True)


@task
def dropdb():
    """Drop database."""
    from craptobuy.config import DATABASE

    # drop database, don't bother destroying tables
    run(pg_command('dropdb', DATABASE), warn=True, echo=True)


@task(pre=['db.drop', 'db.create'])
def reset():
    """Re-create all tables, destroying any existing data."""
    pass


@task
def shell():
    """Shell into the database."""
    from craptobuy.config import DATABASE

    run(pg_command('psql', DATABASE), echo=True, pty=True)
