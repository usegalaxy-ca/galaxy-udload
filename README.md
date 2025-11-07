# galaxy-udload
UseGalaxy upload/download utility, to assist in downloading or uploading files.

# Get you API Key
From UseGalaxy, under User Preferences, select Manage API Key and create an API Key.

# Configuration file
On the desired system, create a file `.env` that follow the format:
```bash
GALAXY_API_KEY=<you API key>
GALAXY_URL=https://usegalaxy.ca
```

# Installation
0. Load any python module (Alliance's system)
1. Create a virtual environment:
```bash
virtualenv ~/ENV && source ~/ENV/bin/activate
```
2. Install the utility (from stable branch):
```bash
pip install git+https://github.com/usegalaxy-ca/galaxy-udload@main
```
or specify a tag
```bash
pip install git+https://github.com/usegalaxy-ca/galaxy-udload@v0.1.0
```

# Usage
## Upload
Upload one or more files to a specific history.
```bash
galaxy-upload --env path/to/.env --history-id <id> --file A B C...
```

## Download
Download a dataset locally.
```bash
galaxy-download --env path/to/.env --dataset-id <id>
```

Download a dataset to a specific name, or directory
```bash
galaxy-download --env path/to/.env --dataset-id <id> --path <filename|directory/filename>
```
