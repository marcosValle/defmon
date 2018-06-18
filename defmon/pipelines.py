# -*- coding: utf-8 -*-
from scrapy.exceptions import DropItem
import os
import pymongo
from scrapy.mail import MailSender
from scrapy.utils.project import get_project_settings
import hashlib
from urllib.parse import quote
from termcolor import colored

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

class ModifiedPipeline(object):

    collection_name = 'pages_items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if self.db[self.collection_name].find({'link':item['link']}).count() <= 0:
            print(colored('[+] New page found! - {}'.format(item['link']), 'green'))
            self.db[self.collection_name].insert_one(dict(item))
            return item

        for a in self.db[self.collection_name].find({'link':item['link']}):
            if a.get('md5') == item['md5']:
                print(colored('[+] Page {} has NOT changed since last crawling'.format(item['link']), 'green'))
                raise DropItem(colored("[+] Page {} dropped".format(item['link']), 'blue'))
            else:
                print(colored('[!] Page {} has changed since last crawling!'.format(item['link']), 'yellow'))
                self.db[self.collection_name].update(dict(item))
                return item

class PwnedPipeline(object):
    wordlist = []

    def __init__(self):
        self.getWordlist('wordlists/wordlistVar.txt')

    def process_item(self, item, spider):
        return self.checkPwned(item)

    def checkPwned(self, item):
        print(colored('[!] Checking if page is pwned', 'yellow'))
        pwned = False
        for word in self.wordlist:
            if word in item['message']:
                pwned = True
                break

        if pwned == True:
            print(colored('[!!] Page {} seems to have been hacked!', 'red').format(item['link']))
            print(colored('[+] Saving suspicious page into log file', 'yellow'))
            with open('log/{}'.format(item['link'].split('/')[2]), 'a+') as f:
                f.write(item['timestamp']+
                        ' - '+
                        item['link']+
                        '\n')

            print(colored('[+] Sending e-mail alert', 'yellow'))
            print(SendMail(
                item,
                "marcos.valle01@gmail.com",
                "ATTENTION REQUIRED: {}".format(item['link'].split('/')[2])
                ).send())
            return item
        else:
            raise DropItem("Page {} -- OK".format(item['link']))

    def getWordlist(self, wlPath):
        with open(wlPath, 'rb') as f:
            word = f.readlines()
            self.wordlist = [x.strip() for x in word]

class SendMail:
    def __init__(self, item, to, subject):
        self.item = item
        self.to = to
        self.subject = subject
        self.settings = get_project_settings()
        self.mailer = MailSender.from_settings(self.settings)

    def send(self):
        self.mailer.send(to=[self.to],
                subject=self.subject,
                body='Possibly hacked URL: {}'.format(self.item['link']),
                cc=None)
