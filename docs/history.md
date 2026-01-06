# History

## Usage
```
usage: galaxy history [-h] [-l] [-n HISTORY_NAME] [--history-id HISTORY_ID] [-i] [--recent]

UseGalaxy history utility.

options:
  -h, --help            show this help message and exit
  -l, --list            List user histories (default: True)
  -n, --history-name HISTORY_NAME
                        History name to filter on (default: None)
  --history-id, --check-history-id HISTORY_ID
                        History id to filter on (default: None)
  -i, --ignore-case     Search for histories by ignoring case (default: False)
  --recent              Display most recent history (not deleted) (default: False)
```

## List histories
By default, its lists histories
```bash
galaxy history
```
or using the `--list` argument:
```bash
galaxy history --list
```

## Search
Search for an history by name
```bash
galaxy history --history-name Unn
```
will return all the histories that matches `Unn`
<pre>┏━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓
┃<b> id               </b>┃<b> name            </b>┃<b> last modified       </b>┃
┡━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━┩
│<font color="#06989A"> dac8a4fd6ad7573f </font>│<font color="#60B48A"> Unnamed history </font>│<font color="#FF8700"> 2026-01-06 19:58:19 </font>│
│<font color="#06989A"> b25fbdc82ddd9710 </font>│<font color="#60B48A"> Unnamed history </font>│<font color="#FF8700"> 2026-01-06 19:18:55 </font>│
└──────────────────┴─────────────────┴─────────────────────┘
</pre>

### Search case-insensitively
And you can search case-insensitively
```bash
galaxy history --history-name unn -i
```
will return all the histories that matches `unn` ignoring case
<pre>┏━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓
┃<b> id               </b>┃<b> name            </b>┃<b> last modified       </b>┃
┡━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━┩
│<font color="#06989A"> dac8a4fd6ad7573f </font>│<font color="#60B48A"> Unnamed history </font>│<font color="#FF8700"> 2026-01-06 19:58:19 </font>│
│<font color="#06989A"> b25fbdc82ddd9710 </font>│<font color="#60B48A"> Unnamed history </font>│<font color="#FF8700"> 2026-01-06 19:18:55 </font>│
└──────────────────┴─────────────────┴─────────────────────┘
</pre>

## Check existence
Check that an history exists
```bash
galaxy history --check <id>
```
or
```bash
galaxy history --history-id <id>
```

When the history exists this will return:
```bash
galaxy history --check b25fbdc82ddd9710
```
<pre>History with id <font color="#06989A"><i>b25fbdc82ddd9710</i></font> <font color="#60B48A">exists</font></pre>

and when it does not:
```bash
galaxy history --check A
```
<pre>History with id <font color="#06989A"><i>A</i></font> <font color="#C4A000">does not exists</font>
</pre>

## Recent history
Show the most recent used (not deleted) history
```bash
galaxy history --recent
```
<pre>
┏━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓
┃<b> id               </b>┃<b> name            </b>┃<b> last modified       </b>┃
┡━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━┩
│<font color="#06989A"> dac8a4fd6ad7573f </font>│<font color="#60B48A"> Unnamed history </font>│<font color="#FF8700"> 2026-01-06 19:58:19 </font>│
└──────────────────┴─────────────────┴─────────────────────┘
</pre>
