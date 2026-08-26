# Download

## Usage
```
usage: galaxy download [-h] [--history-id HISTORY_ID] [--dataset-id DATASET_ID] [--dataset-name DATASET_NAME] [--path PATH] [-i]

UseGalaxy file download utility.

options:
  -h, --help            show this help message and exit
  --history-id HISTORY_ID
                        History id to download datasets from. (default: None)
  --dataset-id DATASET_ID
                        Dataset id to download (default: None)
  --dataset-name DATASET_NAME
                        Dataset name (regex) to filter on (default: None)
  --path PATH           Output directory or file name to write to. (default: /home/charles/Projects/galaxy-udload)
  -i, --ignore-case     Search for datasets ignoring case (default: False)
```

## Download
### With a specific id
Download a dataset locally.
```bash
galaxy download --dataset-id <id>
```

Download a dataset to a specific name, or directory
```bash
galaxy download --dataset-id <id> --path <filename|directory/filename>
```

Download all datasets from a given history
```bash
galaxy download --history-id <history-id>
```

Download matching datasets (by name)
```bash
galaxy download --dataset-name "pasted" --history-id <history-id> -i
```
