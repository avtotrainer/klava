"""Process lifetime lock, independent of Tkinter and training rules."""

from contextlib import contextmanager
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
        # Closing the descriptor releases only our lock, including on exceptions.
        yield acquired
