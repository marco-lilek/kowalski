# Description

Tool for visualizing the connections between musical artists/labels and releases using data from discogs. See `screenshots/` for samples.

# Setup

## Dependencies

- python3

## Running the server

```
PYTHONPATH=. FLASK_APP=server.py flask run
```

## Using the plugin

Once loaded, click the plugin icon, and select the search strategy you would like you use. After selected, the server will begin generating a visualization of the artist/label/release network. Once complete, it should automatically open the resulting graph in your default browser.

# Caveats

The discogs API throttles clients at 60 requests per minute, so you may want to change the API keys if you find the server is getting stalled frequently

# TODO

- load results from a previous run if they exist/saving results to a database
