#!/usr/bin/env python3
from lxml import html

import os
import requests
import sys

BASE_URL = "http://formulae.brew.sh"

def get_dependency_list(package):
    package_name = package['name']
    print("Getting dependencies of {}.".format(package_name))
    package_url = package['url']
    page = requests.get(package_url)
    tree = html.fromstring(page.content)

    # Parse the dependencies and their urls
    package_deps = []
    package_deps_nodes = tree.xpath("//div[@id='deps']//a[@class='formula']")
    for node in package_deps_nodes:
        dep_name = node.xpath("text()")[0]
        dep_relative_url = node.xpath("@href")[0]
        dep_url = "{}{}".format(BASE_URL, dep_relative_url)
        package_dep = { 'name': dep_name, 'url': dep_url }
        package_deps.append(package_dep)
    
    package_urls = tree.xpath("//a[text()='Formula code']/@href")

    if len(package_urls) is not 1:
        print("Couldn't find the formula URL for {}. The scraping is probably broken!".format(package))
        sys.exit(1)
    package_url = package_urls[0]

    return { 'name': package_name, 'url': package_url, 'deps': package_deps }

def package_in_dictionaries(package, dictionaries):
    for dictionary in dictionaries:
        if dictionary['name'] == package['name']:
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

def download_formulas(package_dictionaries, output_dir):
    for package_dictionary in package_dictionaries:
        name = package_dictionary['name']
        url = package_dictionary['url']

        print("Downloading formula for {}.".format(name))
        request = requests.get(url)
        file_name = "{}.rb".format(name)
        file_path = os.path.join(output_dir, file_name)
        with open(file_path, "wb") as output_file:
            output_file.write(request.content)

def main():
    if len(sys.argv) is not 2:
        print("Usage: {} <package name>".format(sys.argv[0]))
        sys.exit(1)

    package_name = sys.argv[1]
    package_url = "{}/formula/{}".format(BASE_URL, package_name)
    package = { 'name': package_name, 'url': package_url }
    dependencies = get_full_dependency_list(package)

    if not os.path.exists(package_name):
        os.makedirs(package_name)
    download_formulas(dependencies, package_name)

if __name__ == "__main__":
    main()
