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
from datetime import timedelta
import copy

from avacore import pyAvaCore
from avacore.avabulletin import AvaBulletin

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

### XML-Parsers

def parse_xml(root):

    '''parses ALBINA-Style CAAML-XML. root is a ElementTree'''

    reports = []

    for bulletin in root.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}Bulletin'):
        report = pyAvaCore.AvaBulletin()
        report.reportId = bulletin.attrib.get('{http://www.opengis.net/gml}id')
        pm_danger_ratings = []

        pm_available = False
        for DangerRating in bulletin.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}DangerRating'):
            for validTime in DangerRating.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}validTime'):
                pm_available = True
                break

        for observations in bulletin:
            et_add_parent_info(observations)
            for locRef in observations.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}locRef'):
                loc_ref = observations.attrib.get('{http://www.w3.org/1999/xlink}href')
                if loc_ref not in report.region:
                    report.region.append(observations.attrib.get('{http://www.w3.org/1999/xlink}href'))
            for dateTimeReport in observations.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}dateTimeReport'):
                report.publicationTime = pyAvaCore.try_parse_datetime(dateTimeReport.text).replace(tzinfo=timezone.utc)
            for validTime in observations.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}validTime'):
                if not et_get_parent(validTime):
                    for beginPosition in observations.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}beginPosition'):
                        report.validity_begin = pyAvaCore.try_parse_datetime(beginPosition.text).replace(tzinfo=timezone.utc)
                    for endPosition in observations.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}endPosition'):
                        report.validity_end = pyAvaCore.try_parse_datetime(endPosition.text).replace(tzinfo=timezone.utc)
            for DangerRating in observations.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}DangerRating'):
                main_value = 0
                am_rating = True
                for mainValue in DangerRating.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}mainValue'):
                    main_value = int(mainValue.text)
                valid_elevation = "-"
                for validElevation in DangerRating.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}validElevation'):
                    valid_elevation = validElevation.attrib.get('{http://www.w3.org/1999/xlink}href')
                for beginPosition in DangerRating.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}beginPosition'):
                    if '11:00' in beginPosition.text:
                        am_rating = False
                        report.validity_end = report.validity_end.replace(hour=11)
                if am_rating:
                    report.danger_main.append(pyAvaCore.DangerMain(main_value, valid_elevation))
                else:
                    pm_danger_ratings.append(pyAvaCore.DangerMain(main_value, valid_elevation))
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
                report.problem_list.append(pyAvaCore.Problem(type_r, aspect, valid_elevation))
            for avActivityHighlights in observations.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}avActivityHighlights'):
                report.report_texts.append(pyAvaCore.ReportText('activity_hl', avActivityHighlights.text))
            for avActivityComment in observations.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}avActivityComment'):
                report.report_texts.append(pyAvaCore.ReportText('activity_com', avActivityComment.text))
            for snowpackStructureComment in observations.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}'\
                                                              'snowpackStructureComment'):
                report.report_texts.append(pyAvaCore.ReportText('snow_struct_com', snowpackStructureComment.text))
            for tendencyComment in observations.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}tendencyComment'):
                report.report_texts.append(pyAvaCore.ReportText('tendency_com', tendencyComment.text))
        reports.append(report)

        if pm_available:
            pm_report = copy.deepcopy(report)
            pm_report.danger_main = pm_danger_ratings
            pm_report.report_id += '_PM'
            pm_report.validity_begin = pm_report.validity_begin + timedelta(hours=12)
            pm_report.validity_end = pm_report.validity_end + timedelta(hours=12)
            reports.append(pm_report)

    for report in reports:
        if report.reportId.endswith('_PM') and any(x.reportId == report.reportId[:-3] for x in reports):
            report.predecessor_id = report.reportId[:-3]

    return reports
