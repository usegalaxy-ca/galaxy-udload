# Download

## Usage
```
usage: galaxy download [-h] [--history-id HISTORY_ID] [--dataset-id DATASET_ID] [--dataset-name DATASET_NAME] [--path PATH] [-v]

UseGalaxy file download utility.

options:
  -h, --help            show this help message and exit
  --history-id HISTORY_ID
                        History id to filter on (default: None)
  --dataset-id DATASET_ID
                        Dataset id to filter on (default: None)
  --dataset-name DATASET_NAME
                        Exact dataset name to filter on (default: None)
  --path PATH           Output directory or file name to write to. (default: current working directory)
  -v, --verbose         Enable verbosity (default: 0)
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
