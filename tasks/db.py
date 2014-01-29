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
        bits.extend(['-p', db['port']])
    return bits


def pg_command(command, meta):
    args = connect_bits(meta)
    bits = [command] + args
    command = ' '.join(bits)
    return '{} {}'.format(command, meta['database'])


@task
def create():
    """Create all postgres tables."""
    from crapforsale.config import DATABASE

    # create database
    run(pg_command('createdb', DATABASE), echo=True)

    # make some models. ugh.
    from crapforsale import models
    thingy = [x for x in dir(models) if x [0] != '_']
    thingy.remove('BaseModel')
    for maybe in thingy:
        hopefully = getattr(models, maybe)
        try:
            if issubclass(hopefully, models.BaseModel):
                hopefully.create_table()
        except TypeError:
            pass


@task
def drop():
    """Drop all tables."""
    from crapforsale.config import DATABASE

    # drop database, don't bother destroying tables
    run(pg_command('dropdb', DATABASE), echo=True)


@task(pre=['db.drop', 'db.create'])
def reset():
    """Re-create all tables, destroying any existing data."""
    pass


@task
def shell():
    """Shell into the database."""
    from crapforsale.config import DATABASE

    run(pg_command('psql', DATABASE), echo=True, pty=True)
