#rwikibot
A bot to pull and push subreddit wikis. Enables to use preferred editors and
version control.

##Usage
Do as you please:

###Submodule:
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

##Attention!
This includes config-files like the stylesheet. This probably lead to problems
with changes done online or restricted access.

Use 'restrict_to' in such a case to only upload and download specific files.
