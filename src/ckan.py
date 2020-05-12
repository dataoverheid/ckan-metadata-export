# encoding: utf-8


import logging
import requests


class CKAN:
    def __init__(self, base_uri: str, verify: bool = True):
        self.base_uri = base_uri
        self.verify = verify

    def datasets(self, query: str = '*:*', batch_size: int = 1000):
        request_offset = 0
        found_datasets = []
        got_all_datasets = False

        while not got_all_datasets:
            uri = self.base_uri + '/api/3/action/package_search'
            params = {
                'q': query,
                'start': request_offset,
                'rows': batch_size
            }
            response = requests.get(uri, dict((k, v) for k, v in params.items()
                                              if v is not None),
                                    verify=self.verify)
            try:
                response_json = response.json()
                result_count = response_json['result']['count']
                request_offset = request_offset + batch_size

                for dataset in response_json['result']['results']:
                    found_datasets.append(dataset)

                if request_offset >= result_count:
                    got_all_datasets = True
            except ValueError as e:
                logging.critical(e)
                exit(1)

        return found_datasets

    def organizations(self):
        uri = self.base_uri + '/api/3/action/organization_list'
        params = {
            'all_fields': True
        }
        response = requests.get(uri, dict((k, v) for k, v in params.items()
                                          if v is not None),
                                verify=self.verify)
        try:
            response_json = response.json()
            if response_json['success']:
                return {organization.get('id'): organization.get('title')
                        for organization in response_json['result']}
            else:
                logging.critical('ckan api response failure; success = false')
                exit(1)
        except ValueError as e:
            logging.critical(e)
            exit(1)
