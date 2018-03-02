#!/usr/bin/env python3
from lxml import html

import requests
import sys

def get_dependency_list(package):
    print("Getting dependencies of {}.".format(package))
    url = "http://formulae.brew.sh/formula/{}".format(package)
    page = requests.get(url)
    tree = html.fromstring(page.content)
    return tree.xpath("//div[@id='deps']//a[@class='formula']/text()")

def get_full_dependency_list(package):
    full_deps = []
    queue = [package]

    while len(queue) > 0:
        subpackage = queue.pop()
        deps = get_dependency_list(subpackage)
        full_deps.append(subpackage)

        for dep in deps:
            if dep not in full_deps and dep not in queue:
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
