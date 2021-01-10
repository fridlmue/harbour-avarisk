"""
    Copyright (C) 2020 Friedrich Mütschele and other contributors
    This file is part of avaRisk.
    avaRisk is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    avaRisk is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with avaRisk. If not, see <http://www.gnu.org/licenses/>.
"""
"""
    The Python Code is responsible for correct parsing of the CAAML-XML.
    The dafault Parsing part is for CAAML-XMLs like used in a wide area of
    Austria.
    Special Implementation is done for other Regions.
"""

import pyotherside
import threading
from datetime import datetime
from datetime import timezone
from urllib.request import urlopen
import copy

def addParentInfo(et):
    for child in et:
        child.attrib['__my_parent__'] = et
        addParentInfo(child)

def getParent(et):
    if '__my_parent__' in et.attrib:
        return et.attrib['__my_parent__']
    else:
        return None

def getXmlAsElemT(url):

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
    except Exception as e:
        print('error parsing ElementTree: ' + str(e))

    return root

def parseXML(root):

    reports = []

    for bulletin in root.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}Bulletin'):
        report = avaReport()
        for observations in bulletin:
            addParentInfo(observations)
            for locRef in observations.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}locRef'):
                report.validRegions.append(observations.attrib.get('{http://www.w3.org/1999/xlink}href'))
            for locRef in observations.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}locRef'):
                report.validRegions.append(observations.attrib.get('{http://www.w3.org/1999/xlink}href'))
            for dateTimeReport in observations.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}dateTimeReport'):
                report.repDate = tryParseDateTime(dateTimeReport.text).replace(tzinfo=timezone.utc)
            for validTime in observations.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}validTime'):
                if not (getParent(validTime)):
                    for beginPosition in observations.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}beginPosition'):
                        report.timeBegin = tryParseDateTime(beginPosition.text).replace(tzinfo=timezone.utc)
                    for endPosition in observations.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}endPosition'):
                        report.timeEnd = tryParseDateTime(endPosition.text).replace(tzinfo=timezone.utc)
            for DangerRating in observations.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}DangerRating'):
                mainValueR = 0
                for mainValue in DangerRating.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}mainValue'):
                    mainValueR = int(mainValue.text)
                validElevR = "-"
                for validElevation in DangerRating.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}validElevation'):
                    validElevR = validElevation.attrib.get('{http://www.w3.org/1999/xlink}href')
                report.dangerMain.append({'mainValue':mainValueR,'validElev':validElevR})
            for DangerPattern in observations.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}DangerPattern'):
                for DangerPatternType in DangerPattern.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}type'):
                    report.dangerPattern.append(DangerPatternType.text)
            i = 0
            for AvProblem in observations.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}AvProblem'):
                typeR = ""
                for avProbType in AvProblem.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}type'):
                    typeR = avProbType.text
                aspect = []
                for validAspect in AvProblem.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}validAspect'):
                    aspect.append(validAspect.get('{http://www.w3.org/1999/xlink}href'))
                validElevR = "-"
                for validElevation in AvProblem.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}validElevation'):
                    validElevR = validElevation.get('{http://www.w3.org/1999/xlink}href')
                i = i+1
                report.problemList.append({'type':typeR,'aspect':aspect,'validElev':validElevR})
            for avActivityHighlights in observations.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}avActivityHighlights'):
                report.activityHighl = avActivityHighlights.text
            for avActivityComment in observations.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}avActivityComment'):
                report.activityCom = avActivityComment.text
            for snowpackStructureComment in observations.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}snowpackStructureComment'):
                report.snowStrucCom = snowpackStructureComment.text
            for tendencyComment in observations.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}tendencyComment'):
                report.tendencyCom = tendencyComment.text
        reports.append(report)

    return reports

def parseXMLVorarlberg(root):
    numberOfRegions = 6
    reports = []
    report = avaReport()
    report.validRegions=[""]
    commentEmpty = 1
    # Common for every Report:
    for bulletin in root.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}Bulletin'):
        for detail in bulletin:
            for metaDataProperty in detail.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}metaDataProperty'):
                for dateTimeReport in metaDataProperty.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}dateTimeReport'):
                    report.repDate = tryParseDateTime(dateTimeReport.text)
            for bulletinResultsOf in detail.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}bulletinResultsOf'):
                for travelAdvisoryComment in bulletinResultsOf.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}travelAdvisoryComment'):
                    report.activityCom = travelAdvisoryComment.text
                for highlights in bulletinResultsOf.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}highlights'):
                    report.activityHighl = highlights.text
                for comment in bulletinResultsOf.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}comment'):
                    if commentEmpty:
                        report.tendencyCom = comment.text
                        commentEmpty = 0
                for wxSynopsisComment in bulletinResultsOf.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}wxSynopsisComment'):
                    report.activityCom = report.activityCom + " <br />Alpinwetterbericht der ZAMG Tirol und Vorarlberg:<br /> " + str(wxSynopsisComment.text)
                for snowpackStructureComment in bulletinResultsOf.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}snowpackStructureComment'):
                    report.snowStrucCom = snowpackStructureComment.text
                i = 0
                for AvProblem in detail.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}AvProblem'):
                    typeR = ""
                    for acProblemType in AvProblem.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}type'):
                        typeR = acProblemType.text
                    aspect = []
                    for validAspect in AvProblem.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}validAspect'):
                        aspect.append(validAspect.get('{http://www.w3.org/1999/xlink}href'))
                    validElev = "-"
                    for validElevation in AvProblem.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}validElevation'):
                        for beginPosition in validElevation.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}beginPosition'):
                            validElev = "ElevationRange_" + beginPosition.text + "Hi"
                        for endPosition in validElevation.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}endPosition'):
                            validElev = "ElevationRange_" + endPosition.text + "Lw"
                    i = i+1
                    report.problemList.append({'type':typeR,'aspect':aspect,'validElev':validElev})


    for i in range(numberOfRegions+1):
        reports.append(copy.deepcopy(report))

    # Individual for the Regions:
    for bulletin in root.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}Bulletin'):
        for detail in bulletin:
            for bulletinResultsOf in detail.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}bulletinResultsOf'):
                for DangerRating in bulletinResultsOf.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}DangerRating'):
                    regionID = 7
                    for locRef in DangerRating.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}locRef'):
                        regionID = int(locRef.attrib.get('{http://www.w3.org/1999/xlink}href')[-1])
                        reports[regionID-1].validRegions[0] = locRef.attrib.get('{http://www.w3.org/1999/xlink}href')
                    for validTime in DangerRating.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}validTime'):
                        for beginPosition in validTime.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}beginPosition'):
                            reports[regionID-1].timeBegin = tryParseDateTime(beginPosition.text)
                        for endPosition in validTime.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}endPosition'):
                            reports[regionID-1].timeEnd = tryParseDateTime(endPosition.text)
                    mainValue = 0
                    validElev = "-"
                    for mainValue in DangerRating.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}mainValue'):
                        mainValue = int(mainValue.text)
                    for validElevation in DangerRating.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}validElevation'):
                        for beginPosition in validElevation.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}beginPosition'):
                            validElev = "ElevationRange_" + beginPosition.text + "Hi"
                        for endPosition in validElevation.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}endPosition'):
                            validElev = "ElevationRange_" + endPosition.text + "Lw"
                    reports[regionID-1].dangerMain.append({'mainValue':mainValue,'validElev':validElev})
    return reports


def parseXMLBavaria(root):

    numberOfRegions = 6
    reports = []
    report = avaReport()
    report.validRegions=[""]

    # Common for every Report:
    for metaData in root.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}metaDataProperty'):
        for dateTimeReport in metaData.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}dateTimeReport'):
                    report.repDate = tryParseDateTime(dateTimeReport.text)

    for bulletinMeasurements in root.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}BulletinMeasurements'):
        for travelAdvisoryComment in bulletinMeasurements.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}travelAdvisoryComment'):
            report.activityCom = travelAdvisoryComment.text
        for wxSynopsisComment in bulletinMeasurements.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}wxSynopsisComment'):
            report.activityCom = report.activityCom + " <br />Deutscher Wetterdienst - Regionale Wetterberatung München:<br /> " + str(wxSynopsisComment.text)
        for snowpackStructureComment in bulletinMeasurements.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}snowpackStructureComment'):
            report.snowStrucCom = snowpackStructureComment.text
        for highlights in bulletinMeasurements.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}comment'):
            report.activityHighl = highlights.text
        i = 0
        for avProblem in bulletinMeasurements.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}avProblem'):
            type = ""
            for avType in avProblem.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}type'):
                type = avType.text
            aspect = []
            for validAspect in avProblem.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}validAspect'):
                aspect.append(validAspect.get('{http://www.w3.org/1999/xlink}href').lower())
            validElev = "-"
            for validElevation in avProblem.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}validElevation'):
                for beginPosition in validElevation.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}beginPosition'):
                    validElev = "ElevationRange_" + beginPosition.text + "Hi"
                for endPosition in validElevation.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}endPosition'):
                    validElev = "ElevationRange_" + endPosition.text + "Lw"
            i = i+1
            report.problemList.append({'type':type,'aspect':aspect,'validElev':validElev})

    for i in range(numberOfRegions+1):
        reports.append(copy.deepcopy(report))

    # Check Names of all Regions

    for bulletinResultOf in root.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}bulletinResultsOf'):
        addParentInfo(bulletinResultOf)
        for locRef in bulletinResultOf.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}locRef'):
            found = False
            regionID = -1
            firstFree = 100
            for index, report in enumerate(reports):
                if any(report.validRegions):
                    for region in report.validRegions:
                        if region == locRef.attrib.get('{http://www.w3.org/1999/xlink}href'):
                            found = True
                            regionID = index
                else:
                    if firstFree > index:
                        firstFree = index
            if not found:
                reports[firstFree].validRegions.append(locRef.attrib.get('{http://www.w3.org/1999/xlink}href'))
                regionID = firstFree

            DangerRating = getParent(locRef)


            for validTime in DangerRating.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}validTime'):
                for beginPosition in validTime.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}beginPosition'):
                    reports[regionID].timeBegin = tryParseDateTime(beginPosition.text)
                for endPosition in validTime.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}endPosition'):
                    reports[regionID].timeEnd = tryParseDateTime(endPosition.text)
            mainValue = 0
            validElev = "-"
            for mainValue in DangerRating.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}mainValue'):
                mainValue = int(mainValue.text)
            for validElevation in DangerRating.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}validElevation'):
                for beginPosition in validElevation.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}beginPosition'):
                    validElev = "ElevationRange_" + beginPosition.text + "Hi"
                for endPosition in validElevation.iter(tag='{http://caaml.org/Schemas/V5.0/Profiles/BulletinEAWS}endPosition'):
                    validElev = "ElevationRange_" + endPosition.text + "Lw"
            reports[regionID].dangerMain.append({'mainValue':mainValue,'validElev':validElev})

    return reports

def getReports(url):
    root = getXmlAsElemT(url)
    if "VORARLBERG" in url.upper():
        reports = parseXMLVorarlberg(root)
    elif "BAYERN" in url.upper():
        reports = parseXMLBavaria(root)
    else:
        reports = parseXML(root)
    return reports


def tryParseDateTime(inStr):
    try:
        r_dateTime = datetime.strptime(inStr, '%Y-%m-%dT%XZ')
        #print(r_dateTime.isoformat())
    except:
        try:
            r_dateTime = datetime.strptime(inStr[:19], '%Y-%m-%dT%X') # 2019-04-30T15:55:29+01:00
            #print(r_dateTime.isoformat())
        except:
            # print('some Error in try dateTime') (Normal vor Vorarlberg)
            r_dateTime = datetime.now()

    return r_dateTime


def issueReport(regionID, local):

    url = "https://api.avalanche.report/albina/api/bulletins"
    reports = []
    provider = ""
    # Euregio-Region Tirol, Südtirol, Trentino
    if ("AT-07" in regionID) or ("IT-32-BZ" in regionID) or ("IT-32-TN" in regionID):
        url = "https://api.avalanche.report/albina/api/bulletins"
        provider = "The displayed information is provided by an open data API on https://avalanche.report by: Avalanche Warning Service Tirol, Avalanche Warning Service Südtirol, Avalanche Warning Service Trentino."
        if "DE" in local.upper():
            url += "?lang=de"
            provider = "Die dargestellten Informationen werden über eine API auf https://avalanche.report abgefragt. Diese wird bereitgestellt von: Avalanche Warning Service Tirol, Avalanche Warning Service Südtirol, Avalanche Warning Service Trentino."

    # Kärnten
    if "AT-02" in regionID:
        url = "https://www.avalanche-warnings.eu/public/kaernten/caaml"
        provider = "Die dargestellten Informationen werden über eine API auf https://www.avalanche-warnings.eu abgefragt. Diese wird bereitgestellt vom: Lawinenwarndienst Kärnten (https://lawinenwarndienst.ktn.gv.at)."

    # Salzburg
    if "AT-05" in regionID:
        url = "https://www.avalanche-warnings.eu/public/salzburg/caaml/en"
        provider = "Die dargestellten Informationen werden über eine API auf https://www.avalanche-warnings.eu abgefragt. Diese wird bereitgestellt vom: Lawinenwarndienst Salzburg (https://lawine.salzburg.at)."
        if "DE" in local.upper():
            url = "https://www.avalanche-warnings.eu/public/salzburg/caaml"
            provider = "The displayed information is provided by an open data API on https://www.avalanche-warnings.eu by: Avalanche Warning Service Salzburg (https://lawine.salzburg.at)."

    # Steiermark
    if "AT-06" in regionID:
        url = "https://www.avalanche-warnings.eu/public/steiermark/caaml/en"
        provider = "The displayed information is provided by an open data API on https://www.avalanche-warnings.eu by: Avalanche Warning Service Steiermark (https://www.lawine-steiermark.at)."
        if "DE" in local.upper():
            url = "https://www.avalanche-warnings.eu/public/steiermark/caaml"
            provider = "Die dargestellten Informationen werden über eine API auf https://www.avalanche-warnings.eu abgefragt. Diese wird bereitgestellt vom: Lawinenwarndienst Steiermark (https://www.lawine-steiermark.at)."

    # Oberösterreich
    if "AT-04" in regionID:
        url = "https://www.avalanche-warnings.eu/public/oberoesterreich/caaml"
        provider = "Die dargestellten Informationen werden über eine API auf https://www.avalanche-warnings.eu abgefragt. Diese wird bereitgestellt vom: Lawinenwarndienst Oberösterreich (https://www.land-oberoesterreich.gv.at/lawinenwarndienst.htm)."

    # Niederösterreich - Noch nicht angelegt
    if "AT-03" in regionID:
        url = "https://www.avalanche-warnings.eu/public/niederoesterreich/caaml"
        provider = "Die dargestellten Informationen werden über eine API auf https://www.avalanche-warnings.eu abgefragt. Diese wird bereitgestellt vom: Lawinenwarndienst Niederösterreich (https://www.lawinenwarndienst-niederoesterreich.at)."

    #Vorarlberg
    if regionID.startswith("AT8"):
        url = "https://warndienste.cnv.at/dibos/lawine_en/avalanche_bulletin_vorarlberg_en.xml"
        provider = "The displayed information is provided by an open data API on https://warndienste.cnv.at by: Landeswarnzentrale Vorarlberg - http://www.vorarlberg.at/lawine"
        if "DE" in local.upper():
            url = "http://warndienste.cnv.at/dibos/lawine/avalanche_bulletin_vorarlberg_de.xml"
            provider = "Die dargestellten Informationen werden über eine API auf https://warndienste.cnv.at abgefragt. Diese wird bereitgestellt von der Landeswarnzentrale Vorarlberg - http://www.vorarlberg.at/lawine"

    #Bavaria
    if regionID.startswith("BY"):
        url = "https://www.lawinenwarndienst-bayern.de/download/lagebericht/caaml_en.xml"
        provider = "The displayed ihe displayed information is provided by an open data API on https://www.lawinenwarndienst-bayern.de/ by: Avalanche warning centre at the Bavarian State Office for the Environment - https://www.lawinenwarndienst-bayern.de/"
        if "DE" in local.upper():
            url = "https://www.lawinenwarndienst-bayern.de/download/lagebericht/caaml.xml"
            provider = "Die dargestellten Informationen werden über eine API auf https://www.lawinenwarndienst-bayern.de abgefragt. Diese wird bereitgestellt von der Lawinenwarnzentrale Bayern (https://www.lawinenwarndienst-bayern.de)."

    #Val d'Aran
    if regionID.startswith("ES-CT-L"):
        url = "https://conselharan2.cyberneticos.net/albina_files_local/latest/en.xml"
        provider = "The displayed ihe displayed information is provided by an open data API on https://lauegi.conselharan.org/ by: Conselh Generau d'Aran - https://lauegi.conselharan.org/"
        if "DE" in local.upper():
            url = "https://conselharan2.cyberneticos.net/albina_files_local/latest/de.xml"
            provider = "Die dargestellten Informationen werden über eine API auf https://lauegi.conselharan.org/ abgefragt. Diese wird bereitgestellt von Conselh Generau d'Aran (https://lauegi.conselharan.org/)."


    reports.extend(getReports(url))

    for report in reports:
        for ID in report.validRegions:
            if ID == regionID:
              matchingReport = report

    try:
        matchingReport
    except NameError:
        pyotherside.send('dangerLevel', "Problem resolving Region")
        pyotherside.send('provider', "Couldn't find the RegionID in the Report. Probably it is not served at the moment.")

        pyotherside.send('finished', False)
    else:
        dangerLevel = 0
        for elem in matchingReport.dangerMain:
            if elem['mainValue'] > dangerLevel:
                dangerLevel = elem['mainValue']

        pyotherside.send('dangerLevel', dangerLevel)
        pyotherside.send('dangerLevel_h', matchingReport.dangerMain[0]['mainValue'])
        if (len(matchingReport.dangerMain) > 1):
            pyotherside.send('dangerLevel_l', matchingReport.dangerMain[1]['mainValue'])
            pyotherside.send('dangerLevel_alti', matchingReport.dangerMain[0]['validElev'])
        else:
            pyotherside.send('dangerLevel_l', matchingReport.dangerMain[0]['mainValue'])
        pyotherside.send('highlights', matchingReport.activityHighl)
        pyotherside.send('comment',matchingReport.activityCom.replace("&nbsp;", " "))
        pyotherside.send('structure', matchingReport.snowStrucCom.replace("&nbsp;", " "))
        pyotherside.send('tendency', matchingReport.tendencyCom.replace("&nbsp;", " "))
        pyotherside.send('repDate', matchingReport.repDate)
        pyotherside.send('validFrom', matchingReport.timeBegin)
        pyotherside.send('validTo', matchingReport.timeEnd)
        pyotherside.send('numberOfDPatterns', len(matchingReport.problemList))
        pyotherside.send('dPatterns', str(matchingReport.problemList).replace("'", '"'))
        pyotherside.send('provider', provider)

        pyotherside.send('finished', True)

class Downloader:
    def __init__(self):
        self.bgthread = threading.Thread()
        self.bgthread.start()

    def download(self, regionID, local):
        if self.bgthread.is_alive():
            return
        self.bgthread = threading.Thread(target=issueReport(regionID, local))
        self.bgthread.start()

class avaReport:
    def __init__(self):
        self.validRegions = []          # list of Regions
        self.repDate = ""               # Date of Report
        self.timeBegin = ""             # valid Ttime start
        self.timeEnd = ""               # valid time end
        self.dangerMain = []            # danger Value and elev
        self.dangerPattern = []         # list of Patterns
        self.problemList = []           # list of Problems with Sublist of Aspect&Elevation
        self.activityHighl = "none"     # String avalanche activity highlits text
        self.activityCom = "none"       # String avalanche comment text
        self.snowStrucCom = "none"      # String comment on snowpack structure
        self.tendencyCom = "none"       # String comment on tendency

downloader = Downloader()
