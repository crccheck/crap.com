from __future__ import print_function

import urlparse

from invoke import run, task


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
def create():
    """Create all postgres tables."""
    from craptobuy.config import DATABASE

    # create database
    run(pg_command('createdb', DATABASE), echo=True)

    # turn on HSTORE cuz i don't have a template
    run('echo "CREATE EXTENSION hstore;" | ' + pg_command('psql', DATABASE), echo=True)

    # make some models. ugh.
    from craptobuy import models
    models.User.create_table()
    models.Comparison.create_table()
    models.Item.create_table()


@task
def drop():
    """Drop all tables."""
    from craptobuy.config import DATABASE

    # drop database, don't bother destroying tables
    run(pg_command('dropdb', DATABASE), echo=True)


@task(pre=['db.drop', 'db.create'])
def reset():
    """Re-create all tables, destroying any existing data."""
    pass


@task
def shell():
    """Shell into the database."""
    from craptobuy.config import DATABASE

    run(pg_command('psql', DATABASE), echo=True, pty=True)
