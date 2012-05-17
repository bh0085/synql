Welcome to SynQL, a crappy web frontend demonstrating the capabilities of metanym-class streaming with TweeQL enabled by ECONTAINS..



#INSTALL#

Ok lets be honest here, I've never tried to share a Pylons project and at the moment, I'm probably not doing it correctly. Since everything is self contained and we don't actually use a database, you should be able to just download the repo and run a server with paster.

eg:

>git clone git://github.com/bh0085/synql.git
>cd synql
>paster serve --reload development.ini

And then navigate your browser to 

>http://localhost:8181/demo


If that fails then I'm probably missing something. Send me an email and I'll fix it up. Oh right, because I'm not taking advantage of pip, you'll have to install the various dependencies yourself; something like:

>sudo pip install paster
>sudo pip install pylons
>sudo pip install sqlalchemy

#Thanks#

Many thanks to Adam Marcus!
