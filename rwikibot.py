#!/usr/bin/env python3
#License: GPL v2

import praw
import yaml
import logging
import os
import argparse

user_agent = 'reddit wiki bot v1.0 by /u/nath_schwarz'
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
    """Logs in to reddit with given username and password, returns reddit-instance.

    Prompts if username or password is missing."""
    global r
    try:
        r = praw.Reddit(user_agent = user_agent)
        if not conf['password']:
            if not conf['username']:
                r.login()
            else:
                r.login(conf['username'])
        else:
            r.login(conf['username'], conf['password'])
        logging.info('Login successful')
    except Exception as e:
        logging.error(e)

def get_folder(subreddit, key):
    if 'folder' in subreddit.keys():
        folder = subreddit['folder']
    else:
        folder = key
    if not folder == '':
        folder += '/'
    return folder

def do(action = 'pull'):
    subreddits = conf['subreddits']

    for key in subreddits:
        subreddit = subreddits[key]
        folder = get_folder(subreddit, key)

        if action in subreddit.keys():
            if subreddit[action] is False:
                logging.info('Subreddit ' + key + ' not ' + action + 'ed, key is false')
                break

        restrict = action + '_restrict_to'
        if restrict in subreddit.keys():
            pagefiles = [ folder + pagefile for pagefile in subreddit[restrict] ]
        elif action == 'pull':
            pagefiles = r.get_wiki_pages(key)
        else:
            pagefiles = [ os.path.join(root, f)
                for root, subfolders, filenames in os.walk(folder)
                for f in filenames
                if not f[0] == '.']

        for pagefile in pagefiles:
            if action == 'pull':
                pull_page(folder, pagefile)
            else:
                push_page(key, folder, pagefile)


def pull_page(folder, pagefile):
    pagename = page.page
    filename = folder + pagename

    if '/' in pagename:
        # use of filename to assure that top-folder is being created
        dirs = filename.rsplit('/', 1)[0]
        if not os.path.exists(dirs):
            os.makedirs(dirs)
            logging.info('Created directory ' + dirs)

    with open(filename, 'w') as f:
        if conf['type'] == 'html':
            f.write(page.content_html)
        else:
            f.write(page.content_md)
        logging.info('Pulled page to file ' + filename)

def push_page(key, folder, pagefile):
    pagename = pagefile.split('/', 1)[1]
    with open(pagefile, 'r') as f:
        r.edit_wiki_page(key, pagename, f.read())
    logging.info('Uploaded wiki page ' + pagename)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true", help="verbose output")
    parser.add_argument("--stdout", action="store_true", help="print log output to stdout")
    parser.add_argument("-d" , "--pull", action="store_true", help="pull wikis from reddit")
    parser.add_argument("-u", "--push", action="store_true", help="push files to reddit wikis")
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level = logging.INFO)
    else:
        logging.basicConfig(level = logging.ERROR)
    if not args.stdout:
        logging.basicConfig(filename = 'rwikibot.log')

    if args.push or args.pull:
        load_config()
        login()
        try:
            if args.push:
                do(action = 'push')
            else:
                do(action = 'pull')
        except Exception as e:
            logging.error(e)
        r.clear_authentication()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
