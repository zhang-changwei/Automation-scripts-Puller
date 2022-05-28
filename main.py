import urllib.request
import urllib.error
import re
import json

def pullRemoteScripts(url):
    try:
        response = urllib.request.urlopen(url, timeout=1.5)
        return True, response
    except urllib.error.HTTPError as e:
        print(url, '\n', e.code)
    return False, None

def getRemoteInfos(url = r'https://raw.githubusercontent.com/zhang-changwei/Automation-scripts-for-Aegisub/main/index.json'):
    try:
        response = urllib.request.urlopen(url, timeout=1.5)
        remote:dict = json.load(response)
        return remote
    except:
        return {}

def getLocalVersion(fp:str):
    with open(fp, encoding='utf-8') as f:
        for line in f.readlines():
            if line.startswith('script_version'):
                v = re.search('["\'](.*)["\']', line)
                return v.group(1)
