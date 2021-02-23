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
from datetime import timezone
from datetime import time
from urllib.request import urlopen
from pathlib import Path
import urllib.request
import zipfile
import copy
import re
import base64
import json
import logging

from avacore.png import png

### ElementTree helpers

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

### XML-Parsers

def parse_xml(root):

    '''parses ALBINA-Style CAAML-XML. root is a ElementTree'''

    reports = []

    for bulletin in root.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}Bulletin'):
        report = AvaReport()
        report.report_id = bulletin.attrib.get('{http://www.opengis.net/gml}id')
        for observations in bulletin:
            et_add_parent_info(observations)
            for locRef in observations.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}locRef'):
                loc_ref = observations.attrib.get('{http://www.w3.org/1999/xlink}href')
                if loc_ref not in report.valid_regions:
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
            for AvProblem in observations.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}AvProblem'):
                type_r = ""
                for avProbType in AvProblem.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}type'):
                    type_r = avProbType.text
                aspect = []
                for validAspect in AvProblem.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}validAspect'):
                    aspect.append(validAspect.get('{http://www.w3.org/1999/xlink}href').upper().replace('ASPECTRANGE_', ''))
                valid_elevation = "-"
                for validElevation in AvProblem.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}validElevation'):
                    valid_elevation = validElevation.get('{http://www.w3.org/1999/xlink}href')
                report.problem_list.append(Problem(type_r, aspect, valid_elevation))
            for avActivityHighlights in observations.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}avActivityHighlights'):
                report.report_texts.append(ReportText('activity_hl', avActivityHighlights.text))
            for avActivityComment in observations.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}avActivityComment'):
                report.report_texts.append(ReportText('activity_com', avActivityComment.text))
            for snowpackStructureComment in observations.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}'\
                                                              'snowpackStructureComment'):
                report.report_texts.append(ReportText('snow_struct_com', snowpackStructureComment.text))
            for tendencyComment in observations.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}tendencyComment'):
                report.report_texts.append(ReportText('tendency_com', tendencyComment.text))
        reports.append(report)

    for report in reports:
        if report.report_id.endswith('_PM') and any(x.report_id == report.report_id[:-3] for x in reports):
            report.predecessor_id = report.report_id[:-3]

    return reports

def parse_xml_vorarlberg(root):

    '''parses Vorarlberg-Style CAAML-XML. root is a ElementTree'''

    numberOfRegions = 6
    reports = []
    report = AvaReport()
    report.valid_regions = [""]
    comment_empty = 1
    # Common for every Report:
    activity_com = ""
    for bulletin in root.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}Bulletin'):
        for detail in bulletin:
            for metaDataProperty in detail.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}metaDataProperty'):
                for dateTimeReport in metaDataProperty.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}dateTimeReport'):
                    report.rep_date = try_parse_datetime(dateTimeReport.text)
            for bulletinResultsOf in detail.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}bulletinResultsOf'):
                for travelAdvisoryComment in bulletinResultsOf.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}'\
                                                                    'travelAdvisoryComment'):
                    activity_com = travelAdvisoryComment.text
                for highlights in bulletinResultsOf.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}highlights'):
                    report.report_texts.append(ReportText('activity_hl', highlights.text))
                for comment in bulletinResultsOf.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}comment'):
                    if comment_empty:
                        report.report_texts.append(ReportText('tendency_com', comment.text))
                        comment_empty = 0
                for wxSynopsisComment in bulletinResultsOf.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}'\
                                                                'wxSynopsisComment'):
                    activity_com = activity_com + ' <br />Alpinwetterbericht der ZAMG Tirol und Vorarlberg:<br /> ' \
                        + str(wxSynopsisComment.text)
                for snowpackStructureComment in bulletinResultsOf.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}'\
                                                                       'snowpackStructureComment'):
                    report.report_texts.append(ReportText('snow_struct_com', snowpackStructureComment.text))
                for AvProblem in detail.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}AvProblem'):
                    type_r = ""
                    for ac_problemt_type in AvProblem.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}type'):
                        type_r = ac_problemt_type.text
                    aspect = []
                    for validAspect in AvProblem.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}validAspect'):
                        aspect.append(validAspect.get('{http://www.w3.org/1999/xlink}href').upper().replace(\
                            'ASPECTRANGE_', '').replace('O', 'E'))
                    valid_elevation = "-"
                    for validElevation in AvProblem.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}validElevation'):
                        for beginPosition in validElevation.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}beginPosition'):
                            valid_elevation = ">" + beginPosition.text
                        for endPosition in validElevation.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}endPosition'):
                            valid_elevation = "<" + endPosition.text
                    report.problem_list.append(Problem(type_r, aspect, valid_elevation))

    report.report_texts.append(ReportText('activity_com', activity_com))

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
                            valid_elevation = ">" + beginPosition.text
                        for endPosition in validElevation.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}endPosition'):
                            valid_elevation = "<" + endPosition.text
                    reports[region_id-1].danger_main.append(DangerMain(main_value, valid_elevation))
    return reports


def parse_xml_bavaria(root):

    '''parses Bavarian-Style CAAML-XML. root is a ElementTree'''

    number_of_regions = 6
    reports = []
    report = AvaReport()

    report_id = ''
    for bulletin in root.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}Bulletin'):
        report_id = bulletin.attrib.get('{http://www.opengis.net/gml}id')

    # Common for every Report:
    for metaData in root.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}metaDataProperty'):
        for dateTimeReport in metaData.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}dateTimeReport'):
            report.rep_date = try_parse_datetime(dateTimeReport.text)

    activity_com = ''

    for bulletinMeasurements in root.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}BulletinMeasurements'):
        for travelAdvisoryComment in bulletinMeasurements.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}'\
                                                               'travelAdvisoryComment'):
            activity_com = travelAdvisoryComment.text

        for wxSynopsisComment in bulletinMeasurements.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}wxSynopsisComment'):
            activity_com = activity_com + ' <br />Deutscher Wetterdienst - Regionale Wetterberatung München:<br /> ' \
                + str(wxSynopsisComment.text)
        for snowpackStructureComment in bulletinMeasurements.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}'\
                                                                  'snowpackStructureComment'):
            report.report_texts.append(ReportText('snow_struct_com', snowpackStructureComment.text))
        for highlights in bulletinMeasurements.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}comment'):
            report.report_texts.append(ReportText('activity_hl', highlights.text))
        for avProblem in bulletinMeasurements.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}avProblem'):
            type_r = ""
            for avType in avProblem.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}type'):
                type_r = avType.text
            aspect = []
            for validAspect in avProblem.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}validAspect'):
                aspect.append(validAspect.get('{http://www.w3.org/1999/xlink}href').upper().replace('ASPECTRANGE_', ''))
            valid_elevation = "-"
            for validElevation in avProblem.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}validElevation'):
                for beginPosition in validElevation.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}beginPosition'):
                    if not 'Keine' in beginPosition.text:
                        valid_elevation = ">" + beginPosition.text
                for endPosition in validElevation.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}endPosition'):
                    if not 'Keine' in endPosition.text:
                        valid_elevation = "<" + endPosition.text
            report.problem_list.append(Problem(type_r, aspect, valid_elevation))

    report.report_texts.append(ReportText('activity_com', activity_com))

    for bulletinResultOf in root.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}bulletinResultsOf'):
        et_add_parent_info(bulletinResultOf)

        loc_list = []

        for locRef in bulletinResultOf.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}locRef'):
            current_loc_ref = locRef.attrib.get('{http://www.w3.org/1999/xlink}href')

            DangerRating = et_get_parent(locRef)
            validity_begin = ""
            validity_end = ""
            main_value = 0
            valid_elevation = "-"

            for validTime in DangerRating.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}validTime'):
                for beginPosition in validTime.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}beginPosition'):
                    validity_begin = try_parse_datetime(beginPosition.text)
                for endPosition in validTime.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}endPosition'):
                    validity_end = try_parse_datetime(endPosition.text)
            main_value = 0
            for main_value in DangerRating.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}mainValue'):
                main_value = int(main_value.text)
            for validElevation in DangerRating.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}validElevation'):
                for beginPosition in validElevation.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}beginPosition'):
                    if not 'Keine' in beginPosition.text:
                        valid_elevation = ">" + beginPosition.text
                for endPosition in validElevation.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}endPosition'):
                    if not 'Keine' in endPosition.text:
                        valid_elevation = "<" + endPosition.text

            loc_list.append([current_loc_ref, validity_begin, validity_end, DangerMain(main_value, valid_elevation)])

    loc_ref_list = []
    del_index = []

    for index, loc_elem in enumerate(loc_list):
        if loc_elem[1].time() == time(0, 0, 0):
            if not any(loc_elem[0] in loc_ref for loc_ref in loc_ref_list):
                c_report = copy.deepcopy(report)
                c_report.valid_regions.append(loc_elem[0])
                c_report.report_id = report_id + '-' + loc_elem[0]
                c_report.validity_begin = loc_elem[1]
                c_report.validity_end = loc_elem[2]
                c_report.danger_main.append(loc_elem[3])
                loc_ref_list.append(loc_elem[0])
                reports.append(c_report)
                del_index.append(index)

    loc_list = [i for j, i in enumerate(loc_list) if j not in del_index]
    del_index = []

    for index, loc_elem in enumerate(loc_list):
        if loc_elem[1].time() == time(0, 0, 0):
            report_elem_number = loc_ref_list.index(loc_elem[0])
            if reports[report_elem_number].validity_end > loc_elem[2]:
                reports[report_elem_number].validity_end = loc_elem[2]
            if not (reports[report_elem_number].danger_main[0].main_value == loc_elem[3].main_value and \
                    reports[report_elem_number].danger_main[0].valid_elevation == loc_elem[3].valid_elevation):
                reports[report_elem_number].danger_main.append(loc_elem[3])
            del_index.append(index)

    loc_list = [i for j, i in enumerate(loc_list) if j not in del_index]
    del_index = []

    for index, loc_elem in enumerate(loc_list):
        if not any((loc_elem[0] + '_PM') in loc_ref for loc_ref in loc_ref_list):
            report_elem_number = loc_ref_list.index(loc_elem[0])
            c_report = copy.deepcopy(reports[report_elem_number])
            loc_ref_list.append(loc_elem[0] + '_PM')

            c_report.valid_regions.append(loc_elem[0])
            c_report.report_id = report_id + '-' + loc_elem[0] + '_PM'
            c_report.validity_begin = loc_elem[1]
            c_report.validity_end = loc_elem[2]
            c_report.predecessor_id = report_id + '-' + loc_elem[0]
            for danger_main in c_report.danger_main:
                if danger_main.valid_elevation == loc_elem[3].valid_elevation:
                    danger_main.main_value = loc_elem[3].main_value
            reports.append(c_report)
            del_index.append(index)

    loc_list = [i for j, i in enumerate(loc_list) if j not in del_index]
    del_index = []

    for index, loc_elem in enumerate(loc_list):
        report_elem_number = loc_ref_list.index(loc_elem[0] + '_PM')
        for danger_main in reports[report_elem_number].danger_main:
            if danger_main.valid_elevation == loc_elem[3].valid_elevation:
                danger_main.main_value = loc_elem[3].main_value

    return reports

### XML-Helpers

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
        url = "https://conselharan2.cyberneticos.net/albina_files_local/latest/en.xml"
        provider = "The displayed ihe displayed information is provided by an open data API on https://lauegi.conselharan.org/ by: "\
            "Conselh Generau d'Aran - https://lauegi.conselharan.org/"
        if "DE" in local.upper():
            url = "https://conselharan2.cyberneticos.net/albina_files_local/latest/de.xml"
            provider = "Die dargestellten Informationen werden über eine API auf https://lauegi.conselharan.org/ abgefragt. "\
                "Diese wird bereitgestellt von Conselh Generau d'Aran (https://lauegi.conselharan.org/)."

    return url, provider

### CH Helpers and Parsers

def fetch_files_ch(lang, path):
    '''
    Downloads the swiss avalanche zip for the slf app together with the region mapping information
    '''
    Path(path + '/swiss/').mkdir(parents=True, exist_ok=True)
    url = 'https://www.slf.ch/avalanche/mobile/bulletin_'+lang+'.zip'
    urllib.request.urlretrieve(url, path + '/swiss/bulletin_'+lang+'.zip')

    urllib.request.urlretrieve('https://www.slf.ch/avalanche/bulletin/'+lang+'/gk_region2pdf.txt', path + '/swiss/gk_region2pdf.txt')

    with zipfile.ZipFile(path + '/swiss/bulletin_'+lang+'.zip', 'r') as zip_ref:
        zip_ref.extractall(path + '/swiss/')


def get_prone_locations(img_text):
    '''
    Extract dangerous aspects from png
    '''
    imgdata = base64.b64decode(img_text)
    png_data = png.Reader(bytes=imgdata)

    _, _, px, _ = png_data.read()

    px_list = list(px)

    aspects = []

    if px_list[20][129] == 0:
        aspects.append('NNE')
    if px_list[25][145] == 0:
        aspects.append('ENE')
    if px_list[31][145] == 0:
        aspects.append('ESE')
    if px_list[36][129] == 0:
        aspects.append('SSE')
    if px_list[36][101] == 0:
        aspects.append('SSW')
    if px_list[31][77] == 0:
        aspects.append('WSW')
    if px_list[25][77] == 0:
        aspects.append('WNW')
    if px_list[20][101] == 0:
        aspects.append('NNW')

    return aspects

def get_reports_ch(path, lang="en", cached=False):
    '''
    Download the reports for CH
    '''
    if not cached:
        fetch_files_ch(lang, path)

    if Path(path + '/swiss/gk_region2pdf.txt').is_file():

        # Receives validity information from text.json
        with open(path + '/swiss/text.json') as fp:
            data = json.load(fp)

        # region_id = region_id[-4:]

        common_report = AvaReport()

        begin, end = data['validity'].split('/')

        date_time_now = datetime.now()

        common_report.rep_date = datetime.strptime(str(date_time_now.year) + '-' + begin[begin.find(':')+2:-1], '%Y-%d.%m., %H:%M')
        common_report.validity_begin = common_report.rep_date
        # Achtung: validity_end is here the next expected update. It should be valid sometimes longer than that.
        # (5PM repot up to 5PM next day)
        common_report.validity_end = datetime.strptime(str(date_time_now.year) + '-' + end[end.find(':')+2:], '%Y-%d.%m., %H:%M')

        report_ids = []
        reports = []

        # Receives the ID of the report that matches the selected region_id
        with open(path + '/swiss/gk_region2pdf.txt') as fp:
            for line in fp:
                report_id = line.split('_')[5][:-5]
                report_id_pm = None
                if len(report_id) > 7:
                    report_id_pm = report_id[7:]
                    report_id = report_id[:7]
                if report_id not in report_ids:
                    report_ids.append(report_id)
                    new_report = copy.deepcopy(common_report)
                    new_report.report_id = report_id
                    reports.append(new_report)
                if not report_id_pm is None and report_id_pm not in report_ids:
                    report_ids.append(report_id_pm)
                    new_report = copy.deepcopy(common_report)
                    new_report.report_id = report_id_pm
                    new_report.predecessor_id = report_id
                    reports.append(new_report)
                elif not report_id_pm is None:
                    if not report_id in reports[report_ids.index(report_id_pm)].predecessor_id:
                        reports[report_ids.index(report_id_pm)].predecessor_id += ('_' + report_id)
                reports[report_ids.index(report_id)].valid_regions.append("CH-" + line[:4])
                reports[report_ids.index(report_id_pm)].valid_regions.append("CH-" + line[:4])

        for report in reports:
            # Opens the matching Report-File
            folder = '1'
            if hasattr(report, 'predecessor_id'):
                folder = '2'

            with open(path + '/swiss/'+folder+'/dst' + report.report_id + '.html', encoding="utf-8") as f:
                text = f.read()

            # Isolates the relevant Danger Information
            text_pos = text.find('data-level=')+len('data-level=')+1
            report.danger_main.append(DangerMain(int(text[text_pos:text_pos+1]), '-'))

            # Isolates the prone location Image
            text_pos = text.find('src="data:image/png;base64,')+len('src="data:image/png;base64,')
            subtext = text[text_pos:]
            prone_locations_img = ReportText('prone_locations_img')
            prone_locations_img.text_content = subtext[:subtext.find('"')]
            general_problem_locations = ''
            if len(prone_locations_img.text_content) < 1000: # Sometimes no Picture is attached
                prone_locations_img.text_content = '-'
            else:
                general_problem_locations = get_prone_locations(prone_locations_img.text_content)
            report.report_texts.append(prone_locations_img)

            # Isolates the prone location Text
            text_pos = subtext.find('alt="')+len('alt="')
            subtext = subtext[text_pos:]
            prone_locations_text = ReportText('prone_locations_text')
            prone_locations_text.text_content = subtext[:subtext.find('"')]
            general_problem_valid_elevation = "-"
            if prone_locations_text.text_content == 'Content-Type':
                prone_locations_text.text_content = '-'
            else:
                valid_elevation = ''.join(c for c in prone_locations_text.text_content if c.isdigit())
                general_problem_valid_elevation = ">" + valid_elevation

            report.report_texts.append(prone_locations_text)
            report.problem_list.append(Problem("general", general_problem_locations, general_problem_valid_elevation))

            # Remove Image from html, sometimes no Picture is attached
            html_report_local = ReportText('html_report_local')
            try:
                split1 = text.split('<img')
                split2 = split1[1].split('">')
                html_report_local.text_content = split1[0]+'"'.join(split2[1:])

            except:
                html_report_local.text_content = text
            report.report_texts.append(html_report_local)

            # Retreives the Weather and Snow Information
            text = ""
            with open(path + '/swiss/sdwetter.html', encoding="utf-8") as f:
                text = f.read()

            html_weather_snow = ReportText('html_weather_snow')
            html_weather_snow.text_content = text
            report.report_texts.append(html_weather_snow)

    return reports

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
    def __init__(self):
        self.report_id = ""                 # ID of the Report
        self.valid_regions = []             # list of Regions
        self.rep_date = ""                  # Date of Report
        self.validity_begin = ""            # valid Ttime start
        self.validity_end = ""              # valid time end
        str: self.predecessor_id = None     # ID of first report (AM) if Report is e. g. a PM-Report
        self.danger_main = []               # danger Value and elev
        self.dangerpattern = []             # list of Patterns
        self.problem_list = []              # list of Problems with Sublist of Aspect&Elevation
        self.report_texts = []              # All textual elements of the Report


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
