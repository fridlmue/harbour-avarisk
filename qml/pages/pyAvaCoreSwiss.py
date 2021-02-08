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
    The Python Code is responsible for correct fetch of the slf avalanche information.
"""
import pyotherside
import threading
from datetime import datetime

import urllib.request
import zipfile
import pickle
from pathlib import Path
import json

# Downloads the swiss avalanche zip for the slf app together with the region mapping information
def downloadFiles(lang, path):
    Path(path + '/swiss/').mkdir(parents=True, exist_ok=True)
    url = 'https://www.slf.ch/avalanche/mobile/bulletin_'+lang+'.zip'
    urllib.request.urlretrieve(url, path + '/swiss/bulletin_'+lang+'.zip')

    urllib.request.urlretrieve('https://www.slf.ch/avalanche/bulletin/'+lang+'/gk_region2pdf.txt', path + '/swiss/gk_region2pdf.txt')

    with zipfile.ZipFile(path + '/swiss/bulletin_'+lang+'.zip', 'r') as zip_ref:
        zip_ref.extractall(path + '/swiss/')

# Decodes the information from the Report
def issueReport(regionID, local, path, fromCache=False):

    lang = "en"  #Set Lang to get Report (fr, it, en, de)
    provider = "Report from slf.ch"

    if not fromCache:
        cached = False
        if "DE" in local.upper():
            lang = "de"
            provider = "Bericht des slf.ch"

        downloadFiles(lang, path)
    else:
        cached = True

    # If some files are available in chache or newly loaded
    if Path(path + '/swiss/gk_region2pdf.txt').is_file():

        # Receives validity information from text.json
        with open(path + '/swiss/text.json') as fp:
            data = json.load(fp)

        region_id = regionID[-4:]

        report = avaReport_swiss()

        begin, end = data['validity'].split('/')

        dateTimeNow = datetime.now()

        report.repDate = datetime.strptime(str(dateTimeNow.year) + '-' + begin[begin.find(':')+2:-1], '%Y-%d.%m., %H:%M')
        report.timeBegin = report.repDate
        report.timeEnd = datetime.strptime(str(dateTimeNow.year) + '-' + end[end.find(':')+2:], '%Y-%d.%m., %H:%M')

        report_id = 0

        # Receives the ID of the report that matches the selected region_id
        with open(path + '/swiss/gk_region2pdf.txt') as fp:
            for line in fp:
                if line[:4] == region_id:
                    report_id = line.split('_')[5][:-5]
                    break

        if report_id != 0:

        # Opens the matching Report
            with open(path + '/swiss/1/dst' + report_id + '.html', encoding="utf-8") as f:
                text = f.read()

            # Isolates the relevant Danger Information
            text_pos = text.find('data-level=')+len('data-level=')+1
            report.dangerMain = text[text_pos:text_pos+1]

            # Isolates the prone location Image
            text_pos = text.find('src="data:image/png;base64,')+len('src="data:image/png;base64,')
            subtext = text[text_pos:]
            report.proneLocationsImg = subtext[:subtext.find('"')]
            if (len(report.proneLocationsImg) < 1000): # Sometimes no Picture is attached
                report.proneLocationsImg = '-'

            # Isolates the prone location Text
            text_pos = subtext.find('alt="')+len('alt="')
            subtext = subtext[text_pos:]
            report.proneLocationsText = subtext[:subtext.find('"')]
            if (report.proneLocationsText == 'Content-Type'):
                report.proneLocationsText = '-'

            # Remove Image from html, sometimes no Picture is attached

            try:
                split1 = text.split('<img')
                split2 = split1[1].split('">')
                report.htmlLocal = split1[0]+'"'.join(split2[1:])

            except:
                report.htmlLocal = text

            # Retreives the Weather and Snow Information
            text = ""
            with open(path + '/swiss/sdwetter.html', encoding="utf-8") as f:
                text = f.read()
            report.htmlWeatherSnow = text

            pyotherside.send('repDate', report.repDate)
            pyotherside.send('timeBegin', report.timeBegin)
            pyotherside.send('timeEnd', report.timeEnd)
            pyotherside.send('dangerMain', report.dangerMain)
            pyotherside.send('proneLocationsText', report.proneLocationsText)
            pyotherside.send('proneLocationsImg', report.proneLocationsImg)
            pyotherside.send('htmlLocal', report.htmlLocal)
            pyotherside.send('htmlWeatherSnow', report.htmlWeatherSnow)

            pyotherside.send('provider', provider)
            pyotherside.send('finished', True)
            pyotherside.send('cached', cached)
        else:
            pyotherside.send('finished', False)

    else:
        pyotherside.send('finished', False)

# Threaded Downloading of Report
class Downloader:
    def __init__(self):
        self.bgthread = threading.Thread()
        self.bgthread.start()

    # Starts Download and decoding of Report
    def download(self, regionID, local, path):
        if self.bgthread.is_alive():
            return
        self.bgthread = threading.Thread(target=issueReport(regionID, local, path))
        self.bgthread.start()

    # Starts Decoding of Report if available
    def cached(self, regionID, local, path):
        issueReport(regionID, local, path, fromCache=True)


class avaReport_swiss:
    def __init__(self):
        self.validRegions = []        # list of Regions
        self.repDate = ""             # Date of Report
        self.timeBegin = ""           # valid Ttime start
        self.timeEnd = ""             # valid time end
        self.dangerMain = 0           # danger main value
        self.proneLocationsText = ""  # prone locations text (elev and compass direction)
        self.proneLocationsImg = ""   # image of prone locations (elev and compass direction)
        self.htmlLocal = ""           # content of local bulletin
        self.htmlWeatherSnow = ""     # weather and snow report

downloader = Downloader()
