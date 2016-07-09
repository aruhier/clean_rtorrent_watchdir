#!/usr/bin/env python3

import argparse
import glob
import hashlib
import os

BUF_SIZE = 65536


def hash_all_torrents(source_dir):
    for torrent in glob.glob(os.path.join(source_dir, "*.torrent")):
        torrent_hash = hashlib.sha256()
        with open(torrent, "rb") as f:
            while True:
                data = f.read(BUF_SIZE)
                if not data:
                    break
                torrent_hash.update(data)

        yield (torrent, torrent_hash.hexdigest())


def clean(session_dir, watch_dir, dryrun=True):
    session_torrents_hash = tuple(r[1] for r in hash_all_torrents(session_dir))
    for torrent, t_hash in hash_all_torrents(watch_dir):
        if t_hash in session_torrents_hash:
            continue
        elif dryrun:
            print(torrent)
        else:
            os.remove(torrent)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Clean torrents of a watch directory when they are not in the "
            "session directory anymore"
        )
    )

    parser.add_argument("session_dir", metavar="session_dir", type=str,
                        help="rtorrent session dir")
    parser.add_argument("watch_dir", metavar="watch_dir", type=str,
                        help="rtorrent watch dir")
    parser.add_argument(
        "-D", "--dryrun",
        help="dry run, to print files that would normally be removed",
        dest="dryrun", action="store_true"
    )

    args = parser.parse_args()
    clean(**vars(args))
