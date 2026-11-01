"""Process lifetime lock, independent of Tkinter and training rules."""

from contextlib import contextmanager, suppress
import errno
import os
from pathlib import Path

from logic.exercise_library import library_dir


@contextmanager
def single_instance(path: Path | None = None):
    """Yield whether this process owns the per-user KLAVA lock.

    The OS releases the lock on close or process death. The persistent file must
    never be unlinked: replacing it could let two processes lock different files.
    Windows locks one byte (including beyond EOF); POSIX locks the whole file.
    Unexpected filesystem/locking errors propagate instead of starting unlocked.
    """
    path = path if path is not None else library_dir() / "instance.lock"
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_RDWR | os.O_CREAT, 0o600)
    with os.fdopen(fd, "r+b") as lock:
        try:
            if os.name == "nt":
                import msvcrt

                msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl

                fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            if exc.errno not in (errno.EACCES, errno.EAGAIN, errno.EDEADLK):
                raise
            acquired = False
        else:
            acquired = True
        try:
            yield acquired
        finally:
            # POSIX releases flock on close. Windows also does, but only "eventually"
            # (LockFile docs), so unlock explicitly to allow an immediate relaunch.
            if acquired and os.name == "nt":
                import msvcrt

                # Closing still releases the lock if this fails; never mask the
                # original exception from the application with an unlock error.
                with suppress(OSError):
                    lock.seek(0)
                    msvcrt.locking(lock.fileno(), msvcrt.LK_UNLCK, 1)
