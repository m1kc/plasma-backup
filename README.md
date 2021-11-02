# plasma-backup

Plasma is a small and simple backup utility designed to be able to do backups using btrfs snapshots. So, its primary (not the only one, fortunately) usecase is: take a btrfs filesystem, make a read-only snapshot, tar it up and upload on remote server via SSH. Naturally, it also provides tools for backup rotation, that is, deleting old archives.

* :wrench: Quality: **stable** with caveats (see below)
* :cityscape: Was used in production: **Dec 2017 — Jul 2021** (on fleet of 30 servers)
* :2nd_place_medal: Was awarded a title (by me) of 2nd best backup utility in the world (1st place taken by [borg](https://borgbackup.readthedocs.io))


## Why snapshots?

Imagine backing up a really large frequently changed file&nbsp;&mdash; like, a database. If you just copy it to another machine, you will discover that the copy is a complete garbage&nbsp;&mdash; it looks like a database but your RDBMS says it's not valid. That happened because these files are not append-only: while you copy the file's tail, RDBMS changes its head, transaction becomes half-written-half-not, and the whole DB becomes unusable.

Btrfs snapshots, on the other hand, mitigate this issue. Once you create a snapshot, all the files within it are frozen, and any consequent writes do not affect snapshot's state. In other words, to your RDBMS snapshotting looks like a sudden loss of electricity&nbsp;&mdash; and most of them are specifically designed to handle such cases. Specifically, MySQL and PostgreSQL seem to recover from these backups quite successfully.

Please note that snapshotting a working database is not the only and definitely not the best way to do this. Consider using `pg_dump` or similar tools first. Use snapshots only if you're sure what are you doing.


## Compatibility promise

We promise not to break existing features, configs, etc. until a major release.

## Known issues (or features)

* Up to a half of your disk space will be reserved for backup archive;
* btrfs snapshotting is dumb (see below).


## Installing (Arch Linux)

```sh
git clone https://github.com/m1kc/plasma-backup
cd plasma-backup/archlinux
makepkg -si
```


## Configuration (backup storage)

Install Plasma, create some folders for your backups, one per machine. Their names and locations do not matter. What matters, however, is that every such folder contains a file named `plasma-rotate.json` with content like this:

```json
{
    "policy": {
        "daily": 5,
        "weekly": 3,
        "monthly": 2
    }
}
```

These numbers indicate how many backups of each type should be stored. Monthly backups happen at 1st day of every month, weekly backups - on 1st day of every week, any other backup is considered daily. In the example above, Plasma will always store 5+3+2=10 last backups (even if some weekly backup happens on 1st day of month, slot will be used for an extra weekly backup).

Also make sure that every agent can write to these folders using SSH without a password (set up public key auth for this purpose).


## Configuration (agents)

Install Plasma on every machine, then edit `/etc/plasma-agent.conf`. Note that this file must be a valid JSON (you can't actually put comments there).

```js
{
    // What to back up
    "folders": [
        "/bin",
        "/etc"
    ],
    // Where to store backup archive prior to uploading it
    "tempfile": "/tmp/backup.tar",
    // Desired backup strategy and its options (see below)
    "strategy": "tar",
    "options": {},

    // SSH credentials
    "ssh": {
        "host": "127.0.0.1",
        "login": "plasma"
    },
    // Where to put backups on remote machine
    "remoteFolder": "/data/backup",

    // Commands to execute before the actual backup (if they fail, operation is canceled)
    "executeBefore": ["df -h"],
    // Commands to execute after successful backup (Plasma will always execute all of them, no matter if they fail or not)
    "executeAfter": ["echo THIS WAS A TRIUMPH", "echo I AM MAKING A NOTE HERE: HUGE SUCCESS"]
}
```

Make a test backup by running `sudo plasma-agent`. To enable midnight timer, type `sudo systemctl enable --now plasma-agent.timer` (systemd only, use cronjobs for other distributions).


## Backup strategies

* `tar` &mdash; Just tar up target folders.
* `btrfs-snapshot` &mdash; Make a read-only snapshot of filesystem, then tar things up. **IMPORTANT:** This strategy is somewhat dumb and assumes that all your target folders are located in the same mountpoint as `/`, and it's btrfs. In other words, it makes a snapshot of `/` and then runs `tar`, so if any of the target files are located on another filesystem, they will still be archived but won't be covered by snapshotting (which is probably not what you want, altough it depends on the situation). Currently the only way to work around this issue is to make modifications to Plasma source code. We'll address that in the future.
* `noop` &mdash; Use for debugging. Just creates an empty file.
