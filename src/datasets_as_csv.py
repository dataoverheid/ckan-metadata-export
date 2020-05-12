# encoding: utf-8


import csv
import ckan
import logging
import os
import translator
from slugify import slugify
from argparse import ArgumentParser


logging.basicConfig(format='%(asctime)s \t %(levelname)s \t %(message)s',
                    level=logging.INFO)


csv_columns = {
    'CKAN ID': 'id',
    'CKAN Name': 'name',
    'CKAN organization': 'owner_org',
    'CKAN Created': 'metadata_created',
    'CKAN LastModified': 'metadata_modified',
    'Identifier': 'identifier',
    'Title': 'title',
    'LandingsPage': 'url',
    'Changetype': 'changetype',
    'Authority': 'authority',
    'Publisher': 'publisher',
    'Status': 'dataset_status',
    'AccessRights': 'access_rights',
    'Theme': 'theme',
    'License': 'license_id',
    'Language': 'metadata_language',
    'SourceCatalog': 'source_catalog',
    'HighValue': 'high_value',
    'Basisregister': 'basis_register',
    'Referentiedata': 'referentie_data',
    'NationalCoverage': 'national_coverage',
    'Community': 'communities',
    'TagCount': 'num_tags',
    'DistributionCount': 'num_resources',
    'DistributionFormats': 'resource_formats'
}


if __name__ == '__main__':
    parser = ArgumentParser(description='Analyzes the contents of a CKAN '
                                        'installation and generates a CSV file '
                                        'from its datasets')
    parser.add_argument('source', metavar='s', type=str,
                        help='The CKAN installation to target, omit the '
                             'trailing \'/\'.')
    source = parser.parse_args().source
    this_file = os.path.basename(__file__)

    logging.info('%s starting', this_file)
    logging.info(' > source %s', source)

    ckan = ckan.CKAN(source, verify=True)
    datasets = ckan.datasets(query='*:*', batch_size=1000)

    translator = translator.Translator()
    translator.add_translations(ckan.organizations())

    target_file = os.path.join(
        os.path.dirname(__file__),
        '../export/{0}__{1}.csv'.format(this_file, slugify(source))
    )

    logging.info(' > target %s', target_file)

    with open(target_file, 'w+', newline='') as fh:
        writer = csv.writer(fh)
        writer.writerow(csv_columns.keys())

        for dataset in datasets:
            dataset['resource_formats'] = [resource.get('format') for resource
                                           in dataset.get('resources')]
            entry = []

            for csv_column in csv_columns.values():
                val = dataset.get(csv_column, '')

                if 'title' == csv_column:
                    val = val.encode('utf-8')

                translated = translator.translate(val)

                if isinstance(translated, list):
                    entry.append(', '.join(translated))
                else:
                    entry.append(translated)

            writer.writerow(entry)

    fh.close()

    logging.info('%s finished', this_file)
