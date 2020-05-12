# CKAN Metadata Export

Repository: https://github.com/dataoverheid/ckan-metadata-export

## Contact

- Web: [data.overheid.nl/contact](https://data.overheid.nl/contact)
- Email: [opendata@overheid.nl](mailto:opendata@overheid.nl)

## Requirements

- Python 3.x
- Python-PIP
- See `requirements.txt` (and `dev-requirements.txt`) for specific pip dependencies

## License

Licensed under the CC0 license. View the `LICENSE.md` file for more information.

## Installation

```shell script
git clone https://github.com/dataoverheid/ckan-metadata-export.git
python3 -m venv ckan-metadata-export/venv
source ckan-metadata-export/venv/bin/activate
pip3 install -r ckan-metadata-export/requirements.txt --no-cache-dir
# (Optional) pip3 install -r ckan-metadata-export/dev-requirements.txt --no-cache-dir
```

## Usage

```shell script
cd /path/to/ckan-metadata-export
source venv/bin/activate
python src/datasets_as_csv.py https://data.overheid.nl/data

# Or, as a one-liner
/path/to/venv/bin/python /path/to/ckan-metadata-export/src/datasets_as_csv.py https://data.overheid.nl/data
```

The `https://data.overheid.nl/data` URL can be substituted for any other endpoint hosting a CKAN installation running the ckanext-dataoverheid CKAN extension.
All output is written to the `./export` directory, the exact file is indicated by the logging output.
