import json
import urllib.request
from datetime import datetime
from datetime import timedelta
from datetime import time
import pytz
import dateutil.parser

from avacore.avabulletin import AvaBulletin, DangerRatingType, AvalancheProblemType, AvaCoreCustom, ElevationType, RegionType


def process_reports_no(region_id):

    langkey = '2' # Needs to be set by language 1 -> Norwegian, 2 -> Englisch (parts of report)

    url = "https://api01.nve.no/hydrology/forecast/avalanche/v6.0.0/api/AvalancheWarningByRegion/Detail/" + region_id[3:] + "/" + langkey + "/"

    headers = {
        "Content-Type": "application/json; charset=utf-8"
        }

    req = urllib.request.Request(url, headers=headers)

    with urllib.request.urlopen(req) as response:
        content = response.read()

    varsom_report = json.loads(content)

    reports = get_reports_fromjson(region_id, varsom_report)
    
    return reports


def get_reports_fromjson(region_id, varsom_report, fetch_time_dependant=True):
    reports = []
    report = AvaBulletin()
    
    current = 0
    now = datetime.now(pytz.timezone('Europe/Oslo'))
    if fetch_time_dependant and now.time() > time(17, 0, 0):
        current = 1

    report.regions.append(RegionType(region_id))
    report.publicationTime = dateutil.parser.parse(varsom_report[current]['PublishTime'].split('.')[0])
    report.bulletinID = (region_id + "_" + str(report.publicationTime))

    report.validTime.startTime = dateutil.parser.parse(varsom_report[current]['ValidFrom'])
    report.validTime.endTime = dateutil.parser.parse(varsom_report[current]['ValidTo'])

    # report.danger_main.append(pyAvaCore.DangerMain(int(varsom_report[current]['DangerLevel']), '-'))
    
    danger_rating = DangerRatingType()
    danger_rating.set_mainValue_int(int(varsom_report[current]['DangerLevel']))
    
    report.dangerRatings.append(danger_rating)

    for problem in varsom_report[current]['AvalancheProblems']:
        problem_type = ''
        if problem['AvalancheProblemTypeId'] == 7:
            problem_type = 'new_snow'
        elif problem['AvalancheProblemTypeId'] == 10:
            problem_type = 'wind_drifted_snow'
        elif problem['AvalancheProblemTypeId'] == 30:
            problem_type = 'persistent_weak_layers'
        elif problem['AvalancheProblemTypeId'] == 45:
            problem_type = 'wet_snow'
        elif problem['AvalancheProblemTypeId'] == 0: #???
            problem_type = 'gliding_snow'
        elif problem['AvalancheProblemTypeId'] == 0: #???
            problem_type = 'favourable_situation'

        aspects = ['N','NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        aspect_list = []

        for i, c in enumerate(problem['ValidExpositions']):
            if c == '1':
                aspect_list.append(aspects[i])

        elev_prefix = ''
        if problem['ExposedHeightFill'] == 1:
            elev_prefix = '>'
        elif problem['ExposedHeightFill'] == 2:
            elev_prefix = '<'
        
        if not problem_type == '':
            problem_danger_rating = DangerRatingType()
            problem_danger_rating.aspect = aspect_list
            problem_danger_rating.elevation.auto_select(elev_prefix + str(problem['ExposedHeight1']))
            problem = AvalancheProblemType()
            problem.dangerRating = problem_danger_rating
            problem.problemType = problem_type
            report.avalancheProblems.append(problem)

    report.avalancheActivityHighlights = varsom_report[current]['MainText']
    report.avalancheActivityComment = varsom_report[current]['AvalancheDanger']
    waek_layers = ''
    if varsom_report[0]['CurrentWeaklayers'] != None:
        waek_layers = '\n' + varsom_report[0]['CurrentWeaklayers']
    report.snowpackStructureComment = varsom_report[current]['SnowSurface']  + waek_layers
    report.tendency.tendencyComment = varsom_report[current+1]['MainText']

    reports.append(report)

    return reports
