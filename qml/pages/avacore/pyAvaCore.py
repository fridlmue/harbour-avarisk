"""
    Copyright (C) 2021 Friedrich Mütschele and other contributors
    This file is part of pyAvaCore.
    pyAvaCore is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    pyAvaCore is distributed in the hope that it will be useful, 
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with pyAvaCore. If not, see <http://www.gnu.org/licenses/>.
"""

import configparser
from datetime import datetime
from urllib import parse
from urllib.parse import urlparse
from urllib.request import urlopen
from pathlib import Path
import re
import json
import logging
import typing

from avacore.avabulletin import AvaBulletin
from avacore.processor_fr import process_reports_fr, process_all_reports_fr
from avacore.processor_ch import process_reports_ch
from avacore.processor_it import process_reports_it, process_all_reports_it
from avacore.processor_norway import process_reports_no
from avacore.processor_caamlv5 import parse_xml, parse_xml_bavaria, parse_xml_vorarlberg

config = configparser.ConfigParser()
config.read(f'{__file__}.ini')

### XML-Helpers

def get_xml_as_et(url):
    '''
    returns the xml-file from url as ElementTree
    '''

    with urlopen(url) as response:
        response_content = response.read()
    try:
        try:
            import xml.etree.cElementTree as ET
        except ImportError:
            import xml.etree.ElementTree as ET
        root = ET.fromstring(response_content.decode('utf-8'))
    except Exception as r_e:
        print('error parsing ElementTree: ' + str(r_e))
    return root

def get_reports(region_id, local='en', cache_path=str(Path('cache')), from_cache=False):
    '''
    returns array of AvaReports for requested region_id and provider information
    '''

    url = ''
    if region_id.startswith("FR"):
        if region_id == "FR":
            reports = process_all_reports_fr()
        else:
            reports = process_reports_fr(region_id)
        provider = "Rédigé par Météo-France avec la contribution des observateurs du réseau nivo-météorologique. Partenariat : "\
            + "ANMSM (Maires de Stations de Montagne), DSF (Domaines Skiables de France), "\
            + "ADSP (Directeurs de Pistes et de la Sécurité des Stations de Sports d'Hiver) et autres acteurs de la montagne."
    elif region_id.startswith("CH"):
        reports = process_reports_ch(lang=local, path=cache_path, cached=from_cache)
        url, provider = get_report_url(region_id, local)
    elif region_id.startswith('IT-') and not region_id.startswith('IT-32-BZ') and not region_id.startswith('IT-32-TN'):
        if region_id == 'IT-AINEVA':
            reports = process_all_reports_it()
        elif region_id == 'IT-21' or region_id == 'IT-23' or region_id == 'IT-25' or region_id == 'IT-34' or region_id == 'IT-36' or region_id == 'IT-57':
            reports = process_all_reports_it(region_prefix=region_id)
        else:
            reports = process_reports_it(region_id)
        provider = "AINEVA: aineva.it"
    elif region_id.startswith("NO"):
        reports = process_reports_no(region_id)
        provider = "varsom.no"
    else:
        url, provider = get_report_url(region_id, local)

        logging.info('Fetching %s', url)
        root = get_xml_as_et(url)

        if region_id.startswith("SI"):
            reports = parse_xml_bavaria(root, "slovenia")
        else:
            reports = parse_xml(root)
    return reports, provider, url


def get_report_url(region_id, local=''): #You can ignore "provider" return value by url, _ = getReportsUrl
    '''
    returns the valid URL for requested region_id
    '''
    name = config[region_id]['name']
    url = config[region_id]['url']
    if f'url.{local}' in config[region_id]:
        url = config[region_id][f'url.{local}']
    netloc = urlparse(url).netloc
    if "DE" == local.upper():
        provider = f"Die dargestellten Informationen werden über eine API auf {netloc} abgefragt. Diese wird bereitgestellt von: {name}."
    else:
        provider = f"The displayed information is provided by an open data API on {netloc} by: {name}"
    return url, provider



class JSONEncoder(json.JSONEncoder):
    """JSON serialization of datetime"""
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        try:
            return obj.toJSON()
        except: # pylint: disable=bare-except
            return obj.__dict__

