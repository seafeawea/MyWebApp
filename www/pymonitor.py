#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'XZ'

import os
import sys
import time
import subprocess

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def log(s):
    print '[Monitor] %s' % s


class MyFileSystemEventHandler(FileSystemEventHandler):

    def __init__(self, fn):
        super(MyFileSystemEventHandler, self).__init__()
        self.restart = fn

    def on_any_event(self, event):
        if event.src_path.endswith('.py'):
            log('Python source file changed: %s' % event.src_path)
            self.restart()


command = ['echo', 'ok']
process = None


def kill_process():
    global process
    if process:
        log('Kill process [%s]...' % process.pid)
        process.kill()
        process.wait()
        log('Process ended with code %s.' % process.returncode)
        process = None


def start_process():
    global process, command
    log('Start process %s...' % ' '.join(command))
    process = subprocess.Popen(command, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)


def restart_process():
    kill_process()
    start_process()


def start_watch(path, callback):
    """
    Here are some tips for below understanding

    Observer.Schedule
    Schedules watching a path and calls appropriate methods specified
        in the given event handler in response to file system events.
    """
    observer = Observer()
    observer.schedule(MyFileSystemEventHandler(restart_process), path, recursive=True)
    observer.start()
    log('Watching directory %s...' % path)
    start_process()
    try:
        while True:
            time.sleep(0.5)     # Keep run here
    except KeyboardInterrupt:   # If detect Ctrl+C
        observer.stop()  # Signals the thread to stop
    observer.join()  # Wait until the thread terminates


if __name__ == '__main__':
    argv = sys.argv[1:]
    if not argv:
        print('Usage: ./pymonitor your-script.py')
        exit(0)
    if argv[0] != 'python':
        argv.insert(0, 'python')
    command = argv
    path = os.path.abspath('.')
    start_watch(path, None)
