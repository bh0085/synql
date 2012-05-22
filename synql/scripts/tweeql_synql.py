#!/usr/bin/env python
'''
Helper functions for calling econtains queries.
'''

import subprocess as spc
import time, os, signal, inspect
import sys, json
TABLENAME = 'synql'
DAEMON_CWD = os.environ['SYNQL_DAEMON_ROOT']
if not os.path.isdir(DAEMON_CWD):
    os.makedirs(TWEEQL_CWD)
TWEEQL_CWD = os.path.dirname(inspect.stack()[0][1])


class TimeoutInterrupt(Exception):
    def __init__(self,**args):
        Exception.__init__(self, **args)

import time
def launchECONTAINS(econtains):
    global TWEEQL_CWD, TABLENAME

    starttime = time.time()
    #sorry but for the moment, we just hand a single process and will fail if
    #that's not the case.
    
    cwd = DAEMON_CWD
    command = '''"SELECT text FROM twitter INTO TABLE {1} WHERE text ECONTAINS '{0}';"'''.format(econtains, TABLENAME)

    #trundir = os.path.dirname(inspect.stack()[0][0]),
                            
    tweets_file = os.path.join(cwd, 'tweets.txt')
    status_file = os.path.join(cwd, 'status.txt')
    params_file = os.path.join(cwd, 'params.json')
    
    #clean tweets/status before any querying.
    if os.path.isfile(tweets_file):
        os.remove(tweets_file)
    if os.path.isfile(status_file):
        os.remove(status_file)

    #write lock and status files
    lock_file = os.path.join(cwd,'lock.txt')
    if os.path.isfile(lock_file):
        with open(lock_file,'r') as f: 
            lock_pids = [int(l) for l in json.loads(f.read())]
        for lock_pid in lock_pids:
            try:
                os.kill(lock_pid, signal.SIGTERM)
            except OSError:
                print 'Process already killed, moving on.'
        

    with open(status_file, 'w') as f: f.write('initializing')
    with open(tweets_file, 'w') as f: f.write(json.dumps([]))
    with open(params_file, 'w') as f: f.write(json.dumps({'query':econtains,
                                                          'start_time':starttime}))

    
    prc_tweeql = spc.Popen('tweeql-launch-query.py {0}'.format( command), 
                           shell = True,
                           cwd = TWEEQL_CWD
                           )

    prc_eavesdropper =spc.Popen('tweeql-eavesdrop.py -r -o {0} -t {1}'.\
                                    format(tweets_file,TABLENAME),
                                shell = True,
                                cwd = TWEEQL_CWD
                                )
    prc_eavesdropper = prc_tweeql

    #write subprocess PIDs to a file so that they can be killed if the
    #webserver goes away or makes a new request
    with open(lock_file, 'w') as f: 
        f.write(json.dumps([p.pid for p in [prc_tweeql, prc_eavesdropper]]))
    with open(status_file, 'w') as f: f.write('streaming')
    return {
        'outfile':tweets_file
        }


def queryECONTAINS():         
    cwd = DAEMON_CWD
    tweets_file = os.path.join(cwd, 'tweets.txt')
    status_file = os.path.join(cwd, 'status.txt')
    params_file = os.path.join(cwd, 'params.json')
    
    if not os.path.isfile(status_file):
        return {'status':'uninitialized',
                'params':{},
                'tweets':['']}

    with open(status_file, 'r') as f: status = f.read()
    with open(tweets_file, 'r') as f: tweets =json.loads(f.read())
    with open(params_file, 'r') as f: params =json.loads(f.read())
    
    return  {
        'status':status,
        'params':params,
        'tweets':tweets
        }
    

if __name__ == '__main__':
    launchECONTAINS('person:Barack Obama')
