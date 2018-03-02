#!/usr/bin/env python3
import sys

def main():
    if len(sys.argv) is not 2:
        print("Usage: {} <package name>".format(sys.argv[0]))
        sys.exit(1)

if __name__ == "__main__":
    main()
