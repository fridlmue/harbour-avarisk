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
import json
import urllib.request
from datetime import datetime
from datetime import time
from datetime import timedelta
from pathlib import Path
import pytz
import dateutil.parser
import logging
import logging.handlers

from avacore import pyAvaCore
from avacore.avabulletin import AvaBulletin, DangerRatingType, AvalancheProblemType, AvaCoreCustom, ElevationType, RegionType

Path('logs').mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    format='[%(asctime)s] {%(module)s:%(lineno)d} %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.handlers.TimedRotatingFileHandler(filename='logs/pyAvaCore.log', when='midnight'),
        logging.StreamHandler()])


def process_reports_it(region_id, today=datetime.now(pytz.timezone('Europe/Rome'))):
    
    '''
    if today == datetime(1, 1, 1, 1, 1, 1):
        now = datetime.now(pytz.timezone('Europe/Rome'))
        if now.time() > time(17, 0, 1):
            today = now.date() + timedelta(days=1)
        else:
            today = now.date()
    '''
    
    reports = []
    report = pyAvaCore.AvaBulletin()

    format = 0
    pm_available = False
    valid_report = True

    old = False

    p_code, p_zona = it_region_ref[region_id]
    p_giorno = '1'
    
    now = datetime.now(pytz.timezone('Europe/Rome'))
    if now.time() > time(16, 0, 0):
        p_giorno = '3'

    url = "https://services.aineva.it/Aineva_bollettini/NivoMeteo/ServiziNivo.asmx/getZonePrevisioni?pGiorno='" + p_giorno + "'&pIdZona='" \
        + str(p_zona) + "'&pCode='" + p_code + "'&pIdBollettino=''"

    headers = {
        "Content-Type": "application/json; charset=utf-8"
        }

    req = urllib.request.Request(url, headers=headers)

    with urllib.request.urlopen(req) as response:
        content = response.read()

    aineva_object = json.loads(content)
    all_text = aineva_object['d']
    details_1x = all_text.split('£')
    details_10 = details_1x[0].split('|')
    details_11 = details_1x[1].split('|')
    details_12 = details_1x[2].split('|')

    report.publicationTime = date_from_report(details_1x[9])
    report.regions.append(RegionType(region_id))

    report.bulletinID = region_id + '_' + today.isoformat()
    
    if p_giorno == '1':
        report.validTime.startTime = datetime.combine(today, time(17,0)) - timedelta(hours=24)
    else:
        report.validTime.startTime = datetime.combine(today, time(17,0))
    report.validTime.endTime =  report.validTime.startTime + timedelta(hours=24)
    
    danger_rating = DangerRatingType()

    if int(details_10[0][3]) < 6:
        danger_rating.set_mainValue_int(int(details_10[0][3]))
        # danger_rating.elevation.auto_select(valid_elevation)
        # report.danger_main.append(pyAvaCore.DangerMain(int(details_10[0][3]), '-'))

    prefix_alti = ''

    if int(details_10[2][3]) in [1, 2, 3]:
        prefix_alti = '>'
    if int(details_10[2][3]) == 4:
        prefix_alti = '<'
    elev_data = details_11[2]
    if prefix_alti != '' and len(elev_data) < 20:
        aspects = []
        general_problem_valid_elevation = ''.join(c for c in elev_data.split('/')[0].split('-')[0] if c.isdigit())
        # ToDo Aspects are missing at the moment
        # report.problem_list.append(pyAvaCore.Problem("general", aspects, prefix_alti + general_problem_valid_elevation))
        danger_rating.elevation.auto_select(prefix_alti + general_problem_valid_elevation)
        
    report.dangerRatings.append(danger_rating)

    av_problem = details_10[3][5:-4].lower()
    if av_problem != '':
        #report.problem_list.append(av_problem)
        problem = AvalancheProblemType()
        problem.add_problemType(av_problem)
        report.avalancheProblems.append(problem)

    reports.append(report)

    return reports

def date_from_report(date):
    date = dateutil.parser.parse(date, dayfirst=True)
    # date = datetime.datetime.strptime(date, '%d/%m/%Y')
    return date

# Only temporary for debug
def process_all_reports_it():
    all_reports = []
    for region in it_region_ref.keys():
        try:
            m_reports = process_reports_it(region)
        except Exception as e: # pylint: disable=broad-except
            logging.error('Failed to download %s', region, exc_info=e)
            
        for report in m_reports:
            all_reports.append(report)

    return all_reports
            

it_region_ref = {
    'IT-21-VB-03': ['Piemonte', 1],
    'IT-21-VB-02': ['Piemonte', 2],
    'IT-21-VB-01': ['Piemonte', 3],
    'IT-21-VC-01': ['Piemonte', 4],
    'IT-21-TO-03': ['Piemonte', 5],
    'IT-21-TO-01': ['Piemonte', 6],
    'IT-21-TO-04': ['Piemonte', 7],
    'IT-21-TO-02': ['Piemonte', 8],
    'IT-21-CN-03': ['Piemonte', 9],
    'IT-21-CN-01': ['Piemonte', 10],
    'IT-21-CN-02': ['Piemonte', 11],
    'IT-21-CN-04': ['Piemonte', 12],
    'IT-21-CN-05': ['Piemonte', 13],
    'IT-23-AO-A01': ['Aosta', 1],
    'IT-23-AO-A02': ['Aosta', 2],
    'IT-23-AO-A03': ['Aosta', 3],
    'IT-23-AO-A04': ['Aosta', 4],
    'IT-23-AO-A05': ['Aosta', 5],
    'IT-23-AO-B06': ['Aosta', 6],
    'IT-23-AO-B07': ['Aosta', 7],
    'IT-23-AO-B08': ['Aosta', 8],
    'IT-23-AO-B09': ['Aosta', 9],
    'IT-23-AO-B10': ['Aosta', 10],
    'IT-23-AO-B11': ['Aosta', 11],
    'IT-23-AO-C12': ['Aosta', 12],
    'IT-23-AO-C13': ['Aosta', 13],
    'IT-23-AO-D14': ['Aosta', 14],
    'IT-23-AO-D15': ['Aosta', 15],
    'IT-23-AO-D16': ['Aosta', 16],
    'IT-23-AO-D17': ['Aosta', 17],
    'IT-23-AO-D18': ['Aosta', 18],
    'IT-23-AO-D19': ['Aosta', 19],
    'IT-23-AO-D20': ['Aosta', 20],
    'IT-23-AO-C21': ['Aosta', 21],
    'IT-23-AO-D22': ['Aosta', 22],
    'IT-23-AO-A23': ['Aosta', 23],
    'IT-23-AO-A24': ['Aosta', 24],
    'IT-23-AO-B25': ['Aosta', 25],
    'IT-23-AO-A26': ['Aosta', 26],
    'IT-25-BS-01': ['Lombardia', 1],
    'IT-25-BG-01': ['Lombardia', 2],
    'IT-25-BG-02': ['Lombardia', 3],
    'IT-25-BS-02': ['Lombardia', 4],
    'IT-25-LC-01': ['Lombardia', 5],
    'IT-25-VA-01': ['Lombardia', 6],
    'IT-25-SO-02': ['Lombardia', 7],
    'IT-25-SO-01': ['Lombardia', 8],
    'IT-25-SO-03': ['Lombardia', 9],
    'IT-34-VI-01': ['Veneto', 1],
    'IT-34-VR-01': ['Veneto', 2],
    'IT-34-BL-06': ['Veneto', 3],
    'IT-34-BL-05': ['Veneto', 4],
    'IT-34-BL-02': ['Veneto', 5],
    'IT-34-BL-03': ['Veneto', 6],
    'IT-34-BL-04': ['Veneto', 7],
    'IT-34-BL-01': ['Veneto', 8],
    'IT-36-UD-01': ['Friuli', 1],
    'IT-36-UD-02': ['Friuli', 2],
    'IT-36-UD-03': ['Friuli', 3],
    'IT-36-UD-04': ['Friuli', 4],
    'IT-36-UD-05': ['Friuli', 5],
    'IT-36-PN-01': ['Friuli', 6],
    'IT-36-PN-02': ['Friuli', 7],
    'IT-57-MC-01': ['Marche', 1],
    'IT-57-AP-01': ['Marche', 2],
    'IT-57-PU-01': ['Marche', 3],
    'IT-57-AP-02': ['Marche', 4],
    }



