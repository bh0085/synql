'''
Demo powering the SynQL web metacritic. 

/index 
 Serves the page

/getQueryTypes 
 Yields a list of the predefined types that tweeql is expected
 to know how to expand.

/info[...]
 Yields info for a given type, a list of options that when returned
 allows the user to select an instance of "type" for streaming.

/run[...]
 Launches a stream with tweeql, sets up an instance of the eavesdropper
 to report tweets.

'''

import logging
from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from synql.lib.base import BaseController, render
from tweeql.econtains import freebase_utils as fbu
from synql.scripts import tweeql_synql, ows_tools

import json

log = logging.getLogger(__name__)

class DemoController(BaseController):

    def index(self):
        # Return a rendered template
        #return render('/demo.mako')
        # or, return a string
        return render('demo.mako')

    def cityLLs(self):
        return json.dumps(ows_tools.city_lls())

    def getQueryTypes(self):
        query_types = {
            'band':{
                "title":"Bands",
                "description":"Create a twitter feed filtering tweets related to a band",
                "infoFun":'infoBandName',
                "runFun":'runBandName',
                },
            'bandcollection':{
                "title":"Band Collections",
                "description":"Create a twitter feed filtering tweets related to any band in some collection of bands, eg: Every artist at the Bonnaroo! music festival",
                "infoFun":'infoBandCollectionName',
                "runFun":'runBandCollectionName',
                },
            'person':{
                "title":"People",
                "description":"Create a twitter feed filtering tweets related to a person or family", 
                "infoFun":'infoPersonName',
                "runFun":'runPersonName'
                },
            'food':{
                "title":"Foods",
                "description":"Create a twitter feed filtering tweets fitting into one or multiple genres of food",
                "infoFun":"infoFoodName",
                "runFun":"runFoodName"
                }
            }
        return json.dumps(query_types)

    #Info funs
    #Displays a list of querying options for the preset run type
    #If no list is available, returns an dict having and empty array, options.

    #Generic types.
    def infoEcontainsType(self,type):
        return json.dumps({'options':[]})
    def infoBandName(self):
        return self.infoEcontainsType('band');
    def infoPersonName(self):
        return self.infoEcontainsType('person')
    def infoFoodName(self):
        return self.infoEcontainsType('food')
    
    #Predefined type.
    def infoBandCollectionName(self):
        '''
        Similar to the above, agglomerates aliases from band 
        collections to return a preset list of band collections
        and the sum of aliases that each will run with

        input (GET params):
        {
        name:[string] -- the band collection name to run an econtains query for.
        }
        '''
        p = request.params
        allowed= fbu.allowedBandCollectionNames()        
        data = {}
        data['options'] = []
        for name in allowed:
            aliases = fbu.getBandCollectionAliases(list = name)
            data['options'].append({'name':name,
                                    'aliases':aliases})
        return json.dumps(data)

    #Runners...
    #These take a user's selection of band name, collection etc

    #Generic types. (everything!)
    def runBandCollectionName(self):
        return self.runEcontainsType('bandcollection', request.params['name'])
    def runPersonName(self):
        return self.runEcontainsType('person',request.params['name'])
    def runBandName(self):
        return self.runEcontainsType('band',request.params['name'])
    def runFoodGenre(self):
        return self.runEcontainsType('food',request.params['name'])
    def runEcontainsType(self,type,key):
        p = request.params
        name = p['name']
        econtains = '{0}:{1}'.format(type,key)
        state = tweeql_synql.launchECONTAINS(econtains)
        out = {
            'params':{
                'name':name
                },
            'state':state
            }
        return json.dumps(out)
        

    def checkStatus(self):
        last_state = request.params.get('tweeql_state')
        info = tweeql_synql.queryECONTAINS()
        return json.dumps(info)
