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

import urllib.request
import zipfile
from pathlib import Path
import pickle
import json

def issueReport(regionID, local, path):

    lang = "en"  #Set Lang to get Report (fr, it, en, de)

    if "DE" in local.upper():
        lang = "de"

    Path(path + '/swiss/').mkdir(parents=True, exist_ok=True)
    url = 'https://www.slf.ch/avalanche/mobile/bulletin_'+lang+'.zip'
    urllib.request.urlretrieve(url, path + '/swiss/bulletin_'+lang+'.zip')

    with zipfile.ZipFile(path + '/swiss/bulletin_'+lang+'.zip', 'r') as zip_ref:
        zip_ref.extractall(path + '/swiss/')

    with open(path + '/swiss/text.json') as fp:
        data = json.load(fp)

    region_id = regionID[-4:]

    report = avaReport_swiss()

    begin, end = data['validity'].split('/')

    report.repDate = begin[begin.find(':')+2:-1]
    report.timeBegin = report.repDate
    report.timeEnd = end[end.find(':')+2:]
    report.timeBegin

    response = urllib.request.urlopen('https://www.slf.ch/avalanche/bulletin/'+lang+'/gk_region2pdf.txt')

    report_id = 0

    for line in response.readlines():
        if str(line)[2:6] == region_id:
            report_id = str(line).split('_')[5][:-7]
            break

    with open(path + '/swiss/1/dst' + report_id + '.html', encoding="utf-8") as f:
        text = f.read()

    text_pos = text.find('data-level=')+len('data-level=')+1
    report.dangerMain = text[text_pos:text_pos+1]

    text_pos = text.find('src="data:image/png;base64,')+len('src="data:image/png;base64,')
    subtext = text[text_pos:]
    report.proneLocationsImg = subtext[:subtext.find('"')]

    text_pos = subtext.find('alt="')+len('alt="')
    subtext = subtext[text_pos:]

    report.proneLocationsText = subtext[:subtext.find('"')]

    # Remove Image
    split1 = text.split('<img')
    split2 = split1[1].split('">')
    report.htmlLocal = split1[0]+'"'.join(split2[1:])
    # report.htmlLocal = text

    text = ""

    with open(path + '/swiss/sdwetter.html', encoding="utf-8") as f:
        text = f.read()

    report.htmlWeatherSnow = text

    # pyotherside.send('validRegions', report.validRegions)
    pyotherside.send('repDate', report.repDate)
    pyotherside.send('timeBegin', report.timeBegin)
    pyotherside.send('timeEnd', report.timeEnd)
    pyotherside.send('dangerMain', report.dangerMain)
    pyotherside.send('proneLocationsText', report.proneLocationsText)
    pyotherside.send('proneLocationsImg', report.proneLocationsImg)
    pyotherside.send('htmlLocal', report.htmlLocal)
    pyotherside.send('htmlWeatherSnow', report.htmlWeatherSnow)

    pyotherside.send('provider', "SLF.ch")
    pyotherside.send('finished', True)

    Path(path + "reports/").mkdir(parents=True, exist_ok=True)

    with open(path + 'reports/'+regionID+local+'.pkl', 'wb') as f:
        pickle.dump(matchingReport, f, pickle.HIGHEST_PROTOCOL)

class Downloader:
    def __init__(self):
        self.bgthread = threading.Thread()
        self.bgthread.start()

    def download(self, regionID, local, path):
        if self.bgthread.is_alive():
            return
        self.bgthread = threading.Thread(target=issueReport(regionID, local, path))
        self.bgthread.start()

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
