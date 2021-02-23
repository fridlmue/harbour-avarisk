"""
CLI for pyAvaCore
"""
from datetime import datetime
from datetime import timedelta
from pathlib import Path
from urllib.request import urlopen
import json
import logging
import logging.handlers
import sys

from .pyAvaCore import AvaReport, clean_elevation, get_report_url, get_reports, get_reports_ch

Path('logs').mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    format='[%(asctime)s] {%(module)s:%(lineno)d} %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.handlers.TimedRotatingFileHandler(filename='logs/pyAvaCore.log', when='midnight'),
        logging.StreamHandler()])


def dumper(obj):
    """JSON serialization of datetime"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    try:
        return obj.toJSON()
    except: # pylint: disable=bare-except
        return obj.__dict__


def download_region(regionID):
    """Downloads the given region and converts it to JSON"""
    if regionID == 'CH':
        url = 'https://www.slf.ch/avalanche/mobile/bulletin_en.zip'
        reports = get_reports_ch(str(Path('cache')))
    else:
        url, _ = get_report_url(regionID)
        reports = get_reports(url)
    report: AvaReport
    for report in reports:
        if isinstance(report.validity_begin, datetime):
            validityDate = report.validity_begin
            if validityDate.hour > 15:
                validityDate = validityDate + timedelta(days=1)
            validityDate = validityDate.date().isoformat()
        report.report_texts = None
        report.valid_regions = [r.replace('AT8R', 'AT-08-0') for r in report.valid_regions]
        for danger in report.danger_main:
            danger.valid_elevation = clean_elevation(danger.valid_elevation)
        for problem in report.problem_list:
            problem.valid_elevation = clean_elevation(problem.valid_elevation)
            problem.aspect = [a.upper().replace('ASPECTRANGE_', '') for a in problem.aspect]

    directory = Path(sys.argv[1] if len(sys.argv) > 1 else 'data')
    directory.mkdir(parents=True, exist_ok=True)
    ext = 'zip' if url[-3:] == 'zip' else 'xml'
    with urlopen(url) as http, open(f'{directory}/{validityDate}-{regionID}.{ext}', mode='wb') as f:
        logging.info('Writing %s to %s', url, f.name)
        f.write(http.read())
    with open(f'{directory}/{validityDate}-{regionID}.json', mode='w', encoding='utf-8') as f:
        logging.info('Writing %s', f.name)
        json.dump(reports, fp=f, default=dumper, indent=2)


if __name__ == "__main__":
    regions = ["AT-02", "AT-03", "AT-04", "AT-05", "AT-06", "AT-08", "BY", "CH"]
    for region in regions:
        try:
            download_region(region)
        except Exception as e: # pylint: disable=broad-except
            logging.error('Failed to download %s', region, exc_info=e)
