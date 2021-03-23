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

from avacore.processor_fr import process_reports_fr
from avacore.processor_ch import process_reports_ch
from avacore.processor_caaml import parse_xml, parse_xml_bavaria, parse_xml_vorarlberg

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
        reports = process_reports_fr(region_id)
        provider = "Rédigé par Météo-France avec la contribution des observateurs du réseau nivo-météorologique. Partenariat : "\
            + "ANMSM (Maires de Stations de Montagne), DSF (Domaines Skiables de France), "\
            + "ADSP (Directeurs de Pistes et de la Sécurité des Stations de Sports d'Hiver) et autres acteurs de la montagne."
    elif region_id.startswith("CH"):
        reports = process_reports_ch(lang=local, path=cache_path, cached=from_cache)
        provider = "WSL Institute for Snow and Avalanche Research SLF: www.slf.ch"
    else:
        url, provider = get_report_url(region_id, local)

        logging.info('Fetching %s', url)
        root = get_xml_as_et(url)
        if region_id.startswith("AT8") or region_id.startswith("AT-08"):
            reports = parse_xml_vorarlberg(root)
        elif region_id.startswith("BY"):
            reports = parse_xml_bavaria(root, "bavaria")
        elif region_id.startswith("SI"):
            reports = parse_xml_bavaria(root, "slovenia")
        else:
            reports = parse_xml(root)
    return reports, provider, url


def try_parse_datetime(datetime_string):

    '''try to parse a datetime from string with matching format'''

    try:
        r_datetime = datetime.strptime(datetime_string, '%Y-%m-%dT%XZ')
    except:
        try:
            r_datetime = datetime.strptime(datetime_string[:19], '%Y-%m-%dT%X') # 2019-04-30T15:55:29+01:00
        except:
            r_datetime = datetime.now()
    return r_datetime

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

    #Vorarlberg
    if region_id.startswith("AT8") or region_id.startswith("AT-08"):
        url = "https://warndienste.cnv.at/dibos/lawine_en/avalanche_bulletin_vorarlberg_en.xml"
        provider = "The displayed information is provided by an open data API on https://warndienste.cnv.at by: "\
            "Landeswarnzentrale Vorarlberg - http://www.vorarlberg.at/lawine"
        if "DE" in local.upper():
            url = "http://warndienste.cnv.at/dibos/lawine/avalanche_bulletin_vorarlberg_de.xml"
            provider = "Die dargestellten Informationen werden über eine API auf https://warndienste.cnv.at abgefragt. Diese wird "\
                "bereitgestellt von der Landeswarnzentrale Vorarlberg - http://www.vorarlberg.at/lawine"

    #Bavaria
    if region_id.startswith("BY"):
        url = "https://www.lawinenwarndienst-bayern.de/download/lagebericht/caaml_en.xml"
        provider = "The displayed ihe displayed information is provided by an open data API on https://www.lawinenwarndienst-bayern.de/ "\
            "by: Avalanche warning centre at the Bavarian State Office for the Environment - https://www.lawinenwarndienst-bayern.de/"
        if "DE" in local.upper():
            url = "https://www.lawinenwarndienst-bayern.de/download/lagebericht/caaml.xml"
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

### Data-Classes

class Problem:
    '''
    Defines a avalanche problem with aspect and elevation
    '''
    problem_type: str
    aspect: list
    valid_elevation: str

    def __init__(self, problem_type: str, aspect: list, validElev: str) -> None:
        self.problem_type = problem_type
        self.aspect = aspect
        self.valid_elevation = clean_elevation(validElev)

    def __str__(self):
        return "{'problem_type':'" + self.problem_type + "', 'aspect':" + str(self.aspect) + ", 'valid_elevation':'" \
            + self.valid_elevation + "'}"

    def __repr__(self):
        return str(self)

class DangerMain:
    '''
    Defines Danger-Level with elevation
    '''
    main_value: int
    valid_elevation: str

    def __init__(self, mainValue: int, validElev: str):
        self.main_value = mainValue
        self.valid_elevation = clean_elevation(validElev)

class ReportText:
    '''
    Defines a report text with type.
    '''
    text_type: str
    text_content: str

    def __init__(self, text_type: str, text_content="") -> None:
        self.text_type = text_type
        self.text_content = text_content

    def __str__(self):
        return "{'text_type':'" + self.text_type + "', 'text_content':" + self.text_content + "'}"

    def __repr__(self):
        return str(self)

class AvaReport:
    '''
    Class for the AvaReport
    '''
    report_id: str
    '''ID of the Report'''
    valid_regions: typing.List[str]
    '''list of Regions'''
    rep_date: datetime
    '''Date of Report'''
    validity_begin: datetime
    '''valid time start'''
    validity_end: datetime
    '''valid time end'''
    predecessor_id: str
    '''ID of first report (AM) if Report is e. g. a PM-Report'''
    danger_main: typing.List[DangerMain]
    '''danger Value and elev'''
    dangerpattern: typing.List[str]
    '''list of Patterns'''
    problem_list: typing.List[Problem]
    '''list of Problems with Sublist of Aspect&Elevation'''
    report_texts: typing.List[ReportText]
    '''All textual elements of the Report'''

    def __init__(self):
        self.valid_regions = []
        self.danger_main = []
        self.dangerpattern = []
        self.problem_list = []
        self.report_texts = []

    def cli_out(self):
        print('╔═════ AvaReport ', self.report_id, ' ══════')
        if hasattr(self, 'predecessor_id'):
            print('║ This is PM-Report to: ', self.predecessor_id)
        print('║ Report from:          ', self.rep_date)
        print('║ Validity:             ', self.validity_begin, ' -> ', self.validity_end)
        print('║ Valid for:')
        for region in self.valid_regions:
            print('║ |- ', region)

        print('╟───── Danger Rating')
        for danger_main in self.danger_main:
            if danger_main.valid_elevation != None:
                print('║ ', danger_main.valid_elevation, ' -> : ', danger_main.main_value)
            else:
                print('║ ', danger_main.main_value, ' in entire range')

        print('╟───── Av Problems')
        for problem in self.problem_list:
            print('║ Problem: ', problem.problem_type, ' Elevation: ', problem.valid_elevation, ' Aspects: ', problem.aspect)

        if len(self.dangerpattern)  > 0:
            print('╟───── Danger Patterns')
            for dangerpattern in self.dangerpattern:
                print('║ ', dangerpattern)

        print('╟───── Av Texts (if not html or img)')
        for texts in self.report_texts:
            if texts.text_type != 'html_report_local' and texts.text_type != 'prone_locations_img' and \
                texts.text_type != 'html_weather_snow':
                print('║ ', texts.text_type, ': ', texts.text_content)

        print('╚══════════════════════════════════════════')


class JSONEncoder(json.JSONEncoder):
    """JSON serialization of datetime"""
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        try:
            return obj.toJSON()
        except: # pylint: disable=bare-except
            return obj.__dict__


def clean_elevation(elev: str):
    '''
    Cleans up the elevation description. Should move to the XML-Parsers.
    '''
    if elev in ['', '-', 'ElevationRange_Keine H\u00f6hengrenzeHi']:
        return None
    elev = re.sub(r'ElevationRange_(.+)Hi', r'>\1', elev)
    elev = re.sub(r'ElevationRange_(.+)(Lo|Lw)', r'<\1', elev)
    elev = elev.replace('Forestline', 'Treeline')
    return elev
