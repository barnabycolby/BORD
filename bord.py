#!/usr/bin/env python3
from lxml import html

import requests
import sys

def get_dependency_list(package):
    print("Getting dependencies of {}.".format(package))
    url = "http://formulae.brew.sh/formula/{}".format(package)
    page = requests.get(url)
    tree = html.fromstring(page.content)

    package_name = package
    package_deps = tree.xpath("//div[@id='deps']//a[@class='formula']/text()")
    package_url = tree.xpath("//a[text()='Formula code']/@href")

    return { 'name': package_name, 'url': package_url, 'deps': package_deps }

def package_in_dictionaries(package, dictionaries):
    for dictionary in dictionaries:
        if dictionary['name'] == package:
            return True

    return False

def get_full_dependency_list(package):
    full_deps = [] # List of package dictionaries
    queue = [package] # List of package names

    while len(queue) > 0:
        subpackage = queue.pop()
        subpackage_dictionary = get_dependency_list(subpackage)
        full_deps.append(subpackage_dictionary)

        for dep in subpackage_dictionary['deps']:
            if not package_in_dictionaries(dep, full_deps) and dep not in queue:
                queue.append(dep)

    return full_deps


def main():
    if len(sys.argv) is not 2:
        print("Usage: {} <package name>".format(sys.argv[0]))
        sys.exit(1)

    package = sys.argv[1]
    print(get_full_dependency_list(package))

if __name__ == "__main__":
    main()
