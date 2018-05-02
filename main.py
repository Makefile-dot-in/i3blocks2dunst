#!/usr/bin/env python3

import subprocess
import sys
import json
from threading import Thread
from queue import Queue, Empty

def enqueue_output(out, queue):
    for line in iter(out.readline, ''):
        queue.put(line)
    out.close()
class VersionNotSupportedError(Exception):
    pass
sxhkd = subprocess.Popen(["sxhkd"], stdout=subprocess.PIPE, encoding='utf-8', bufsize=1)
i3blocks = subprocess.Popen(["i3blocks"] + sys.argv[1:], stdout=subprocess.PIPE, encoding='utf-8', bufsize=1)
sxhkq = Queue()
i3q = Queue()
sxhkt = Thread(target=enqueue_output, args=(sxhkd.stdout, sxhkq))
i3t = Thread(target=enqueue_output, args=(i3blocks.stdout, i3q))

if json.loads(i3blocks.stdout.readline())['version'] != 1:
    raise VersionNotSupportedError("This i3blocks version is not supported.")

def genlines(process):
    while True:
        yield process.readline()

blocks = {}
kbdpipe = genlines(sxhkd.stdout)
i3pipe = genlines(i3blocks.stdout)

while True:
    try:
        for i in i3q.get_nowait():
            blocks[i["name"] if i["name"] in i else "throwaway_pls_dont_try_to_exploit_this_thx"] = i["full_text"]
    except Empty:
        pass

    try:
        request = sxhkq.get_nowait().strip()
        subprocess.run(["notify-send", request, blocks[request]])
    except Empty:
        pass
