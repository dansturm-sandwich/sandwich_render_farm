import sys
import os
from os import scandir, path
import time
from datetime import datetime
from logger_push import logger
import re
import requests
import subprocess

is_scanning = False

nukepath = '/Applications/Nuke14.0v5/Nuke14.0v5.app/Contents/MacOS/Nuke14.0'
nukeflags = '-xi'


def scantree(path):
    try:
        with os.scandir(path) as it:
            for entry in it:
                if not entry.name.startswith('.') and entry.is_file(follow_symlinks=False):
                    # logger.info(entry.path)
                    yield entry
            else:
                # logger.info(entry.path)
                yield entry
    except FileNotFoundError:
        logger.error(f"Directory {directory_path} is not accessible.")
        sys.exit(1)
    except Exception as e:
        logger.error(f'An unexpected error occurred: {str(e)}')
        sys.exit(1)


def read_render_submission(file_path):
    with open(file_path, 'r') as file:
        # Read the file and split into a list by new lines
        render_details = file.read().splitlines()
    return render_details



def link_to_path(sourceURL):
    fsn = re.search("(\d+\:\d+)", sourceURL)
    requestLucid = "http://localhost:7778/fsEntry?id=" + fsn[0]
    responseLucid = requests.get(requestLucid).json()
    pathLucid = responseLucid['path']
    fullpathLucid = f'/Volumes/sandwich-post/{pathLucid}'
    return fullpathLucid


if __name__ == '__main__':
    directory_path = "/Volumes/sandwich-post/assets/render_queue"
    scan_interval_day = 10  # seconds
    scan_interval_night = 10  # seconds
    
    file_extensions = ['.txt']  # add any other extensions you need
    render_queue_only = 'assets/render_queue'

    if not path.isdir(directory_path):
        logger.error(f"Directory {directory_path} is not accessible.")
        sys.exit(1)

      
    def update_scan():
        global is_scanning
        if is_scanning:
            return

        is_scanning = True
        current_seen = set()

        for entry in scandir(directory_path):
            if path.isdir(directory_path):
                try:
                    new_seen = set(
                        entry.path for entry in scantree(directory_path)
                        if render_queue_only in path.dirname(entry.path)
                        and path.splitext(entry.path)[1] in file_extensions
                    )
                    current_seen = current_seen.union(new_seen)
                except FileNotFoundError:
                    logger.error(f"Directory {directory_path} is not accessible.")
                    sys.exit(1)
            else:
                pass

        for new_file in current_seen:
            # logger.info(f'{new_file}')
            try:
                logger.info(f'Trigger file: {new_file}')
                logger.info(f'Render Submission: {new_file}')
                new_render = read_render_submission(new_file)
                logger.info(f'new_render: {new_render}')
                if 'lucid://' in new_render[0]:
                    script_url = new_render[0]
                    logger.info(f'script_url: {script_url}')
                    script_path = link_to_path(script_url)
                    logger.info(f'script_path: {script_path}')
                else:
                    script_path = new_render[0]
                    logger.info(f'script_path: {script_path}')
                script_name = os.path.basename(script_path)
                logger.info(f'script_name: {script_name}')
                if len(new_render) >= 3:
                    renderShell = f'"{nukepath}" -F {new_render[1]}-{new_render[2]} {nukeflags} "{script_path}"'
                    subprocess.Popen(renderShell, shell=True)
                    moveShell = f'mv -f {new_file} /Volumes/sandwich-post/assets/render_queue/_archive/'
                    subprocess.Popen(moveShell, shell=True)
                else:
                    renderShell = f'"{nukepath}" {nukeflags} "{script_path}"'
                    subprocess.Popen(renderShell, shell=True)
                    moveShell = f'mv -f {new_file} /Volumes/sandwich-post/assets/render_queue/_archive/'
                    subprocess.Popen(moveShell, shell=True)
                # new_render_listed = '\n'.join(new_render)
                # print(f'Render Details: \n{new_render_listed}')
            except:
                logger.info(f'Failed to open {new_file}')
                pass

        is_scanning = False


    while True:
        current_time = datetime.now()
        if 9 <= current_time.hour < 18:
            time.sleep(scan_interval_day)  # wait for the interval
        else:
            time.sleep(scan_interval_night)
        update_scan()

