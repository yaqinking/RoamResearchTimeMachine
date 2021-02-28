'''
Roam Research Time Machine

- Backup Roam Research image files.
- Support incremental backup.

Script steps:
1. Get file download link.
2. Check local file folder is exist file.
3. If not exist file download it.
'''
import os
import re
import requests
import shutil

from pathlib import Path
from urllib.parse import urlparse

roam_export = Path('roam_export')
files = Path('roam_export/files')

md_files = roam_export.glob('*.md')
file_url_pattern = "(?P<url>https?://firebasestorage.[^\s]+)"

proxies = {
  'http': 'http://127.0.0.1:1080',
  'https': 'http://127.0.0.1:1080',
}

def is_exist_file(fn):
    '''
    Is file exist in roam export folder.
    '''
    return len(list(roam_export.glob('**/' + fn))) > 0

print('------------------------------\nStart Roam Time Machine task.\n------------------------------')

for md in md_files:
    content = open(md, mode='r', encoding='utf8')
    lines = content.readlines()
    for line in lines:
        # Skip line by url prefix
        if not 'https://firebasestorage.' in line:
            continue

        url = re.search(file_url_pattern, line).group('url')
        url = url.replace(')', '') # Remove extract url end character )
        # Get file name from parsed url
        parsed_url = urlparse(url)
        file_name = parsed_url.path.split('%2F')[-1]
        file_save_path = Path.joinpath(files, file_name)
        print('Check downloaded file from url:\n{0}'.format(url))
        if is_exist_file(file_name):
            #Skip downloaded file
            print('Skip downloaded file: {0}'.format(file_name))
            continue

        print('Start download: {0}'.format(url))
        # Get image use proxy
        response = requests.get(url, stream=True, proxies=proxies)
        with open(file_save_path, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response
        print('Saved to: {0}'.format(file_save_path))

    
print('------------------------------\nAll task has been completed!\n------------------------------')
