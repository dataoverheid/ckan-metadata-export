# encoding: utf-8


import logging
import requests


lists = [
    'https://waardelijsten.dcat-ap-donl.nl/adms_changetype.json',
    'https://waardelijsten.dcat-ap-donl.nl/donl_catalogs.json',
    'https://waardelijsten.dcat-ap-donl.nl/donl_language.json',
    'https://waardelijsten.dcat-ap-donl.nl/donl_organization.json',
    'https://waardelijsten.dcat-ap-donl.nl/iana_mediatypes.json',
    'https://waardelijsten.dcat-ap-donl.nl/mdr_filetype_nal.json',
    'https://waardelijsten.dcat-ap-donl.nl/overheid_dataset_status.json',
    'https://waardelijsten.dcat-ap-donl.nl/overheid_frequency.json',
    'https://waardelijsten.dcat-ap-donl.nl/overheid_license.json',
    'https://waardelijsten.dcat-ap-donl.nl/overheid_openbaarheidsniveau.json',
    'https://waardelijsten.dcat-ap-donl.nl/overheid_taxonomiebeleidsagenda.json'
]
taxonomies = [
    'https://data.overheid.nl/service/waardelijsten/donl_communities'
]


class Translator:
    def __init__(self):
        self.terms = {
            'true': 'ja',
            'false': ''
        }

        for valuelist in lists:
            self.load_list(valuelist)

        for taxonomy in taxonomies:
            self.load_taxonomy(taxonomy)

    def load_list(self, valuelist: str) -> None:
        response = requests.get(valuelist)
        licence = 'https://waardelijsten.dcat-ap-donl.nl/overheid_license.json'

        try:
            response_json = response.json()

            if valuelist == licence:
                for values in response_json:
                    self.terms[values['id']] = values['title']
            else:
                for uri, values in response_json.items():
                    self.terms[uri] = values['labels']['nl-NL']

        except ValueError as e:
            logging.critical(e)
            exit(1)

    def load_taxonomy(self, taxonomy: str) -> None:
        response = requests.get(taxonomy)

        try:
            response_json = response.json()

            for values in response_json:
                self.terms[values['field_identifier']] = values['label_nl']

        except ValueError as e:
            logging.critical(e)
            exit(1)

    def add_translations(self, translations: dict) -> None:
        for key, value in translations.items():
            self.terms[key] = value

    def translate(self, term):
        if isinstance(term, list):
            return [self.translate(item) for item in term]

        return self.terms.get(term, term)
