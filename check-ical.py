import argparse
from datetime import datetime, timezone, timedelta
import json
from sys import stderr
from os import environ

import ics
import requests


def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("calendar_tzoffset", type=float, nargs="?")
    parser.add_argument("datetime", type=dt_parser, nargs="?", default=datetime.now(timezone.utc))
    return parser


def dt_parser(s):
    try:
        return datetime.fromisoformat(s)
    except Exception as e:
        print(f"{e}: fallback to datetime.now(timezone.utc)", file=stderr)
    return datetime.now(timezone.utc)


def main(url, dt, offset):
    r = requests.get(url)
    cal = ics.Calendar(r.text)
    offset = timedelta(hours=offset) if offset else timedelta()
    events = []
    for e in sorted(cal.events):
        if e.begin - offset <= dt < e.end - offset:
            print(e.name, e.begin - offset, e.end - offset)
            events.append({
                "name": e.name,
                "description": e.description,
                "begin": e.begin.datetime.isoformat(),
                "end": e.end.datetime.isoformat(),
            })
    file = open(environ.get("GITHUB_OUTPUT"), "w+")
    print("events={}".format(json.dumps(events, ensure_ascii=False)), file=file)
    print("has-events={}".format(json.dumps(bool(events))), file=file)


if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()
    main(args.url, args.datetime, args.calendar_tzoffset)
