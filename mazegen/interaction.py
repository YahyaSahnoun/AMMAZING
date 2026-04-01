import os
import sys
import tty
import termios
from typing import Union


def get_key() -> str:
    """
    Reads a single keypress from the terminal and returns it as lowercase.
    """
    fd = sys.stdin.fileno()
    # tcgetattr returns a list of lists/ints:
    # [iflag, oflag, cflag, lflag, ispeed, ospeed, cc]
    old: list[Union[int, list[Union[int, bytes]]]] = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return ch.lower()


def clear() -> None:
    """Clears the terminal screen."""
    os.system("clear")
