# Dataset

## Usage
```bash
usage: galaxy dataset [-h] [-l] [-n DATASET_NAME] [--dataset-id DATASET_ID] [-i] [--history-id HISTORY_ID]

UseGalaxy dataset utility.

options:
  -h, --help            show this help message and exit
  -l, --list            List user datasets (default: True)
  -n, --dataset-name DATASET_NAME
                        Dataset name to filter on (default: None)
  --dataset-id, --check-dataset-id DATASET_ID
                        Dataset id to check existence of (default: None)
  -i, --ignore-case     Search for datasets ignoring case (default: False)
  --history-id HISTORY_ID
                        Restrict datasets to a specific history id (default: None)
```

## List datasets
By default, its lists all datasets
```bash
galaxy dataset
```
or using the `--list` argument:
```bash
galaxy dataset --list
```

## Search
Search for an dataset by name
```bash
galaxy dataset --dataset-name pasted 
```
will return all the histories that matches `pasted` (case sensitive)
<pre>┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━┓
┃<b> dataset id </b>┃<b> dataset name </b>┃<b> last updated </b>┃<b> history id </b>┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━┩
└────────────┴──────────────┴──────────────┴────────────┘
</pre>

### Search case-insensitively
And you can search case-insensitively
```bash
galaxy dataset --dataset-name pasted -i
```
will return all the histories that matches `unn` ignoring case
<pre>┏━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┓
┃<b> dataset id       </b>┃<b> dataset name </b>┃<b> last updated        </b>┃<b> history id       </b>┃
┡━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━┩
│<font color="#06989A"> 74df81c5c85d8564 </font>│<font color="#60B48A"> Pasted Entry </font>│<font color="#FF8700"> 2026-07-23 02:15:41 </font>│<font color="#75507B"> 697304b47bf86889 </font>│
│<font color="#06989A"> f962859c9afb4a74 </font>│<font color="#60B48A"> Pasted Entry </font>│<font color="#FF8700"> 2026-07-17 01:59:32 </font>│<font color="#75507B"> 697304b47bf86889 </font>│
│<font color="#06989A"> 5f83dfbc1bd20549 </font>│<font color="#60B48A"> Pasted Entry </font>│<font color="#FF8700"> 2025-09-26 16:18:59 </font>│<font color="#75507B"> bc0a36ece81c9189 </font>│
└──────────────────┴──────────────┴─────────────────────┴──────────────────┘
</pre>

## Check existence
Check that a dataset exists
```bash
galaxy dataset --check <id>
```
or
```bash
galaxy dataset --dataset-id <id>
```

When the dataset exists this will return:
```bash
galaxy dataset --check f962859c9afb4a74
```
<pre>Dataset with id <font color="#06989A"><i>f962859c9afb4a74</i></font> <font color="#60B48A">exists</font></pre>

and when it does not:
```bash
galaxy dataset --check A
```
<pre>Dataset with id <font color="#06989A"><i>A</i></font> <font color="#C4A000">does not exist</font></pre>

## Restrict datasets to a given history
Show the datasets from an history
```bash
galaxy dataset --history-id 697304b47bf86889
```
<pre>┏━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┓
┃<b> dataset id       </b>┃<b> dataset name </b>┃<b> last updated        </b>┃<b> history id       </b>┃
┡━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━┩
│<font color="#06989A"> 74df81c5c85d8564 </font>│<font color="#60B48A"> Pasted Entry </font>│<font color="#FF8700"> 2026-07-23 02:15:41 </font>│<font color="#75507B"> 697304b47bf86889 </font>│
│<font color="#06989A"> f962859c9afb4a74 </font>│<font color="#60B48A"> Pasted Entry </font>│<font color="#FF8700"> 2026-07-17 01:59:32 </font>│<font color="#75507B"> 697304b47bf86889 </font>│
└──────────────────┴──────────────┴─────────────────────┴──────────────────┘
</pre>
