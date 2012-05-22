# Twitter authentication information
TWITTER_USERNAME = "bh0085"
TWITTER_PASSWORD = "twitterpassword"

# set to a database URI according to sqlalchemy's scheme for the database to dump stored tweets into
DATABASE_URI = "sqlite:///test.db"
# to send parameters to the connection argument, set the DATABASE_URI to
# the database protocol you want (e.g. "postgresql://") and then uncomment
# and fill in the following DATABASE_CONFIG
#
#DATABASE_CONFIG = {
#    'database':'',
#    'host':'',
#    'user':'',
#    'password':''
#}

# batch size of database writes
# smaller values allow the web server to "stream" sparse queries from the DB
DATABASE_BATCHSIZE = 20

# specify a directory for ECONTAINS to store tweets
# if you want to use ECONTAINS, you'll want to set this.
ECONTAINS_DATADIR = '/data/econtains'

# add any desired user-defined econtains extensions
# ECONTAINS_TYPE_EXTENSIONS = {movies:'tweeql.econtains.extensions.movies'}

# configure tweeql-eavesdrop.py - in case you want to run synQL web for example.
EAVESDROPPING_COUNT = 100  # number of results to print per broadcast
EAVESDROPPING_DELAY = 1    # delay between broadcasts

# Running in debug mode, the system prints a lot more information
DEBUG = False

# set to a database URI according to sqlalchemy's scheme for the database to allow 
# various operators use as scratch space
SCRATCHSPACE_URI = "sqlite:///scratch.db"
# what prefix should tables used for scratchspace get
SCRATCHSPACE_PREFIX = "tweeql_scratch__"
