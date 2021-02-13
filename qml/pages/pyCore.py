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
from pathlib import Path
from pyAvaCore.pyAvaCore import pyAvaCore

def fetch_cached_report(region_id, local, path):

    '''checks for a region_id if a local copy of this report is available at path at language local'''

    if Path(path + '/reports/'+region_id+local+'.pkl').is_file():
        with open(path + '/reports/'+region_id+local+'.pkl', 'rb') as input_file:
            return pickle.load(input_file)
    return None

def issue_report(region_id, local, path, from_cache=False, cli_out=False, send_other_side=True):

    '''function to issue report from remote or local cache. Caches local.'''

    url = "https://api.avalanche.report/albina/api/bulletins"
    reports = []
    provider = ""

    url, provider = pyAvaCore.get_report_url(region_id, local)


    cached = True
    if not from_cache:
        try:
            reports.extend(pyAvaCore.get_reports(url))
        except:
            matching_report = fetch_cached_report(region_id, local, path)


        Path(path + "/reports/").mkdir(parents=True, exist_ok=True)

        for report in reports:
            for current_region_id in report.valid_regions:
                with open(path + '/reports/'+current_region_id+local+'.pkl', 'wb') as f:
                    pickle.dump(report, f, pickle.HIGHEST_PROTOCOL)
            for ID in report.valid_regions:
                if ID == region_id:
                    matching_report = report
                    cached = False
    else:
        matching_report = fetch_cached_report(region_id, local, path)

    if send_other_side:
        send_to_other_side(matching_report, provider, cached)

    if cli_out:
        pyAvaCore.cli_print_report(matching_report, provider, cached)

def send_to_other_side(matching_report, provider, cached): # Should be part of avaRisk not pyAvaCore

    '''Sends out result using pyotherside'''

    import pyotherside
    try:
        matching_report
    except NameError:
        pyotherside.send('dangerLevel', "Problem resolving Region")
        pyotherside.send('provider', "Couldn't find the RegionID in the Report. Probably it is not served at the moment.")

        pyotherside.send('finished', False)
    else:
        dangerLevel = 0
        try:
            for elem in matching_report.danger_main:
                if elem.main_value > dangerLevel:
                    dangerLevel = elem.main_value
        except:
            pyotherside.send('finished', False)
        pyotherside.send('dangerLevel', dangerLevel)
        pyotherside.send('dangerLevel_h', matching_report.danger_main[0].main_value)
        if len(matching_report.danger_main) > 1:
            pyotherside.send('dangerLevel_l', matching_report.danger_main[1].main_value)
            pyotherside.send('dangerLevel_alti', matching_report.danger_main[0].valid_elevation)
        else:
            pyotherside.send('dangerLevel_l', matching_report.danger_main[0].main_value)
        pyotherside.send('highlights', matching_report.activity_hl)
        pyotherside.send('comment', matching_report.activity_com.replace("&nbsp;", " "))
        pyotherside.send('structure', matching_report.snow_struct_com.replace("&nbsp;", " "))
        pyotherside.send('tendency', matching_report.tendency_com.replace("&nbsp;", " "))
        pyotherside.send('repDate', matching_report.rep_date)
        pyotherside.send('validFrom', matching_report.validity_begin)
        pyotherside.send('validTo', matching_report.validity_end)
        pyotherside.send('numberOfDPatterns', len(matching_report.problem_list))
        pyotherside.send('dPatterns', str(matching_report.problem_list).replace("'", '"'))
        pyotherside.send('provider', provider)

        pyotherside.send('cached', cached)
        pyotherside.send('finished', True)

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

downloader = Downloader()
