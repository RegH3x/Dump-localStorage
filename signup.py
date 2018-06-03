#!/usr/bin/python2.7


# NOTES

# Find tags in a page
# driver.find_element_by_name("q")

# INSTALL

# pip install selenium

# Firefox:  Get latest release geckodriver of https://github.com/mozilla/geckodriver/releases
# http://selenium-python.readthedocs.io/installation.html#detailed-instructions-for-windows-users
# tar xvf geckodriver-vXX.X-linux64.tar.gz && mv geckodriver /usr/bin

# DA USARE CON LINK HTTP e NON HTTPS. Altrimento il driver non riesce ad accedere al localStorage

import sys
import json

# WebDriver implementations are Firefox, Chrome, IE and Remote
from selenium import webdriver

# The Keys class provide keys in the keyboard like RETURN, F1, ALT etc.
from selenium.webdriver.common.keys import Keys


def payload_js():

    return """
    var localstore = {};
    for (var i = 0; i < localStorage.length; i++){
        nome_key = localStorage.key(i);
        value = localStorage.getItem(nome_key);
        localstore[nome_key] = value;
    }
    return localstore 
    """


def dump_list(handle_file, list, list_name):

    print("{}".format(list_name))

    handle_file.write(list_name+'\n')

    for v in list: handle_file.write("{}\n".format(v))


def dump_json(handle_file, dict, dict_name):

    print("{}".format(dict_name))

    handle_file.write(dict_name+'\n')

    handle_file.write("{0}\n".format(json.dumps(dict)))


def dump(c, ls, t):

    print("localstore: {}".format(ls))
    print("cookies: {}".format(c))

    with open('results.txt','w') as hf:

        hf.write(t + '\n\n')

        if type(ls) is dict or list: dump_json(hf, ls, "localStorage")

        if type(c) is list: dump_list(hf, c, "Cookies")


def main():


    if len(sys.argv) < 1:
        print("Usage {} <url_to_get>".format(sys.argv[0]))
        exit(1)

    uri = sys.argv[1]

    driver = webdriver.Firefox()

    driver.get(uri)

    try:
        localstore = driver.execute_script(payload_js())

    except:
        print("Failed to get localStorage or no elements to show")
        localstore = ''

    cookies = driver.get_cookies()

    title = driver.title

    dump(cookies, localstore, title)


if __name__ == '__main__': main()