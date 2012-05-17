import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from synql.lib.base import BaseController, render
from synql.scripts import freebase_utils as fbu, tweeql_synql, ows_tools
import synql.scripts.tweeql_econtains as tweeql_econtains


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
    def infoBandName(self):
        '''
        This simply returns a preset list of  bands and the aliases 
        that they will run with in tweeql.
        
        Note that this returns an empty list: the intended use of the 
        band-names presets right now is to select a band name from
        the freebase/jquery autocomplete.

        '''
        
        return json.dumps({'options':[]})

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

    def infoPersonName(self):
        '''
        ... Same as infoBandName
        '''
        return json.dumps({'options':[]})

    def infoFoodName(self):
        '''
        ... Same as info BandName
        '''
        raise Exception()

    #Runners...
    #These take a user's selection of band name, collection etc
    def runBandName(self):
        '''
        Given a band name, call tweeql with ECONTAINS band:{name}. 

        Tweeql will call freebase_utils to grab the list of aliases for name
        in the same fashion as infoBandName does.
        '''

        p = request.params
        name = p['name']
        econtains = 'band:{0}'.format(name)
        written = tweeql_econtains.setAliasesIfNeeded(econtains,data = json.loads(p['data']), reset = True) 

        state = tweeql_synql.launchECONTAINS(econtains)
        out = {
            'params':{
                'name':name,
                'aliases':written['aliases']
                },
            'written':written,
            'state':state
            }
        return json.dumps(out)
    def runBandCollectionName(self):
        '''
        ... Same as the above with ECONTAINS bandcollection:{name}.
        '''

        p = request.params
        #expected aliases is not required, just allows us to 
        #funnel data forward.
        expected_aliases = p.get('aliases', [])
        name = p['name']
        state = tweeql_synql.launchECONTAINS('bandcollection:{0}'.format(name))
        
        out = {
            'params':{
                'name':name,
                'aliases':expected_aliases,
                },
            'state':state
            }
        return json.dumps(out)

    def runPersonName(self):
        '''
        ... Same as the above with ECONTAINS person:{name}.
        '''
        p = request.params
        name = p['name']
        econtains = 'person:{0}'.format(name)
        written = tweeql_econtains.setAliasesIfNeeded(econtains,data = json.loads(p['data']),reset = True)         
        state = tweeql_synql.launchECONTAINS(econtains)
        out = {
            'params':{
                'name':name,
                'aliases':written['aliases']
                },
            'written':written,
            'state':state
            }
        return json.dumps(out)


    def runFoodGenre(self):
        '''
        ... Same as the above with ECONTAINS food:{name}.
        '''

        p = request.params
        #expected aliases is not required, just allows us to
        #funnel data forward.
        expected_aliases = p.get('aliases', [])
        name = p['name']
        state = tweeql_synql.launchECONTAINS('food:{0}'.format(name))
    
        out = {
            'params':{
                'name':name,
                'aliases':expected_aliases,
                },
            'tweeql_state':state
            }
        return json.dumps(out)

    def checkStatus(self):
        last_state = request.params.get('tweeql_state')
        info = tweeql_synql.queryECONTAINS()#last_state = last_state)

        return json.dumps(info)
