#!/usr/bin/env python
import sys,os
import subprocess as spc
import time
def parent():
    print 'parenting'
    prc = spc.Popen(['/Users/bh0085/db/synql/synql/scripts/unbuffered.py', 'child'],
                    shell = True,
                    stdout = spc.PIPE)

    line = prc.stdout.readline()
    while line:
        print 'looping'
        print line
        line = prc.stdout.readline()
def child():
    print 'childing'
    for i in range(10):
         print 'hello! {0}'.format(i)
         time.sleep(.5)
         sys.stdout.flush()
        
if __name__ == '__main__':
    print 'name = main'
    args = sys.argv[1:]
    if len(args) < 1:
        child()
    elif args[0] == 'parent':
        parent()
    else:
        child()


    exit(0)
