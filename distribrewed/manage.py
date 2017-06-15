#!/usr/bin python
import os
import signal
import sys


# This function is to kill the process immediately when docker sends SIGTERM signal
def handle_sigterm(signum, frame):
    exit(1)


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, handle_sigterm)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "twisted_brew.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
