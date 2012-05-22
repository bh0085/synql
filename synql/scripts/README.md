#Databases project notes:#

##Tweet Collection##

Grabbing tweets from latitutde longitude cordinates. Code right now resides in projects/ows. Goal : 10m randomly selected tweets for clustering analysis, `alltweets = [text1, text2, ...]`

+ Port code out of ows, refactor for project.
+ Fill in iterative code for multipage, then multiday fetching.
+ Debug - are tweet lon/lat tags failing?


##Entity enumeration

+ Process each item in alltweets. Try to simply: (a) lowercase the string, (b) replace all irregular characters and punctuation except for spaces, (c) split lowercased strings at spaces. --> `allwords = [word1, word2, ...]`.
+ For each (possibly repeated) word in `allwords`, compute the occurnce  a list of the count for wordi in the `allwords`.
+ And then compute a histogram for the pVals of word occurence. Grab the top say ---one thousand--- for verifaction.
+ Verify significant words by running freebase queries to decide if they should be designated entities suitable for econtains querying. 

##Synonym collection##
###Easy: Use freebase.###

Freebase API resides at google APIs, can be accessed with Ben's developer API key:

`DEVELOPER_KEY = 'AIzaSyDGJapkaTMy09-nS96huqzdX4ftUCTJxwA'`, 

see test_freebase.py for a usage example. Freebase logins etc are tied to Ben's gmail account.

*Plan. (v0)*:  Figuring out basic search strategy for freebase, run a completely online strategy.

+ File synonyms.py, class FreebaseWords. Init creates a db connection to the freebase API with the google API for python. 
+ Create a FreebaseWords instance, `words` as `FreebaseWords(term)`.
+ Call words.fetchNode(): Runs a string search with the freebase api, select the first match (with preference to nouns) for the incoming term. Assigns words.center = N0.
+ Now, run a query on "also known as ${N0}". Fills words.synonyms
+ And generate an ExpandedContains operator from words.synonyms + words.center.


==Helpful notes==
Nowhere else to stick these:

ps | grep twtest | cut -d ' ' -f2 | xargs kill
