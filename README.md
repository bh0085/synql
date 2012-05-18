Welcome to SynQL, a crappy web frontend demonstrating the capabilities of metanym-class streaming with TweeQL enabled by ECONTAINS..

#INSTALL#

First thing, you'll need a copy of Ben/Fulton Wang's modified tweeql repo - you can get that with:

>git clone git://github.com/bh0085/tweeql.git

Since may not want to to uninstall the stable version of tweeql from github.com/marcua, you can simply add the new tweeql/bin directory to the system path (make sure its loaded stable tweeql). SynQL will need the modified tweeql in its path so you'll probably have to set the pythonPath to recognize it, eg:

> export PYTHONPATH=${PYTHONPATH}:[tweeql-path]/tweeql/bin

in **bashrc**.

----

Ok lets be honest here, I've never tried to share a Pylons project and at the moment, I'm probably not doing it correctly. Since everything is self contained and we don't actually use a database, you should be able to just download the repo and run a server with paster.

eg:

>git clone git://github.com/bh0085/synql.git
>
>cd synql
>
>paster serve --reload development.ini

Before that, you'll have to set an environment variable telling the server where to store output from the daemon that it runs in the background listing tweets:

> export SYNQL_DAEMON_ROOT=[some writeable directory here]

> export PATH=$PATH:[synql-path]/synql/scripts

in **.bashrc**. Then you can navigate your browser to 

>http://localhost:8181/demo

----

If anything fails after that, then I'm probably missing somethingimport . Send me an email and I'll fix it up. Oh right, because I'm not taking advantage of pip, you'll have to install the various dependencies yourself; something like:

>sudo pip install paster, pylons, sqlalchemy



#Thanks#

Many thanks to Adam Marcus!
