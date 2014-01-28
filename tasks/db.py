from __future__ import print_function

import urlparse

from invoke import run, task


# register schemes
urlparse.uses_netloc.append('postgres')
urlparse.uses_netloc.append('postgresql')
urlparse.uses_netloc.append('postgis')


def connect_bits(url):
    bits = []
    url = urlparse.urlparse(url)
    if url.username:
        bits.extend(['-U', url.username])
    if url.password:
        # TODO
        pass
    if url.hostname:
        bits.extend(['-h', url.hostname])
    if url.port:
        bits.extend(['-p', url.port])
    path = url.path[1:]  # strip leading slash
    return bits, path


@task
def create_all():
    """Create all postgres tables."""
    from crapforsale import app, db
    # import to load models
    from crapforsale import models

    # create database
    args, path = connect_bits(app.config['SQLALCHEMY_DATABASE_URI'])
    bits = ['createdb'] + args
    command = ' '.join(bits)
    run('{} {}'.format(command, path))

    db.create_all()


@task
def drop_all():
    """Drop all tables."""
    from crapforsale import app
    # import to load models
    # from crapforsale import models
    # db.drop_all()

    # drop database, don't bother destroying tables
    args, path = connect_bits(app.config['SQLALCHEMY_DATABASE_URI'])
    bits = ['dropdb'] + args
    command = ' '.join(bits)
    run('{} {}'.format(command, path))


@task(pre=['db.drop_all', 'db.create_all'])
def reset():
    """Re-create all tables, destroying any existing data."""
    pass


@task
def shell():
    """Shell into the database."""
    from crapforsale import app
    args, path = connect_bits(app.config['SQLALCHEMY_DATABASE_URI'])
    bits = ['psql'] + args
    command = ' '.join(bits)
    run('{} {}'.format(command, path), pty=True)
