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
import pytz
import dateutil.parser
import urllib.request
import copy
import logging
import re
import string

from avacore import pyAvaCore
from avacore.avabulletin import AvaBulletin, DangerRatingType, AvalancheProblemType, RegionType

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
    logging.info('Fetching %s', req.full_url)
    response_content = urlopen(req).read()

    try:
        root = ET.fromstring(response_content.decode('utf-8'))
    except Exception as r_e:
        print('error parsing ElementTree: ' + str(r_e))

    return root

def process_all_reports_fr():
    all_reports = []
    for region in fr_regions:
        reports = process_reports_fr(region)
        for report in reports:
            all_reports.append(report)
    return all_reports

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

    report = AvaBulletin()
    reports = []

    report.regions.append(RegionType('FR-' + root.attrib.get('ID').zfill(2)))
    report.publicationTime = pytz.timezone("Europe/Paris").localize(dateutil.parser.parse(root.attrib.get('DATEBULLETIN')))
    report.validTime.startTime = pytz.timezone("Europe/Paris").localize(dateutil.parser.parse(root.attrib.get('DATEBULLETIN')))
    report.validTime.endTime = pytz.timezone("Europe/Paris").localize(dateutil.parser.parse(root.attrib.get('DATEVALIDITE')))
    
    

    for cartoucherisque in root.iter(tag='CARTOUCHERISQUE'):
        
        danger_rating_pre = DangerRatingType()
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

        # general_problem_valid_elevation = '-'
        # report.problem_list.append(pyAvaCore.Problem("general", aspects, general_problem_valid_elevation))
        danger_rating_pre.aspect = aspects

        for risque in cartoucherisque.iter(tag='RISQUE'):
            # report.danger_main.append(pyAvaCore.DangerMain(int(risque.attrib.get('RISQUE1')), risque.attrib.get('LOC1')))
            danger_rating = copy.deepcopy(danger_rating_pre)
            danger_rating.set_mainValue_int(int(risque.attrib.get('RISQUE1')))
            danger_rating.elevation.auto_select(risque.attrib.get('LOC1'))
            report.dangerRatings.append(danger_rating)
            if not risque.attrib.get('RISQUE2') == '':
                #report.danger_main.append(pyAvaCore.DangerMain(int(risque.attrib.get('RISQUE2')), risque.attrib.get('LOC2')))
                danger_rating2 = copy.deepcopy(danger_rating_pre)
                danger_rating2.set_mainValue_int(int(risque.attrib.get('RISQUE2')))
                danger_rating2.elevation.auto_select(risque.attrib.get('LOC2'))
                report.dangerRatings.append(danger_rating2)

        for resume in cartoucherisque.iter(tag='RESUME'):
            report.avalancheActivityHighlights = resume.text

    for stabilite in root.iter(tag='STABILITE'):
        for texte in stabilite.iter(tag='TEXTE'):
            report.avalancheActivityComment = texte.text

    for qualite in root.iter(tag='QUALITE'):
        for texte in qualite.iter(tag='TEXTE'):
            report.snowpackStructureComment = texte.text

    pm_danger_ratings = []
    pm_available = False

    for cartoucherisque in root.iter(tag='CARTOUCHERISQUE'):
        
        danger_rating_pre = DangerRatingType()
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

        # general_problem_valid_elevation = '-'
        # report.problem_list.append(pyAvaCore.Problem("general", aspects, general_problem_valid_elevation))
        danger_rating_pre.aspect = aspects
        
        for risque in cartoucherisque.iter(tag='RISQUE'):
            if not risque.attrib.get('EVOLURISQUE1') == '':
                pm_available = True
                danger_rating_pm = copy.deepcopy(danger_rating_pre)
                danger_rating_pm.set_mainValue_int(int(risque.attrib.get('EVOLURISQUE1')))
                danger_rating_pm.elevation.auto_select(risque.attrib.get('LOC1'))
                pm_danger_ratings.append(danger_rating_pm)
                # pm_danger_ratings.append(pyAvaCore.DangerMain(int(risque.attrib.get('EVOLURISQUE1')), risque.attrib.get('LOC1')))
            else:
                pm_danger_ratings.append(report.dangerRatings[0])
            if not risque.attrib.get('EVOLURISQUE2') == '':
                pm_available = True
                danger_rating_pm2 = copy.deepcopy(danger_rating_pre)
                danger_rating_pm2.set_mainValue_int(int(risque.attrib.get('EVOLURISQUE2')))
                danger_rating_pm2.elevation.auto_select(risque.attrib.get('LOC2'))
                pm_danger_ratings.append(danger_rating_pm2)
            elif len(report.dangerRatings) > 1:
                pm_danger_ratings.append(report.dangerRatings[1])

    report.bulletinID = report.regions[0].regionID + '_' + str(report.publicationTime.isoformat())

    if pm_available:
        pm_report = copy.deepcopy(report)
        pm_report.predecessor_id = pm_report.bulletinID
        pm_report.bulletinID += '_PM'
        report.validTime.endTime = report.validTime.endTime.replace(hour=12)
        pm_report.validTime.startTime = report.validTime.endTime.replace(hour=12)
        pm_report.dangerRatings = pm_danger_ratings

        reports.append(pm_report)

    reports.append(report)

    return reports

fr_regions = [
    "FR-01",
    "FR-02",
    "FR-03",
    "FR-04",
    "FR-05",
    "FR-06",
    "FR-09",
    "FR-10",
    "FR-11",
    "FR-07",
    "FR-08",
    "FR-12",
    "FR-14",
    "FR-15",
    "FR-13",
    "FR-16",
    "FR-17",
    "FR-18",
    "FR-19",
    "FR-20",
    "FR-21",
    "FR-22",
    "FR-23",
    "FR-64",
    "FR-65",
    "FR-66",
    "FR-67",
    "FR-68",
    "FR-69",
    "FR-70",
    "FR-72",
    "FR-71",
    "FR-73",
    "FR-74",
    "FR-40",
    "FR-41",
]
