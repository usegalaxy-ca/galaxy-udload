# Upload

## Usage
```
usage: galaxy upload [-h] [--history-id HISTORY_ID] [--history-name HISTORY_NAME] [-i] --file FILE [FILE ...] [--checkpoints CHECKPOINTS]

UseGalaxy file upload utility.

options:
  -h, --help            show this help message and exit
  --history-id HISTORY_ID
                        History id to filter on (default: None)
  --history-name HISTORY_NAME
                        History name to filter on (default: None)
  -i, --ignore-case     Search for histories by ignoring case (default: False)
  --file FILE [FILE ...]
                        Input files path to upload. (default: None)
  --checkpoints CHECKPOINTS
                        Checkpoints file (default: .checkpoints)
```

## Upload
### With an history id
```bash
galaxy upload --history-id <id> --file A B C...
```

### With an history name
```bash
galaxy upload --history-name Unn --file A B C...
```

When multiple histories matches, an error will be returned:
```
┏━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓
┃ id               ┃ name            ┃ last modified       ┃
┡━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━┩
│ dac8a4fd6ad7573f │ Unnamed history │ 2026-01-06 19:58:19 │
│ b25fbdc82ddd9710 │ Unnamed history │ 2026-01-06 19:18:55 │
└──────────────────┴─────────────────┴─────────────────────┘

ERROR: Multiple histories matching Unn found!
Select one by specifying an id with --history-id.
```

Or if the history do not exists:
```
ERROR: No histories matching AAAAA found!
```

One can also ignore case by using `--ignore-case` to filter on histories.
