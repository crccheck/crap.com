from invoke import Collection

from . import db


ns = Collection()
ns.add_collection(db)
