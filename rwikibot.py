#!/usr/bin/env python3
#License: GPL v2

import praw
import yaml
import logging
import os
import argparse

#logging defaults
# logging.basicConfig(filename = 'rwikibot.log', level = logging.ERROR)

user_agent = 'reddit wiki bot v0.1 by /u/nath_schwarz'
conf_file = 'wikibot.conf'

#globals
r = None
conf = None

def load_config():
    """Loads configuration from 'cspaperbot.conf' and returns it."""
    global conf
    try:
        with open(conf_file, 'r') as f:
            conf = yaml.load(f)
    except Exception as e:
        logging.error(e)

def login():
    """Logs in to reddit with given username and password, returns reddit-instance."""
    global r
    try:
        r = praw.Reddit(user_agent = user_agent)
        r.login(conf['username'], conf['password'])
        logging.info('Login successful')
    except Exception as e:
        logging.error(e)

def pull_wiki():
    pages = r.get_wiki_pages(conf['subreddit'])
    for page in pages:
        pagename = page.page
        filename = conf['folder'] + pagename
        if '/' in pagename:
            # use of filename to assure that wiki/ is being created
            dirs = filename.rsplit('/', 1)[0]
            if not os.path.exists(dirs):
                os.makedirs(dirs)
                logging.info('Created directory ' + dirs)
        with open(filename, 'w') as f:
            if conf['type'] == 'html':
                f.write(page.content_html)
            else:
                f.write(page.content_md)
            logging.info('Wrote file ' + filename)

def push_wiki():
    pagefiles = [ os.path.join(root, f)
            for root, subfolders, filenames in os.walk(conf['folder'])
            for f in filenames ]
    for pagefile in pagefiles:
        pagename = pagefile.split('/', 1)[1]
        with open(pagefile, 'r') as f:
            r.edit_wiki_page(conf['subreddit'], pagename, f.read())
        logging.info('Uploaded wiki page ' + pagename)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="verbose output", action="store_true")
    parser.add_argument("-d" , "--pull", action="store_true", help="pull wiki from reddit")
    parser.add_argument("-u", "--push", action="store_true", help="push files to reddit wiki")
    args = parser.parse_args()

    if args.push or args.pull:
        load_config()
        login()
        if args.push:
            push_wiki()
        else:
            pull_wiki()
        r.clear_authentication()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
