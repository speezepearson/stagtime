"""Print a line at the moment of each standard TagTime ping.

Simple standalone usage:

    python stagtime/

You probably want to pipe this into something that catches your attention:

    python stagtime/ | while read; do afplay /System/Library/Sounds/Purr.aiff; done

I personally have the following command run on startup:

    tmux new -d -s tagtimed -- 'cd ~/stagtime/; python stagtime/ | while read line; do echo "$line"; for _ in {1..3}; do afplay /System/Library/Sounds/Purr.aiff; done; done; bash'

"""

import argparse
import datetime
import enum
import json
import sys
import time
import typing as t
from stagtime import Timekeeper

UTC = datetime.timezone.utc

class PingFormat(enum.Enum):
    JSON = 'json'
    ISO8601 = 'iso8601'
    LOCAL = 'local'

FORMAT_FUNCS = {
    PingFormat.ISO8601: lambda now, nextping: nextping.astimezone(UTC).strftime('%Y-%m-%dT%H:%M:%SZ'),
    PingFormat.LOCAL: lambda now, nextping: nextping.astimezone(None).strftime('%Y-%m-%d %H:%M:%S'),
    PingFormat.JSON: lambda now, nextping: json.dumps({
        PingFormat.ISO8601.value: FORMAT_FUNCS[PingFormat.ISO8601](now, nextping),
        PingFormat.LOCAL.value: FORMAT_FUNCS[PingFormat.LOCAL](now, nextping),
    }),
}

parser = argparse.ArgumentParser()
parser.add_argument("--format", choices=list(PingFormat), type=PingFormat, default=PingFormat.JSON)
parser.add_argument("--start-seconds-ago", type=float, default=0.0)

def main(
    ping_format: PingFormat,
    timekeeper: Timekeeper = None,
    get_time: t.Callable[[], datetime.datetime] = lambda: datetime.datetime.now(UTC),
    sleep: t.Callable[[datetime.timedelta], None] = lambda dt: time.sleep(dt.total_seconds()),
    print: t.Callable[[str], None] = lambda s: (print(s), sys.stdout.flush()),
    start_ago: datetime.timedelta = datetime.timedelta(seconds=0),
):
    if timekeeper is None:
        timekeeper = Timekeeper()

    timekeeper.init((get_time() - start_ago).timestamp())
    while True:
        nextping = datetime.datetime.fromtimestamp(timekeeper.nextping(), tz=UTC)
        now = get_time()
        if now < nextping:
            sleep(nextping - get_time())
        print(FORMAT_FUNCS[args.format](now, nextping))

if __name__ == '__main__':
    args = parser.parse_args()
    try:
        main(ping_format=args.format, start_ago=datetime.timedelta(seconds=args.start_seconds_ago))
    except KeyboardInterrupt:
        print("Keyboard interrupt caught, exiting...", file=sys.stderr)
