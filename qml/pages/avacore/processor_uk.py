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
from datetime import timedelta
from datetime import time
import pytz
import dateutil.parser
import logging
import re

from avacore.avabulletin import AvaBulletin, DangerRatingType, AvalancheProblemType, AvaCoreCustom, ElevationType, RegionType

def get_reports_from_json(sais_reports):
    reports = []

    for sais_report in sais_reports:
        report = AvaBulletin()
        report.regions.append(RegionType('GB-SCT-' + sais_report['Region']))
        report.bulletinID = 'GB-SCT-' + sais_report['ID']

        report.publicationTime = dateutil.parser.parse(sais_report['DatePublished'])
        report.validTime.startTime = report.publicationTime.replace(hour=18)
        report.validTime.endTime = report.validTime.startTime + timedelta(days=1)
        report.avalancheActivityHighlights = sais_report['Summary']
        report.avalancheActivityComment = 'Forecast Snow Stability: ' + sais_report['SnowStability']
        report.snowpackStructureComment = 'Forecast Weather Influences: ' + sais_report['WeatherInfluences'] +\
            '\n' + 'Observed Weather Influences: ' + sais_report['ObservedWeatherInfluences'] +\
            '\n' + 'ObservedSnowStability: ' + sais_report['ObservedSnowStability']

        problems = int(sais_report['KeyIcons'])

        problem = AvalancheProblemType()

        if problems & (1<<1):
            problem = AvalancheProblemType()
            problem.problemType = 'wind_drifted_snow'
            report.avalancheProblems.append(problem)
        if problems & (1<<2):
            problem = AvalancheProblemType()
            problem.problemType = 'persistent_weak_layers'
            report.avalancheProblems.append(problem)
        if problems & (1<<3):
            problem = AvalancheProblemType()
            problem.problemType = 'new_snow'
            report.avalancheProblems.append(problem)
        if problems & (1<<4):
            problem = AvalancheProblemType()
            problem.problemType = 'wet_snow'
            report.avalancheProblems.append(problem)
        if problems & (1<<5):
            problem = AvalancheProblemType()
            problem.problemType = 'cornice_failure'
            report.avalancheProblems.append(problem)
        if problems & (1<<6):
            problem = AvalancheProblemType()
            problem.problemType = 'gliding_snow'
            report.avalancheProblems.append(problem)

        danger_ratings_raw = sais_report['CompassRose'][4:36]

        boundary_group = re.search('(?<=txtm\=)(.)*?(?=\&txte)', sais_report['CompassRose'])
        boundary = boundary_group.group(0) # No content if no different ratings for elevations

        filter_lw = [True, False, False, False] * 8
        filter_hi = [False, True, False, False] * 8

        danger_ratings_hi = list(d for d, s in zip(danger_ratings_raw, filter_hi) if s)
        danger_ratings_lw = list(d for d, s in zip(danger_ratings_raw, filter_lw) if s)

        aspects = ['N','NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']

        if (
            max(danger_ratings_hi) == min(danger_ratings_hi)
            and max(danger_ratings_lw) == min(danger_ratings_lw)
            and max(danger_ratings_hi) == max(danger_ratings_lw)
        ):
            danger_rating = DangerRatingType()
            danger_rating.set_mainValue_int(int(max(danger_ratings_lw)))
            report.dangerRatings.append(danger_rating)
        else:
            set_danger_ratings_hi = set(danger_ratings_hi)
            set_danger_ratings_lw = set(danger_ratings_lw)

            for rating in set_danger_ratings_hi:
                aspect_list = []
                for idx, aspect in enumerate(aspects):
                    if (danger_ratings_hi[idx] == rating):
                        aspect_list.append(aspect)

                danger_rating = DangerRatingType()
                danger_rating.set_mainValue_int(int(rating))
                danger_rating.elevation.lowerBound = boundary
                danger_rating.aspect = aspect_list
                report.dangerRatings.append(danger_rating)

            for rating in set_danger_ratings_lw:
                aspect_list = []
                for idx, aspect in enumerate(aspects):
                    if (danger_ratings_lw[idx] == rating):
                        aspect_list.append(aspect)

                danger_rating = DangerRatingType()
                danger_rating.set_mainValue_int(int(rating))
                danger_rating.elevation.upperBound = boundary
                danger_rating.aspect = aspect_list
                report.dangerRatings.append(danger_rating)

        reports.append(report)

    return reports
    

def process_reports_uk():
    reports = []

    url = 'https://www.sais.gov.uk/api?action=getForecast'

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    req = urllib.request.Request(url, headers=headers)

    with urllib.request.urlopen(req) as response:
        content = response.read()

    sais_reports = json.loads(content)

    reports = get_reports_from_json(sais_reports)

    return reports
