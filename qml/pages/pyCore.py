"""
    Copyright (C) 2021 Friedrich Mütschele and other contributors
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
import pickle
import json
from datetime import datetime
from pathlib import Path
from avacore import pyAvaCore

def fetch_cached_report(region_id, local, path, pm=False):

    '''checks for a region_id if a local copy of this report is available at path at language local'''

    if pm:
        local = local + '_pm'

    if Path(path + '/reports/'+region_id+local+'_pm'+'.pkl').is_file() and not '_pm' in region_id:
        with open(path + '/reports/'+region_id+local+'_pm'+'.pkl', 'rb') as input_file:
            print('')
    if Path(path + '/reports/'+region_id+local+'.pkl').is_file():
        with open(path + '/reports/'+region_id+local+'.pkl', 'rb') as input_file:
            return pickle.load(input_file)

def issue_report(region_id, local, path, from_cache=False, cli_out=False, send_other_side=True, pm=False):

    '''function to issue report from remote or local cache. Caches local.'''

    url = "https://api.avalanche.report/albina/api/bulletins"
    reports = []
    provider = ""
    matching_report_pm = ''

    cached = True
    if not from_cache:

        url, provider = pyAvaCore.get_report_url(region_id, local)

        try:
            reports.extend(pyAvaCore.get_reports(url))
        except:
            matching_report = fetch_cached_report(region_id, local, path)


        Path(path + "/reports/").mkdir(parents=True, exist_ok=True)

        for report in reports:
            for current_region_id in report.valid_regions:
                pm_marker = ''
                if hasattr(report, 'predecessor_id'):
                    pm_marker = '_pm'
                with open(path + '/reports/' + current_region_id + local + pm_marker + '.pkl', 'wb') as f:
                    pickle.dump(report, f, pickle.HIGHEST_PROTOCOL)
                if current_region_id == region_id:
                    if not hasattr(report, 'predecessor_id'):
                        matching_report = report
                        cached = False
        for report in reports:
            if hasattr(report, 'predecessor_id'):
                if matching_report.report_id == report.predecessor_id:
                    matching_report_pm = report

    else:
        matching_report = fetch_cached_report(region_id, local, path)

    if send_other_side:
        send_to_other_side(matching_report, matching_report_pm, provider, cached)

    if cli_out:
        pyAvaCore.cli_print_report(matching_report, provider, cached)

def dumper(obj):
    """JSON serialization of datetime"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    try:
        return obj.toJSON()
    except: # pylint: disable=bare-except
        return obj.__dict__

def send_to_other_side(matching_report, matching_report_pm, provider, cached): # Should be part of avaRisk not pyAvaCore

    '''Sends out result using pyotherside'''

    import pyotherside
    try:
        matching_report
    except NameError:
        pyotherside.send('dangerLevel', "Problem resolving Region")
        pyotherside.send('provider', "Couldn't find the RegionID in the Report. Probably it is not served at the moment.")

        pyotherside.send('finished', False)
    else:
        reports = [matching_report, matching_report_pm]
        json_dump = json.dumps(reports, default=dumper, indent=2)
        pyotherside.send('AvaReport', json_dump)

        pyotherside.send('cached', cached)
        pyotherside.send('finished', True)

def sel_report_text(report_texts, searched_type):
    for text in report_texts:
        if text.text_type == searched_type:
            return text.text_content
    return ''

class Downloader:

    '''Enables Assynchronous DL or request of report from chache'''

    def __init__(self):
        self.bgthread = threading.Thread()
        self.bgthread.start()

    def download(self, region_id, local, path):

        '''Download Report in BG-Thread'''

        if self.bgthread.is_alive():
            return
        self.bgthread = threading.Thread(target=issue_report(region_id, local, path))
        self.bgthread.start()

    def cached(self, region_id, local, path):

        '''Print out cached report'''

        issue_report(region_id, local, path, from_cache=True)

    def cached_pm(self, region_id, local, path):

        '''Print out cached report'''

        issue_report(region_id, local, path, from_cache=True, pm=True)

downloader = Downloader()
