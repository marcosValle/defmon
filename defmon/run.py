#!/usr/bin/env python

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import *
from scrapy.utils.project import get_project_settings
import argparse
from sys import exit

if __name__ == "__main__":

    print("""
***************************************
*  ____        __ __  __              *
* |  _ \  ___ / _|  \/  | ___  _ __   *
* | | | |/ _ \ |_| |\/| |/ _ \| '_ \  *
* | |_| |  __/  _| |  | | (_) | | | | *
* |____/ \___|_| |_|  |_|\___/|_| |_| *
*   			              *
***************************************
* DefMon Release 0.1                  *
* Coded by @__mvalle__		      *
***************************************
    """)

    parser = argparse.ArgumentParser(
            description='Deface Monitor: recursively crawl a domain and check for defaced pages',
            epilog='Example of use: ./run.py -d mydefaceddomain.com -u http://mydefaceddomain.com/hackedPages/'
            )
    parser.add_argument("--domain", '-d',  help="Allowed domain", required=True)
    parser.add_argument("--url", '-u',  help="Start URL", required=True)

    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        exit(1)

    process = CrawlerProcess(get_project_settings())
    process.crawl('mySpider', domain=args.domain, start_url=args.url)
    process.start()
