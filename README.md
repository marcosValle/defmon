# DefMon - Deface Monitor
* Recursively crawl a website given a start url and a list of allowed domains using scrapy
* For each link found, store the hash of the page content in a MongoDB and look for a group of wordlists in this content
* If the page has been checked before (ie, its hash is in the db), DefMon will first check only the hashes due to performance issues
* Only if the hashes are not identical look for defacement indicators
* In case of a strong defacement idicator, write suspicious pages to `log/` and send an e-mail

# INSTALL/CONFIG
It is strongly adviced to use this tool within a virtual environment.

**python3.5+ required**

~~~
(myEnv)$ pip install -r requirements.txt
~~~

After installing the requirements, edit `settings.py` with your e-mail settings:

~~~
ITEM_PIPELINES ={
     'defmon.pipelines.ModifiedPipeline': 300,
     'defmon.pipelines.PwnedPipeline': 800,
 }
 
 # Mail settings. Change it!
 MAIL_FROM = 'changeme@gmail.com'
 MAIL_HOST = 'smtp.gmail.com'
 MAIL_PORT = 587
 MAIL_USER = 'changeme@gmail.com'
 MAIL_PASS = 'myDamnSecurePass'
 MAIL_TLS = True
 #MAIL_SSL = True
~~~

# USAGE

~~~
usage: ./run.py [-h] --domain DOMAIN --url URL

Deface Monitor: recursively crawl a domain and check for defaced pages

optional arguments:
  -h, --help            show this help message and exit
  --domain DOMAIN, -d DOMAIN
                        Allowed domain
  --url URL, -u URL     Start URL

Example of use: ./run.py -d mydefaceddomain.com -u http://mydefaceddomain.com/hackedPages/
~~~

In order to reset your database, please run:

~~~
(myEvnv)$ python resetDb.py
~~~~

**NOTICE: this will clear all your database. Use it carefully or dragons might pop up from your screen.**

# DISCLAIMER
This tool is under active developed. No guarantees are provided.

# CONTRIBUTION
No requirements! Feel free to help :)

## TODO
* Take screenshot of defaced pages and send by e-mail
* Implement OTP for images defacements
* Implement AI for learning new indicators (cheers if you do this one)
* Set credentials in environment variables
* TESTS!!!
