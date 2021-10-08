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
from urllib.request import urlopen, Request
import urllib.request
import copy
import re
import string

from avacore import pyAvaCore

def download_report_fr(region_id):
    try:
        import xml.etree.cElementTree as ET
    except ImportError:
        import xml.etree.ElementTree as ET

    response = urllib.request.urlopen('https://meteofrance.com/')
    headers = response.getheaders()
    session_cookie_raw = response.getheader('Set-Cookie')
    session_cookie = re.sub('mfsession=', '', session_cookie_raw.split(';')[0])

    access_token = ''
    shift_by = 13
    for c in session_cookie:
        if c.isdigit() or c in string.punctuation:
            access_token += c
        else:
            c_a = 'A' if c.isupper() else 'a'
            index = ord(c) - ord(c_a)
            access_token += (chr(ord(c_a) + (index + shift_by) % 26))

    req = Request('https://rpcache-aa.meteofrance.com/internet2018client/2.0/report?domain=' + re.sub('FR-', '', region_id) +  \
                '&report_type=Forecast&report_subtype=BRA')
    req.add_header('Authorization', 'Bearer ' + access_token)
    response_content = urlopen(req).read()

    try:
        root = ET.fromstring(response_content.decode('utf-8'))
    except Exception as r_e:
        print('error parsing ElementTree: ' + str(r_e))

    return root

def process_reports_fr(region_id, path='', cached=False):
    '''
    Download report for specified france region
    '''
    try:
        import xml.etree.cElementTree as ET
    except ImportError:
        import xml.etree.ElementTree as ET

    if not cached:
        root = download_report_fr(region_id)

    else:
        m_root = ET.parse(path)
        for bulletins in m_root.iter(tag='BULLETINS_NEIGE_AVALANCHE'):
            root = bulletins

    report = pyAvaCore.AvaReport()
    reports = []

    report.valid_regions.append('FR-' + root.attrib.get('ID').zfill(2))
    report.rep_date = pyAvaCore.try_parse_datetime(root.attrib.get('DATEBULLETIN')+'+01:00')
    report.validity_begin = pyAvaCore.try_parse_datetime(root.attrib.get('DATEBULLETIN')+'+01:00')
    report.validity_end = pyAvaCore.try_parse_datetime(root.attrib.get('DATEVALIDITE')+'+01:00')

    for cartoucherisque in root.iter(tag='CARTOUCHERISQUE'):
        for risque in cartoucherisque.iter(tag='RISQUE'):
            report.danger_main.append(pyAvaCore.DangerMain(int(risque.attrib.get('RISQUE1')), risque.attrib.get('LOC1')))
            if not risque.attrib.get('RISQUE2') == '':
                report.danger_main.append(pyAvaCore.DangerMain(int(risque.attrib.get('RISQUE2')), risque.attrib.get('LOC2')))


        aspects = []
        for pente in cartoucherisque.iter(tag='PENTE'):

            if pente.get('N') == 'true':
                aspects.append('N')
            if pente.get('NE') == 'true':
                aspects.append('NE')
            if pente.get('E') == 'true':
                aspects.append('E')
            if pente.get('SE') == 'true':
                aspects.append('SE')
            if pente.get('S') == 'true':
                aspects.append('S')
            if pente.get('SW') == 'true':
                aspects.append('SW')
            if pente.get('W') == 'true':
                aspects.append('W')
            if pente.get('NW') == 'true':
                aspects.append('NW')

        general_problem_valid_elevation = '-'
        report.problem_list.append(pyAvaCore.Problem("general", aspects, general_problem_valid_elevation))

        for resume in cartoucherisque.iter(tag='RESUME'):
            report.report_texts.append(pyAvaCore.ReportText('activity_hl', resume.text))

    for stabilite in root.iter(tag='STABILITE'):
        for texte in stabilite.iter(tag='TEXTE'):
            report.report_texts.append(pyAvaCore.ReportText('activity_com', texte.text))

    for qualite in root.iter(tag='QUALITE'):
        for texte in qualite.iter(tag='TEXTE'):
            report.report_texts.append(pyAvaCore.ReportText('snow_struct_com', texte.text))

    pm_danger_ratings = []
    pm_available = False

    for cartoucherisque in root.iter(tag='CARTOUCHERISQUE'):
        for risque in cartoucherisque.iter(tag='RISQUE'):
            if not risque.attrib.get('EVOLURISQUE1') == '':
                pm_available = True
                pm_danger_ratings.append(pyAvaCore.DangerMain(int(risque.attrib.get('EVOLURISQUE1')), risque.attrib.get('LOC1')))
            else:
                pm_danger_ratings.append(report.danger_main[0])
            if not risque.attrib.get('EVOLURISQUE2') == '':
                pm_available = True
                pm_danger_ratings.append(pyAvaCore.DangerMain(int(risque.attrib.get('EVOLURISQUE2')), risque.attrib.get('LOC2')))
            elif len(report.danger_main) > 1:
                pm_danger_ratings.append(report.danger_main[1])

    report.report_id = report.valid_regions[0] + '_' + str(report.rep_date.isoformat())

    if pm_available:
        pm_report = copy.deepcopy(report)
        pm_report.predecessor_id = pm_report.report_id
        pm_report.report_id += '_PM'
        report.validity_end = report.validity_end.replace(hour=12)
        pm_report.validity_begin = report.validity_end.replace(hour=12)
        pm_report.danger_main = pm_danger_ratings

        reports.append(pm_report)

    reports.append(report)

    return reports
