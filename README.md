#rwikibot
A bot to pull and push subreddit wikis. Enables to use preferred editors and
version control.

##Usage
Add this repo as a submodule with
`git submodule add https://github.com/nathschwarz/rwikibot.git`. Populate the
`wikibot.conf` as written in `wikibot.conf.example`.
To pull the subreddits' wiki execute `python rwikibot/rwikiboy.py --pull`. The
pulled files are placed in the folder you defined in `wikibot.conf`.  to push
your local files to the subreddits' wiki execute `python rwikibot/rwikibot.py
--push`.

##Attention!
This includes config-files like the stylesheet. This probably lead to problems
with changes done online.

Use 'restrict_to' in such a case to only upload specific files.
