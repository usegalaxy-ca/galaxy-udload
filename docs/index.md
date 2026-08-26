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
pip install git+https://github.com/usegalaxy-ca/galaxy-udload@v1.1.0
```

# Quick Usage

## Upload
```bash
galaxy upload --history-id <id> --file A B C...
```
For more information, see [Upload](./upload.md)

## Download
```bash
galaxy download --dataset-id <id>
```
For more information, see [Download](./download.md)

## History
```bash
galaxy history
```
For more information, see [History](./history.md)

## Datasets
```bash
galaxy dataset
```
For more information, see [Dataset](./dataset.md)

## Acknowledgment
This project was inspired by the [Galaxy Project’s galaxy-upload repository](https://github.com/galaxyproject/galaxy-upload).  
We appreciate their work, which provided valuable inspiration in shaping this code base.
