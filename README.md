## About

Hitman Challenge bot randomizes a challenge for Hitman 2's contracts mode, gets a random title for it from an online book title generator, formats the challenge on an image and posts it on Twitter.

Made using Python 3.

## Getting started

To start using it in it's full capacity you need to first do the following steps:

- Under the root folder, create a folder called res. In that folder create folders named after ids of the missions that will be used (tss, agc, si...) and in those folders place image files you want to use for the missions. PNG-format is recommended, but other formats should also work.
- In the res -folder, also include coolvetica.ttf font, or whatever font you wish to use. Just remember to also change it in DailyHitman.py if you use something else.
- If you want to use the Twitter functionality, create config.ini in the root folder and include the following info:

```
[TWITTER]
consumer_key = [GET_THIS_FROM_developer.twitter.com]
consumer_secret = [GET_THIS_FROM_developer.twitter.com]
access_token_key = [GET_THIS_FROM_developer.twitter.com]
access_token_secret = [GET_THIS_FROM_developer.twitter.com]
```

- In the root folder, create mapfilter.txt which contains a list of mission ids that will NOT be included in the next roll. On the next roll, top id will be removed from the file and the rolled id will be added to the bottom. To adjust the number of the possible missions, simply add or remove ids to the file. Example, in which World of Tomorrow can not appear in the next roll, but can appear in the one after that:

```
wot
tss
agc
```

## Rundown of the important files

- ChallengeFunctions.py contains the randomizers for the different rules. It's jank but mostly works.
- DailyHitman.py is the main script that creates challenge.jpg in the root folder and tweets it to the connected account. Most things happen here.
- GlobalVars.py contains some classes and variables that are nice to have access to globally. A more python-savvy programmer would probably handle this very differently.
- data.json simply includes all the data that's used to create a random challenge. Based on the Hitman Roulette, so some of the included data is far more detailed than it needs to be.
- fix.py is used to fix line endings so the program can be ran on Linux after being edited on on Windows. Should not be needed if that's not your use case.

If this doesn't work, ask TheKotti#4747 on Discord might be able to help.
