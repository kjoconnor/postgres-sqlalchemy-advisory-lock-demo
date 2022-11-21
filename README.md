# advisory locks demo

Just a simple app to show how you might use advisory locks in a context manager.

## Running

You'll have to have a Postgres running somewhere. This doesn't store any data but still
needs the server available. You can change the DSN in `advisory_locks.py`.

```shell
virtualenv .ve
. .ve/bin/activate
python test_advisory_locks.py
```