#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import time

from .process_logger import ProcessLogger


def main():
    description = "Log process info at specified interval (default: 1 sec)"
    usage = "python -m process_monitor [-h] (--pid PID | --name NAME) " \
            "[-s SECS] [-m MINS] [-hr HOURS] [-d DIR]"
    parser = argparse.ArgumentParser(description=description, usage=usage)
    proc_id_group = parser.add_mutually_exclusive_group(required=True)
    proc_id_group.add_argument("--pid", type=int)
    proc_id_group.add_argument("--name")
    parser.add_argument("-s", "--secs", type=int, default=0)
    parser.add_argument("-m", "--mins", type=int, default=0)
    parser.add_argument("-hr", "--hours", type=int, default=0)
    parser.add_argument("-d", "--dir", default=".",
                        help="logs directory (default: cwd)")

    args = parser.parse_args()

    interval = args.secs + args.mins * 60 + args.hours * 3600
    if not interval:
        interval = 1

    logger = ProcessLogger(interval, args.pid, args.name, args.dir)
    logger.start()

    try:
        while not logger.exception:
            time.sleep(.1)
    except KeyboardInterrupt:
        ...

    logger.stop()

if __name__ == "__main__":
    main()
