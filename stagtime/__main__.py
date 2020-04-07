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
    print: t.Callable[[str], None] = print,
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
