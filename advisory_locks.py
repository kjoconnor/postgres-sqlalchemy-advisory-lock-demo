import hashlib

from sqlalchemy import func, select

# For your flask app you'd just import this instead of this `db` class down below
# from app import db


class db(object):
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session

    engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost:6543")
    session = Session(engine)


def key_fn(user_id, state):
    key_str = f"{user_id}-{state}"
    # advisory lock keys can either be one 128 bit integer, or two 64 bit integers
    # there might be a nicer way to do this, but it doesn't need to be
    # super secure, just unique enough!
    return str(int(hashlib.md5(key_str.encode("utf-8")).hexdigest()[:16], 16))


class AdvisoryLockUnavailable(Exception):
    pass


class AdvisoryLock(object):
    def __init__(self, key):
        self._key = key

    def __enter__(self):
        lock_acquired = db.session.execute(
            select(func.pg_try_advisory_lock(self._key))
        ).scalar()
        if not lock_acquired:
            raise AdvisoryLockUnavailable

    def __exit__(self, exc_type, exc, exc_tb):
        return db.session.execute(select(func.pg_advisory_unlock(self._key))).scalar()


if __name__ == "__main__":
    with AdvisoryLock(key_fn("123", "in-progress")):
        print("I have the lock!")
