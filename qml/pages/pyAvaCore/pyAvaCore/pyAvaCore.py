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

import threading
from datetime import date
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from urllib.request import urlopen
from pathlib import Path
import copy
import re
import sys

# avaRisk only
import pickle

# ALBINA only
import json
import logging
import logging.handlers

"""
logging.basicConfig(
    format='[%(asctime)s] {%(module)s:%(lineno)d} %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.handlers.TimedRotatingFileHandler(filename=f'logs/pyAvaCore.log', when='midnight'),
        logging.StreamHandler(),
    ])
"""

def et_add_parent_info(element_tree):

    '''Add Parent-Info to structure an ElementTree'''

    for child in element_tree:
        child.attrib['__my_parent__'] = element_tree
        et_add_parent_info(child)

def et_get_parent(element_tree):

    '''get Parent-Info from ElementTree, when parent Info was added previously.'''

    if '__my_parent__' in element_tree.attrib:
        return element_tree.attrib['__my_parent__']
    return None

def get_xml_as_et(url):

    '''returns the xml-file from url as ElementTree'''


    #timeout_time = 5
    #with urlopen(url, timeout=timeout_time) as response:

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

def parse_xml(root):

    '''parses ALBINA-Style CAAML-XML. root is a ElementTree'''

    reports = []

    for bulletin in root.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}Bulletin'):
        report = AvaReport()
        for observations in bulletin:
            et_add_parent_info(observations)
            for locRef in observations.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}locRef'):
                report.valid_regions.append(observations.attrib.get('{http://www.w3.org/1999/xlink}href'))
            for locRef in observations.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}locRef'):
                report.valid_regions.append(observations.attrib.get('{http://www.w3.org/1999/xlink}href'))
            for dateTimeReport in observations.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}dateTimeReport'):
                report.rep_date = try_parse_datetime(dateTimeReport.text).replace(tzinfo=timezone.utc)
            for validTime in observations.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}validTime'):
                if not et_get_parent(validTime):
                    for beginPosition in observations.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}beginPosition'):
                        report.validity_begin = try_parse_datetime(beginPosition.text).replace(tzinfo=timezone.utc)
                    for endPosition in observations.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}endPosition'):
                        report.validity_end = try_parse_datetime(endPosition.text).replace(tzinfo=timezone.utc)
            for DangerRating in observations.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}DangerRating'):
                main_value = 0
                for mainValue in DangerRating.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}mainValue'):
                    main_value = int(mainValue.text)
                valid_elevation = "-"
                for validElevation in DangerRating.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}validElevation'):
                    valid_elevation = validElevation.attrib.get('{http://www.w3.org/1999/xlink}href')
                report.danger_main.append(DangerMain(main_value, valid_elevation))
            for DangerPattern in observations.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}DangerPattern'):
                for DangerPatternType in DangerPattern.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}type'):
                    report.dangerpattern.append(DangerPatternType.text)
            i = 0
            for AvProblem in observations.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}AvProblem'):
                type_r = ""
                for avProbType in AvProblem.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}type'):
                    type_r = avProbType.text
                aspect = []
                for validAspect in AvProblem.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}validAspect'):
                    aspect.append(validAspect.get('{http://www.w3.org/1999/xlink}href'))
                valid_elevation = "-"
                for validElevation in AvProblem.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}validElevation'):
                    valid_elevation = validElevation.get('{http://www.w3.org/1999/xlink}href')
                i = i+1
                report.problem_list.append(Problem(type_r, aspect, valid_elevation))
            for avActivityHighlights in observations.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}avActivityHighlights'):
                report.activity_hl = avActivityHighlights.text
            for avActivityComment in observations.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}avActivityComment'):
                report.activity_com = avActivityComment.text
            for snowpackStructureComment in observations.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}'\
                                                              'snowpackStructureComment'):
                report.snow_struct_com = snowpackStructureComment.text
            for tendencyComment in observations.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}tendencyComment'):
                report.tendency_com = tendencyComment.text
        reports.append(report)

    return reports

def parse_xml_vorarlberg(root):

    '''parses Vorarlberg-Style CAAML-XML. root is a ElementTree'''

    numberOfRegions = 6
    reports = []
    report = AvaReport()
    report.valid_regions = [""]
    comment_empty = 1
    # Common for every Report:
    for bulletin in root.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}Bulletin'):
        for detail in bulletin:
            for metaDataProperty in detail.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}metaDataProperty'):
                for dateTimeReport in metaDataProperty.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}dateTimeReport'):
                    report.rep_date = try_parse_datetime(dateTimeReport.text)
            for bulletinResultsOf in detail.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}bulletinResultsOf'):
                for travelAdvisoryComment in bulletinResultsOf.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}'\
                                                                    'travelAdvisoryComment'):
                    report.activity_com = travelAdvisoryComment.text
                for highlights in bulletinResultsOf.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}highlights'):
                    report.activity_hl = highlights.text
                for comment in bulletinResultsOf.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}comment'):
                    if comment_empty:
                        report.tendency_com = comment.text
                        comment_empty = 0
                for wxSynopsisComment in bulletinResultsOf.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}'\
                                                                'wxSynopsisComment'):
                    report.activity_com = report.activity_com + ' <br />Alpinwetterbericht der ZAMG Tirol und Vorarlberg:<br /> ' + str(wxSynopsisComment.text)
                for snowpackStructureComment in bulletinResultsOf.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}'\
                                                                       'snowpackStructureComment'):
                    report.snow_struct_com = snowpackStructureComment.text
                i = 0
                for AvProblem in detail.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}AvProblem'):
                    type_r = ""
                    for ac_problemt_type in AvProblem.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}type'):
                        type_r = ac_problemt_type.text
                    aspect = []
                    for validAspect in AvProblem.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}validAspect'):
                        aspect.append(validAspect.get('{http://www.w3.org/1999/xlink}href'))
                    valid_elevation = "-"
                    for validElevation in AvProblem.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}validElevation'):
                        for beginPosition in validElevation.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}beginPosition'):
                            valid_elevation = "ElevationRange_" + beginPosition.text + "Hi"
                        for endPosition in validElevation.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}endPosition'):
                            valid_elevation = "ElevationRange_" + endPosition.text + "Lw"
                    i = i+1
                    report.problem_list.append(Problem(type_r, aspect, valid_elevation))


    for i in range(numberOfRegions+1):
        reports.append(copy.deepcopy(report))

    # Individual for the Regions:
    for bulletin in root.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}Bulletin'):
        for detail in bulletin:
            for bulletinResultsOf in detail.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}bulletinResultsOf'):
                for DangerRating in bulletinResultsOf.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}DangerRating'):
                    region_id = 7
                    for locRef in DangerRating.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}locRef'):
                        region_id = int(locRef.attrib.get('{http://www.w3.org/1999/xlink}href')[-1])
                        reports[region_id-1].valid_regions[0] = locRef.attrib.get('{http://www.w3.org/1999/xlink}href')
                    for validTime in DangerRating.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}validTime'):
                        for beginPosition in validTime.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}beginPosition'):
                            reports[region_id-1].validity_begin = try_parse_datetime(beginPosition.text)
                        for endPosition in validTime.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}endPosition'):
                            reports[region_id-1].validity_end = try_parse_datetime(endPosition.text)
                    main_value = 0
                    valid_elevation = "-"
                    for main_value in DangerRating.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}mainValue'):
                        main_value = int(main_value.text)
                    for validElevation in DangerRating.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}validElevation'):
                        for beginPosition in validElevation.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}beginPosition'):
                            valid_elevation = "ElevationRange_" + beginPosition.text + "Hi"
                        for endPosition in validElevation.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}endPosition'):
                            valid_elevation = "ElevationRange_" + endPosition.text + "Lw"
                    reports[region_id-1].danger_main.append(DangerMain(main_value, valid_elevation))
    return reports


def parse_xml_bavaria(root):

    '''parses Bavarian-Style CAAML-XML. root is a ElementTree'''

    number_of_regions = 6
    reports = []
    report = AvaReport()
    report.valid_regions = [""]

    # Common for every Report:
    for metaData in root.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}metaDataProperty'):
        for dateTimeReport in metaData.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}dateTimeReport'):
            report.rep_date = try_parse_datetime(dateTimeReport.text)

    for bulletinMeasurements in root.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}BulletinMeasurements'):
        for travelAdvisoryComment in bulletinMeasurements.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}'\
                                                               'travelAdvisoryComment'):
            report.activity_com = travelAdvisoryComment.text
        for wxSynopsisComment in bulletinMeasurements.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}wxSynopsisComment'):
            report.activity_com = report.activity_com + ' <br />Deutscher Wetterdienst - Regionale Wetterberatung München:<br /> ' + str(wxSynopsisComment.text)
        for snowpackStructureComment in bulletinMeasurements.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}'\
                                                                  'snowpackStructureComment'):
            report.snow_struct_com = snowpackStructureComment.text
        for highlights in bulletinMeasurements.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}comment'):
            report.activity_hl = highlights.text
        i = 0
        for avProblem in bulletinMeasurements.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}avProblem'):
            type_r = ""
            for avType in avProblem.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}type'):
                type_r = avType.text
            aspect = []
            for validAspect in avProblem.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}validAspect'):
                aspect.append(validAspect.get('{http://www.w3.org/1999/xlink}href').lower())
            valid_elevation = "-"
            for validElevation in avProblem.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}validElevation'):
                for beginPosition in validElevation.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}beginPosition'):
                    valid_elevation = "ElevationRange_" + beginPosition.text + "Hi"
                for endPosition in validElevation.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}endPosition'):
                    valid_elevation = "ElevationRange_" + endPosition.text + "Lw"
            i = i+1
            report.problem_list.append(Problem(type_r, aspect, valid_elevation))

    for i in range(number_of_regions+1):
        reports.append(copy.deepcopy(report))

    # Check Names of all Regions
    for bulletinResultOf in root.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}bulletinResultsOf'):
        et_add_parent_info(bulletinResultOf)
        for locRef in bulletinResultOf.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}locRef'):
            found = False
            region_id = -1
            first_free = 100
            for index, report in enumerate(reports):
                if any(report.valid_regions):
                    for region in report.valid_regions:
                        if region == locRef.attrib.get('{http://www.w3.org/1999/xlink}href'):
                            found = True
                            region_id = index
                else:
                    if first_free > index:
                        first_free = index
            if not found:
                reports[first_free].valid_regions.append(locRef.attrib.get('{http://www.w3.org/1999/xlink}href'))
                region_id = first_free

            DangerRating = et_get_parent(locRef)

            for validTime in DangerRating.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}validTime'):
                for beginPosition in validTime.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}beginPosition'):
                    reports[region_id].validity_begin = try_parse_datetime(beginPosition.text)
                for endPosition in validTime.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}endPosition'):
                    reports[region_id].validity_end = try_parse_datetime(endPosition.text)
            main_value = 0
            valid_elevation = "-"
            for main_value in DangerRating.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}mainValue'):
                main_value = int(main_value.text)
            for validElevation in DangerRating.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}validElevation'):
                for beginPosition in validElevation.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}beginPosition'):
                    valid_elevation = "ElevationRange_" + beginPosition.text + "Hi"
                for endPosition in validElevation.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}endPosition'):
                    valid_elevation = "ElevationRange_" + endPosition.text + "Lw"
            reports[region_id].danger_main.append(DangerMain(main_value, valid_elevation))

    return reports

def get_reports(url):

    '''returns array of AvaReports for requested URL'''

    logging.info('Fetching %s', url)
    root = get_xml_as_et(url)
    if "VORARLBERG" in url.upper():
        reports = parse_xml_vorarlberg(root)
    elif "BAYERN" in url.upper():
        reports = parse_xml_bavaria(root)
    else:
        reports = parse_xml(root)
    return reports


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

    # Niederösterreich - Noch nicht angelegt
    if region_id.startswith("AT-03"):
        url = "https://www.avalanche-warnings.eu/public/niederoesterreich/caaml"
        provider = "Die dargestellten Informationen werden über eine API auf https://www.avalanche-warnings.eu abgefragt. Diese wird "\
            "bereitgestellt vom: Lawinenwarndienst Niederösterreich (https://www.lawinenwarndienst-niederoesterreich.at)."

    #Vorarlberg
    if region_id.startswith("AT8"):
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
        url = "https://conselharan2.cyberneticos.net/albina_files_local/latest/en.xml"
        provider = "The displayed ihe displayed information is provided by an open data API on https://lauegi.conselharan.org/ by: "\
            "Conselh Generau d'Aran - https://lauegi.conselharan.org/"
        if "DE" in local.upper():
            url = "https://conselharan2.cyberneticos.net/albina_files_local/latest/de.xml"
            provider = "Die dargestellten Informationen werden über eine API auf https://lauegi.conselharan.org/ abgefragt. "\
                "Diese wird bereitgestellt von Conselh Generau d'Aran (https://lauegi.conselharan.org/)."

    return url, provider

class Problem:
    type: str
    aspect: list
    valid_elevation: str

    def __init__(self, type: str, aspect: list, validElev: str) -> None:
        self.type = type
        self.aspect = aspect
        self.valid_elevation = validElev

    def __str__(self):
            return("{'type':'" + self.type + "', 'aspect':" + str(self.aspect) + ", 'valid_elevation':'" + self.valid_elevation + "'}")

    def __repr__(self):
        return str(self)

class DangerMain:
    main_value: int
    valid_elevation: str

    def __init__(self, mainValue: int, validElev: str):
        self.main_value = mainValue
        self.valid_elevation = validElev

class AvaReport:
    def __init__(self):
        self.valid_regions = []             # list of Regions
        self.rep_date = ""                  # Date of Report
        self.validity_begin = ""            # valid Ttime start
        self.validity_end = ""              # valid time end
        self.danger_main = []               # danger Value and elev
        self.dangerpattern = []             # list of Patterns
        self.problem_list = []              # list of Problems with Sublist of Aspect&Elevation
        self.activity_hl = "none"           # String avalanche activity highlits text
        self.activity_com = "none"          # String avalanche comment text
        self.snow_struct_com = "none"       # String comment on snowpack structure
        self.tendency_com = "none"          # String comment on tendency

def clean_elevation(elev: str):
    if elev in ['', '-', 'ElevationRange_Keine H\u00f6hengrenzeHi']:
        return None
    elev = re.sub(r'ElevationRange_(.+)Hi', r'>\1', elev)
    elev = re.sub(r'ElevationRange_(.+)(Lo|Lw)', r'<\1', elev)
    elev = elev.replace('Forestline', 'Treeline')
    return elev

def dumper(obj):
    if type(obj) is datetime:
        return obj.isoformat()
    try:
        return obj.toJSON()
    except:
        return obj.__dict__

def download_region(regionID):
    url, _ = get_report_url(regionID)
    reports = get_reports(url)
    report: AvaReport
    for report in reports:
        if type(report.validity_begin) is datetime:
            validityDate = report.validity_begin
            if validityDate.hour > 15:
                validityDate = validityDate + timedelta(days=1)
            validityDate = validityDate.date().isoformat()
        report.activity_hl = None
        report.activity_com = None
        report.snow_struct_com = None
        report.tendency_com = None
        report.valid_regions = [r.replace('AT8R', 'AT-08-0') for r in report.valid_regions]
        for danger in report.danger_main:
            danger.valid_elevation = clean_elevation(danger.valid_elevation)
        for problem in report.problem_list:
            problem.valid_elevation = clean_elevation(problem.valid_elevation)
            problem.aspect = [a.upper().replace('ASPECTRANGE_', '') for a in problem.aspect]

    directory = Path(sys.argv[1] if len(sys.argv) > 1 else '.')
    with urlopen(url) as http, open(f'{directory}/{validityDate}-{regionID}.xml', mode='wb') as f:
        logging.info('Writing %s to %s', url, f.name)
        f.write(http.read())
    with open(f'{directory}/{validityDate}-{regionID}.json', mode='w', encoding='utf-8') as f:
        logging.info('Writing %s', f.name)
        json.dump(reports, fp=f, default=dumper, indent=2)

def cli_print_report(matching_report, provider, cached):

    '''Displays report details on CLI'''

    try:
        matching_report
    except NameError:
        print('dangerLevel', "Problem resolving Region")
        print('provider', "Couldn't find the RegionID in the Report. Probably it is not served at the moment.")

        print('finished')
    else:

        dangerLevel = 0
        for elem in matching_report.danger_main:
            if elem.main_value > dangerLevel:
                dangerLevel = elem.main_value

        print('dangerLevel', dangerLevel)
        print('dangerLevel_h', matching_report.danger_main[0].main_value)
        if len(matching_report.danger_main) > 1:
            print('dangerLevel_l', matching_report.danger_main[1].main_value)
            print('dangerLevel_alti', matching_report.danger_main[0].valid_elevation)
        else:
            print('dangerLevel_l', matching_report.danger_main[0].main_value)
        print('highlights', matching_report.activity_hl)
        print('comment', matching_report.activity_com)
        print('structure', matching_report.snow_struct_com)
        print('tendency', matching_report.tendency_com)
        print('repDate', matching_report.rep_date)
        print('validFrom', matching_report.validity_begin.isoformat())
        print('validTo', matching_report.validity_end)
        print('numberOfDPatterns', len(matching_report.problem_list))
        print('dPatterns', str(matching_report.problem_list))
        print('provider', provider)

        print('finished')

        print(matching_report.valid_regions)

if __name__ == "__main__":
    regions = ["AT-02", "AT-03", "AT-04", "AT-05", "AT-06", "AT-08", "BY"]
    for regionID in regions:
        try:
            download_region(regionID)
        except Exception as e:
            logging.error('Failed to download %s', regionID, exc_info=e)
