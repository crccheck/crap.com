from invoke import Collection

from . import db, repl, test


ns = Collection()
ns.add_collection(db)
ns.add_collection(repl)
ns.add_collection(test)
