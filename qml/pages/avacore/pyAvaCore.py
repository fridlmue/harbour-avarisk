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

from datetime import datetime
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

### XML-Helpers

def get_xml_as_et(url):

    '''returns the xml-file from url as ElementTree'''

    with urlopen(url) as response:
        response_content = response.read()
    try:
        try:
            import xml.etree.cElementTree as ET
        except ImportError:
            import xml.etree.ElementTree as ET
        if "VORARLBERG" in url.upper():
            root = ET.fromstring(response_content.decode('latin-1'))
        else:
            root = ET.fromstring(response_content.decode('utf-8'))
    except Exception as r_e:
        print('error parsing ElementTree: ' + str(r_e))
    return root

def get_reports(region_id, local='en', cache_path=str(Path('cache')), from_cache=False):

    '''returns array of AvaReports for requested region_id and provider information'''

    url = ''
    if region_id.startswith("FR"):
        logging.info('Fetching %s', region_id)
        if region_id == "FR":
            reports = process_all_reports_fr()
        else:
            reports = process_reports_fr(region_id)
        provider = "Rédigé par Météo-France avec la contribution des observateurs du réseau nivo-météorologique. Partenariat : "\
            + "ANMSM (Maires de Stations de Montagne), DSF (Domaines Skiables de France), "\
            + "ADSP (Directeurs de Pistes et de la Sécurité des Stations de Sports d'Hiver) et autres acteurs de la montagne."
    elif region_id.startswith("CH"):
        reports = process_reports_ch(lang=local, path=cache_path, cached=from_cache)
        provider = "WSL Institute for Snow and Avalanche Research SLF: www.slf.ch"
    elif region_id.startswith('IT-') and not region_id.startswith('IT-32-BZ') and not region_id.startswith('IT-32-TN'):
        if region_id == 'IT-AINEVA':
            reports = process_all_reports_it()
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
        '''
        if region_id.startswith("AT8") or region_id.startswith("AT-08"):
            reports = parse_xml_vorarlberg(root)
        elif region_id.startswith("BY"):
            reports = parse_xml_bavaria(root, "bavaria")
        '''
        if region_id.startswith("SI"):
            reports = parse_xml_bavaria(root, "slovenia")
        else:
            reports = parse_xml(root)
    return reports, provider, url


def get_report_url(region_id, local=''): #You can ignore "provider" return value by url, _ = getReportsUrl

    '''returns the valid URL for requested region_id'''

     # Euregio-Region Tirol, Südtirol, Trentino
    if ("AT-07" in region_id) or ("IT-32-BZ" in region_id) or ("IT-32-TN" in region_id):
        url = "https://avalanche.report/albina_files/latest/en.xml"
        provider = "The displayed information is provided by an open data API on https://avalanche.report by: "\
            "Avalanche Warning Service Tirol, Avalanche Warning Service Südtirol, Avalanche Warning Service Trentino."
        if "DE" in local.upper():
            url = "https://avalanche.report/albina_files/latest/de.xml"
            provider = "Die dargestellten Informationen werden über eine API auf https://avalanche.report abgefragt. Diese wird "\
            "bereitgestellt von: Avalanche Warning Service Tirol, Avalanche Warning Service Südtirol, Avalanche Warning Service Trentino."
        if "FR" in local.upper():
            url = "https://avalanche.report/albina_files/latest/fr.xml"
        provider = "The displayed information is provided by an open data API on https://avalanche.report by: "\
            "Avalanche Warning Service Tirol, Avalanche Warning Service Südtirol, Avalanche Warning Service Trentino."

    # Kärnten
    if region_id.startswith("AT-02"):
        url = "https://www.avalanche-warnings.eu/public/kaernten/caaml"
        provider = "Die dargestellten Informationen werden über eine API auf https://www.avalanche-warnings.eu abgefragt. Diese wird "\
            "bereitgestellt vom: Lawinenwarndienst Kärnten (https://lawinenwarndienst.ktn.gv.at)."

    # Salzburg
    if region_id.startswith("AT-05"):
        url = "https://www.avalanche-warnings.eu/public/salzburg/caaml/en"
        provider = "Die dargestellten Informationen werden über eine API auf https://www.avalanche-warnings.eu abgefragt. Diese wird "\
            "bereitgestellt vom: Lawinenwarndienst Salzburg (https://lawine.salzburg.at)."
        if "DE" in local.upper():
            url = "https://www.avalanche-warnings.eu/public/salzburg/caaml"
            provider = "The displayed information is provided by an open data API on https://www.avalanche-warnings.eu by: "\
                "Avalanche Warning Service Salzburg (https://lawine.salzburg.at)."

    # Steiermark
    if region_id.startswith("AT-06"):
        url = "https://www.avalanche-warnings.eu/public/steiermark/caaml/en"
        provider = "The displayed information is provided by an open data API on https://www.avalanche-warnings.eu by: "\
            "Avalanche Warning Service Steiermark (https://www.lawine-steiermark.at)."
        if "DE" in local.upper():
            url = "https://www.avalanche-warnings.eu/public/steiermark/caaml"
            provider = "Die dargestellten Informationen werden über eine API auf https://www.avalanche-warnings.eu abgefragt. "\
                "Diese wird bereitgestellt vom: Lawinenwarndienst Steiermark (https://www.lawine-steiermark.at)."

    # Oberösterreich
    if region_id.startswith("AT-04"):
        url = "https://www.avalanche-warnings.eu/public/oberoesterreich/caaml"
        provider = "Die dargestellten Informationen werden über eine API auf https://www.avalanche-warnings.eu abgefragt. Diese wird "\
            "bereitgestellt vom: Lawinenwarndienst Oberösterreich (https://www.land-oberoesterreich.gv.at/lawinenwarndienst.htm)."

    # Niederösterreich
    if region_id.startswith("AT-03"):
        url = "https://www.avalanche-warnings.eu/public/niederoesterreich/caaml"
        provider = "Die dargestellten Informationen werden über eine API auf https://www.avalanche-warnings.eu abgefragt. Diese wird "\
            "bereitgestellt vom: Lawinenwarndienst Niederösterreich (https://www.lawinenwarndienst-niederoesterreich.at)."
    
    '''
    #Vorarlberg - outdated!
    if region_id.startswith("AT8"):
        url = "https://warndienste.cnv.at/dibos/lawine_en/avalanche_bulletin_vorarlberg_en.xml"
        provider = "The displayed information is provided by an open data API on https://warndienste.cnv.at by: "\
            "Landeswarnzentrale Vorarlberg - http://www.vorarlberg.at/lawine"
        if "DE" in local.upper():
            url = "http://warndienste.cnv.at/dibos/lawine/avalanche_bulletin_vorarlberg_de.xml"
            provider = "Die dargestellten Informationen werden über eine API auf https://warndienste.cnv.at abgefragt. Diese wird "\
                "bereitgestellt von der Landeswarnzentrale Vorarlberg - http://www.vorarlberg.at/lawine"
    '''

    #Vorarlberg Neu
    if region_id.startswith("AT-08"):
        url = "https://www.avalanche-warnings.eu/public/vorarlberg/caaml/en"
        provider = "The displayed information is provided by an open data API on https://warndienste.cnv.at by: "\
            "Landeswarnzentrale Vorarlberg - http://www.vorarlberg.at/lawine"
        if "DE" in local.upper():
            url = "https://www.avalanche-warnings.eu/public/vorarlberg/caaml"
            provider = "Die dargestellten Informationen werden über eine API auf https://warndienste.cnv.at abgefragt. Diese wird "\
                "bereitgestellt von der Landeswarnzentrale Vorarlberg - http://www.vorarlberg.at/lawine"

    '''
    #Bavaria - outdated
    if region_id.startswith("BY"):
        url = "https://www.lawinenwarndienst-bayern.de/download/lagebericht/caaml_en.xml"
        provider = "The displayed ihe displayed information is provided by an open data API on https://www.lawinenwarndienst-bayern.de/ "\
            "by: Avalanche warning centre at the Bavarian State Office for the Environment - https://www.lawinenwarndienst-bayern.de/"
        if "DE" in local.upper():
            url = "https://www.lawinenwarndienst-bayern.de/download/lagebericht/caaml.xml"
            provider = "Die dargestellten Informationen werden über eine API auf https://www.lawinenwarndienst-bayern.de abgefragt. "\
                "Diese wird bereitgestellt von der Lawinenwarnzentrale Bayern (https://www.lawinenwarndienst-bayern.de)."
    '''
            
    #Bavaria - neu
    if region_id.startswith("DE-BY"):
        url = "https://www.avalanche-warnings.eu/public/bayern/caaml/en"
        provider = "The displayed ihe displayed information is provided by an open data API on https://www.lawinenwarndienst-bayern.de/ "\
            "by: Avalanche warning centre at the Bavarian State Office for the Environment - https://www.lawinenwarndienst-bayern.de/"
        if "DE" in local.upper():
            url = "https://www.avalanche-warnings.eu/public/bayern/caaml"
            provider = "Die dargestellten Informationen werden über eine API auf https://www.lawinenwarndienst-bayern.de abgefragt. "\
                "Diese wird bereitgestellt von der Lawinenwarnzentrale Bayern (https://www.lawinenwarndienst-bayern.de)."

    #Val d'Aran
    if region_id.startswith("ES-CT-L"):
        url = "http://statics.lauegi.report/albina_files_local/latest/en.xml"
        provider = "The displayed ihe displayed information is provided by an open data API on https://lauegi.conselharan.org/ by: "\
            "Conselh Generau d'Aran - https://lauegi.conselharan.org/"
        if "DE" in local.upper():
            url = "http://statics.lauegi.report/albina_files_local/latest/de.xml"
            provider = "Die dargestellten Informationen werden über eine API auf https://lauegi.conselharan.org/ abgefragt. "\
                "Diese wird bereitgestellt von Conselh Generau d'Aran (https://lauegi.conselharan.org/)."
        if "FR" in local.upper():
            url = "http://statics.lauegi.report/albina_files_local/latest/fr.xml"
            provider = "The displayed ihe displayed information is provided by an open data API on https://lauegi.conselharan.org/ by: "\
                "Conselh Generau d'Aran - https://lauegi.conselharan.org/"

    if region_id.startswith("SI"):
        url = "https://meteo.arso.gov.si/uploads/probase/www/avalanche/text/sl/bulletinAvalanche.xml"
        provider = "Slovenia"

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

