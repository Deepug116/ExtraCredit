class MyDBError(Exception):
    pass

class InMemoryDB:
    def __init__(self):
        self.data = {}
        self.pending = None

    def begin_transaction(self):
        if self.pending is not None:
            raise MyDBError("Transaction already running")
        self.pending = {}

    def put(self, key, value):
        if self.pending is None:
            raise MyDBError("No active transaction")
        self.pending[key] = value

    def get(self, key):
        return self.data.get(key)

    def commit(self):
        if self.pending is None:
            raise MyDBError("Nothing to commit")
        self.data.update(self.pending)
        self.pending = None

    def rollback(self):
        if self.pending is None:
            raise MyDBError("Nothing to rollback")
        self.pending = None

# testing purposes

if __name__ == "__main__":
    db = InMemoryDB()
    print(db.get("A"))
    try:
        db.put("A", 5)
    except MyDBError as e:
        print(e)
    db.begin_transaction()
    db.put("A", 5)
    print(db.get("A"))
    db.put("A", 6)
    db.commit()
    print(db.get("A"))
    for action in (db.commit, db.rollback):
        try:
            action()
        except MyDBError as e:
            print(e)
    print(db.get("B"))
    db.begin_transaction()
    db.put("B", 10)
    db.rollback()
    print(db.get("B"))
