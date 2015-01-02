#rwikibot
A bot to pull and push subreddit wikis. Enables to use preferred editors and
version control.

Well, at least it is meant as a bot. You can use it as a script. The bot
functionality would be to setup a cronjob on a server to pull changes from
a git-repositoy and to push them to reddit.

##Usage
Do as you please:

###Submodule in existing repo:
Folder structure:
```
.
├── .gitignore
├── .gitmodules
├── rwikibot
│   ├── .gitignore
│   ├── rwikibot.py
│   └── wikibot.conf.exmaple
├── wiki
│   ├── config
│   │   └── stylesheet
│   └── index
└── wikibot.conf
```
Pull wiki pages: `py rwikibot/rwikibot.py --pull`  
Push wiki pages: `py rwikibot/rwikibot.py --push`

###Script in dir:
Folder structure:
```
.
├── .gitignore
├── .gitmodules
│── rwikibot.py
├── wiki
│   ├── config
│   │   └── stylesheet
│   └── index
└── wikibot.conf
```
Pull wiki pages: `py rwikibot.py --pull`  
Push wiki pages: `py rwikibot.py --push`

###Script with multiple submodules:
Folder structure:
```
.
├── .gitignore
├── .gitmodules
├── rwikibot
│   ├── .gitignore
│   ├── rwikibot.py
│   └── wikibot.conf.exmaple
├── subreddit1
│   ├── config
│   │   └── stylesheet
│   ├── index
│   └── contributions
├── subreddit2
│   ├── config
│   │   └── sidebar
│   └── index
├── subreddit3foldername
│   ├── config
│   │   ├── sidebar
│   │   ├── description
│   │   └── submit_text
│   └── index
└── wikibot.conf
```
wikibot.conf:
```
password: password
username: username
type: md
subreddits:
    subreddit1:
        restrict_to:
            - config/stylesheet
            - index
            - contributions
    subreddit2:
        restrict_to:
            - config/sidebar
            - index
    subreddit3:
        folder: subreddit3foldername
```
Pull wiki pages: `py rwikibot/rwikibot.py --pull`  
Push wiki pages: `py rwikibot/rwikibot.py --push`

Cronjob:
```
#!/usr/bin/env bash

cd /path/to/repo
git submodule foreach 'git pull' #or git pull if you use a single repo without collaboration with others
python rwikibot/rwikibot.py --push
```

##python packages:
`sudo pip3 install praw pyaml logging argparse`

##Attention!
This includes config-files like the stylesheet. This probably lead to problems
with changes done online or restricted access.

Use 'restrict_to' in such a case to only upload and download specific files.

##Known issues
If the config/ folder doesn't show up, you have to edit
something in there first - be it the stylesheet, sidebar or
submit_text.
