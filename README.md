# plasma-backup

`WORK IN PROGRESS` `EXPERIMENTAL SOFTWARE` Dec 2017

Plasma is a small and simple backup utility designed to be able to handle btrfs snapshots. So, its primary (not the only one, fortunately) usecase is: take a btrfs filesystem, make a read-only snapshot, tar it up and upload on remote server via SSH. It also provides tools for backup rotation, that is, deleting old archives.

Plasma used with `btrfs-snapshot` strategy is suitable for backing up working databases without stopping them. Not the best way (you probably should use pg_dump or something like this), but it's definitely possible. Such a backup would look like a sudden loss of electricity to your database and will probably just trigger its normal recovery procedures. MySQL and PostgreSQL seem to eat these backups quite successfully.


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

These numbers indicate how many backups of each types should be stored. Monthly backups happen at 1st of every month, weekly backups - on 1st day of every week, any other backup is considered daily. In the example above, Plasma will always store 5+3+2=10 last backups (even if some weekly backup happens on 1st day of month, slot will be used for an extra weekly backup).

Also make sure that every agent can write to these folders using SSH without a password (set up public key auth for this purpose).


## Configuration (agents)

Install Plasma on every machine, then edit `/etc/plasma-agent.conf`. Note that this file should be a valid JSON (you can't actually put comments there).

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
* `btrfs-snapshot` &mdash; Make a read-only snapshot of filesystem, then tar it up. **IMPORTANT:** This strategy is somewhat dumb and assumes that all your target folders are located in the same mountpoint as `/`, and it's btrfs. If that's not the case, you might need to make some modifications to Plasma source code to fit your case. We'll improve that in the future.
* `noop` &mdash; Use for debugging. Just creates an empty file.
