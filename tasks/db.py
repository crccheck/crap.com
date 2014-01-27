from invoke import task, Collection


@task
def create_all():
    """Create all tables."""
    from crapforsale import db
    # import to load models
    from crapforsale import models
    db.create_all()


@task
def drop_all():
    """Drop all tables."""
    from crapforsale import db
    # import to load models
    from crapforsale import models
    db.drop_all()


@task(pre=['db.drop_all', 'db.create_all'])
def reset():
    """Re-create all tables, destroying any existing data."""
    pass
