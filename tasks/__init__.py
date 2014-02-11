from invoke import Collection

from . import amazon, db, repl, sass, test


ns = Collection()
ns.add_collection(amazon)
ns.add_collection(db)
ns.add_collection(repl)
ns.add_collection(sass)
ns.add_collection(test)
