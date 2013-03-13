Pope Names
==========

Scrape and parse all popes from [NewAdvent.org](http://www.newadvent.org/cathen/12272b.htm)

## Quick setup

It's recommended to make a virtualenv, then run:

```bash
pip install -r requirements.txt
```

## Data

The popes are represented in the JSON file popes.json in the data directory.

To recreate this file, run ```./scripts/fetch.py```, which will download the names from the page.

Pope names are parsed into salutation, name and number like so:

    moniker = re.findall("^(Blessed|[A-z]+\. )*(.*?)([IXV]*)$", data["fullname"])[0]
    data["title"],data["name"],data["number"] = [x.strip() for x in moniker]


