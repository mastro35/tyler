#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Tyler - a python tail supporting rolling files
# Copyright (C) 2016 Davide Mastromatteo - @mastro35
# ----------------------------------------------------

import sys
import os
import time
import platform


class Tyler(object):
    """
    Creates an iterable object that returns new lines.
    """

    def __init__(self, filename, os_is_windows=False):
        self._fh = None
        self._os_is_windows = os_is_windows

        self.filename = filename
        self.offset = 0
        self.opened_before = False

    def __del__(self):
        if self._fh:
            self._fh.close()

    def __iter__(self):
        return self

    def next(self):
        """
        Return the next line in the file, updating the offset.
        """
        my_line = None
        try:
            my_line = self._get_next_line()
        except StopIteration:
            raise

        return my_line

    def __next__(self):
        """`__next__` is the Python 3 version of `next`"""
        return self.next()

    def _get_next_line(self):
        my_line = str(self._filehandle().readline(),
                      encoding='utf-8', errors='ignore')
        self.offset = self._fh.tell()
        if not my_line:
            raise StopIteration
        return my_line

    def _getsize_of_current_file(self):
        size = 0
        try:
            old_file_position = self._fh.tell()
            self._fh.seek(0, os.SEEK_END)
            size = self._fh.tell()
            self._fh.seek(old_file_position, os.SEEK_SET)
        except:
            pass

        return size

    def _has_file_rolled(self):
        """Check if the file has been rolled"""
        # if the size is smaller then offset, the file has
        # probabilly been rolled
        if self._fh:
            size = self._getsize_of_current_file()
            if size < self.offset:
                return True

        return False

    def _open_file(self, filename):
        """Open a file to be tailed"""
        if not self._os_is_windows:
            self._fh = open(filename, "rb")
            self.filename = filename

            return

        # if we're in Windows, we need to use the WIN32 API to open the
        # file without locking it
        import win32file
        import msvcrt

        handle = win32file.CreateFile(filename,
                                      win32file.GENERIC_READ,
                                      win32file.FILE_SHARE_DELETE |
                                      win32file.FILE_SHARE_READ |
                                      win32file.FILE_SHARE_WRITE,
                                      None,
                                      win32file.OPEN_EXISTING,
                                      0,
                                      None)
        detached_handle = handle.Detach()
        file_descriptor = msvcrt.open_osfhandle(
            detached_handle, os.O_RDONLY)

        self._fh = open(file_descriptor, "rb")
        self.filename = filename

    def _filehandle(self):
        """
        Return a filehandle to the file being tailed, with the position set
        to the current offset.
        """
        # if file is opened and it has been rolled we need to close the file
        # and then to reopen it
        if self._fh and self._has_file_rolled():
            try:
                self._fh.close()
            except Exception:
                pass

            self._fh = None
            self.offset = 0

        # if the file is closed (or has been closed right now), open it
        if not self._fh:
            self._open_file(self.filename)

            if not self.opened_before:
                self.opened_before = True
                my_start_position = self._getsize_of_current_file()
                self._fh.seek(my_start_position)
                self.offset = self._fh.tell()

        return self._fh


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Usage: tyler [filename]")
        sys.exit(0)
    FILENAME = sys.argv[1]

    if not os.path.isfile(FILENAME):
        print("Specified file does not exists")
        sys.exit(8)

    IS_WINDOWS = (platform.system() == "Windows")
    MY_TYLER = Tyler(filename=FILENAME, os_is_windows=IS_WINDOWS)
    while True:
        try:
            for line in MY_TYLER:
                print(line)
            time.sleep(1)
        except KeyboardInterrupt:
            print("Quit signal received")
            sys.exit(0)
