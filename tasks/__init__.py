from invoke import Collection

from . import db, repl, sass, test


ns = Collection()
ns.add_collection(db)
ns.add_collection(repl)
ns.add_collection(sass)
ns.add_collection(test)
