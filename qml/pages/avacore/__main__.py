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

from .pyAvaCore import AvaReport, JSONEncoder, get_report_url, get_reports

Path('logs').mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    format='[%(asctime)s] {%(module)s:%(lineno)d} %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.handlers.TimedRotatingFileHandler(filename='logs/pyAvaCore.log', when='midnight'),
        logging.StreamHandler()])


def download_region(regionID):
    """Downloads the given region and converts it to JSON"""
    if regionID == 'CH':
        url = 'https://www.slf.ch/avalanche/mobile/bulletin_en.zip'
        reports, _, _ = get_reports(regionID, cache_path=str(Path('cache')))
    else:
        reports, _, url = get_reports(regionID)
    report: AvaReport
    for report in reports:
        if isinstance(report.validity_begin, datetime):
            validityDate = report.validity_begin
            if validityDate.hour > 15:
                validityDate = validityDate + timedelta(days=1)
            validityDate = validityDate.date().isoformat()
        report.report_texts = None
        report.valid_regions = [r.replace('AT8R', 'AT-08-0') for r in report.valid_regions]

    directory = Path(sys.argv[1] if len(sys.argv) > 1 else 'data')
    directory.mkdir(parents=True, exist_ok=True)
    ext = 'zip' if url[-3:] == 'zip' else 'xml'
    with urlopen(url) as http, open(f'{directory}/{validityDate}-{regionID}.{ext}', mode='wb') as f:
        logging.info('Writing %s to %s', url, f.name)
        f.write(http.read())
    with open(f'{directory}/{validityDate}-{regionID}.json', mode='w', encoding='utf-8') as f:
        logging.info('Writing %s', f.name)
        json.dump(reports, fp=f, cls=JSONEncoder, indent=2)


if __name__ == "__main__":
    regions = ["AT-02", "AT-03", "AT-04", "AT-05", "AT-06", "AT-08", "BY", "CH"]
    for region in regions:
        try:
            download_region(region)
        except Exception as e: # pylint: disable=broad-except
            logging.error('Failed to download %s', region, exc_info=e)
