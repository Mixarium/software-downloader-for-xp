import os
import sys
import inquirer
import requests
import platform
import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse

def integer(string):
    parallelCount = int(string)
    if parallelCount <= 0:
        raise argparse.ArgumentTypeError("integer value must be positive.")
    return parallelCount

def output_directory(string):
    if not os.path.exists(string):
        raise argparse.ArgumentTypeError("path does not exist.")
    return string


# default args
defaultDestFolder = "./"
defaultParallelDownloads = 1

parser = argparse.ArgumentParser()

parser.add_argument(
    '-o', '--output',
    type=output_directory,
    default=defaultDestFolder,
    help='download the selected software to a specified existing directory (default: .\\).\
        a folder named "sdfwxp_downloads" will be created in that directory.'
)
parser.add_argument(
    '-p', '--parallel',
    type=integer, 
    default=defaultParallelDownloads,
    help='Maximum number of parallel downloads (default: 1).'
)
parser.add_argument(
    '-oa', '--other-architecture',
    action='store_true',
    help='Will download the opposing architecture type of the software (x64 -> x86 / x86 -> x64), if possible.'
)

args = parser.parse_args()

destFolder = args.output
parallelDownloads = args.parallel
switchArchFlag = args.other_architecture

tqdm_params = {
    'miniters': 1,
    'unit': 'B',
    'unit_scale': True,
    'unit_divisor': 1024,
    'ascii': '-#',
    'bar_format': '{desc:<30} {total_fmt:>5}  {rate_fmt:>8}{postfix} {elapsed} [{bar:18}] {percentage:3.0f}%'
}

jsonURL = 'https://raw.githubusercontent.com/Mixarium/software-downloader-for-xp/refs/heads/main/urls.json'

with requests.get(jsonURL) as r:
    jsonData = r.json()

questions = []
sections = tuple(jsonData.keys())
sectionsLen = len(sections)

for i, section in enumerate(sections):
    questions.append(inquirer.Checkbox(
        section,
        message=f"{section} ({i+1}/{sectionsLen})",
        choices=tuple(jsonData[section].keys()),
        carousel=True
    ))

answers = inquirer.prompt(questions)
if not answers:
    exit()

get_architecture = platform.machine()

if get_architecture == 'x86':
    arch_index = 0 if not switchArchFlag else -1
elif get_architecture in ('x86_64', 'AMD64'):
    arch_index = -1 if not switchArchFlag else 0


def download(url, software):
    firstSplitName = url.split('/')[-1]
    filename = firstSplitName.split('dwl=')[-1]
    os.makedirs(f"{destFolder}/sdfwxp_downloads", exist_ok=True)

    with open(f"{destFolder}/sdfwxp_downloads/{filename}", 'wb') as f:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            total = int(r.headers.get('content-length', 0))

            with tqdm.tqdm(desc=software, total=total, **tqdm_params) as pb:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
                    pb.update(len(chunk))
                    

with ThreadPoolExecutor(max_workers=parallelDownloads) as ex:
    futures = []

    for section in answers:
        answersSection = answers[section]
        for software in answersSection:
            futures.append(ex.submit(download, jsonData[section][software][arch_index], software))

    for future in as_completed(futures):
        result = future.result()