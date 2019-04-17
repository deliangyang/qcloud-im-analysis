# -*-- coding:utf-8 -*--
import os


class FileCache:
    __slots__ = ('filename', 'mode', )

    def __init__(self, filename, mode=''):
        self.filename = filename
        self.mode = mode or ''

    def exist(self):
        return os.path.exists(self.filename)

    def set(self, content):
        with open(self.filename, 'w' + self.mode) as f:
            f.write(content)
            f.close()

    def get(self):
        with open(self.filename, 'r' + self.mode) as f:
            content = f.read()
            f.close()
            return content
