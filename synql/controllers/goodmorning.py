import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from synql.lib.base import BaseController, render

log = logging.getLogger(__name__)

class GoodmorningController(BaseController):

    def index(self):
        # Return a rendered template
        #return render('/goodmorning.mako')
        # or, return a string
        return render('goodmorning.mako')
