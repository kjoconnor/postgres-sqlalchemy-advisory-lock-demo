import time

from multiprocessing import Process

from advisory_locks import AdvisoryLock, AdvisoryLockUnavailable, key_fn


def get_lock(user_id, state):
    try:
        with AdvisoryLock(key_fn(user_id, state)):
            print("I've acquired the lock, sleeping for 3 seconds to simulate working")
            time.sleep(3)
            print("I'm done - I should be releasing the lock now")
    except AdvisoryLockUnavailable:
        print("I could not get the lock!")


if __name__ == "__main__":
    # This will first acquire the lock, then sleep
    # While the lock holder is sleeping, we start another process and try to
    # acquire the lock, which will fail (by throwing the `AdvisoryLockUnavailable` exception)
    # Then once the first process is done (the time.sleep() has passed), another
    # process can get the lock and do its work.
    successful_lock_holder = Process(target=get_lock, args=("123", "in-progress"))
    failed_lock_holder = Process(target=get_lock, args=("123", "in-progress"))

    successful_lock_holder.start()
    failed_lock_holder.start()

    successful_lock_holder.join()
    failed_lock_holder.join()

    latecomer_lock_holder = successful_lock_holder = Process(
        target=get_lock, args=("123", "in-progress")
    )
    latecomer_lock_holder.start()
    latecomer_lock_holder.join()
