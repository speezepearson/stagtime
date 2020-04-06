import argparse
import datetime
import json
from pathlib import Path
import subprocess
import threading
import time
import typing as t
from stagtime import Timekeeper

parser = argparse.ArgumentParser()
parser.add_argument("-l", "--logfile", type=Path, default=Path.home()/'.tagtime.jsons')
parser.add_argument("--on-ping-cmd", default=None, type=str)

def main(
    timekeeper: Timekeeper = None,
    get_time: t.Callable[[], datetime.datetime] = datetime.datetime.now,
    sleep: t.Callable[[datetime.timedelta], None] = lambda dt: time.sleep(dt.total_seconds()),
):
    if timekeeper is None:
        timekeeper = Timekeeper()

    timekeeper.init(get_time().timestamp())
    while True:
        nextping = datetime.datetime.fromtimestamp(timekeeper.nextping())
        now = get_time()
        if now < nextping:
            sleep(nextping - get_time())
        if args.on_ping_cmd is not None:
            threading.Thread(target=lambda: subprocess.run(args.on_ping_cmd, shell=True)).start()
        try:
            response = input("Whatcha doing ({:%Y-%m-%d %H:%M:%S})? ".format(nextping))
        except KeyboardInterrupt:
            print("Keyboard interrupt caught; exiting")
            return
        with args.logfile.open('a') as f:
            f.write(json.dumps({"ts": nextping.strftime("%Y-%m-%dT%H:%M:%SZ"), "response": response}))
            f.write('\n')

if __name__ == '__main__':
    args = parser.parse_args()
    main()
