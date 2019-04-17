# -*-- coding:utf-8 -*--
import os

with open('taskId', 'r') as fr:
    lines = fr.readlines()
    lines = list(map(lambda x: x.strip(), lines))
    command = 'grep -oP "(%s)" callback-2019041314  | sort | uniq -c' % '|'.join(lines)
    os.system(command)
