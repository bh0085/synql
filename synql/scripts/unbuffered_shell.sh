#!/usr/bin/env bash
sleep .5
echo 'hi'
sleep .5
python -c 'import time, sys; print "p1";sys.stdout.flush(); time.sleep(3); print "p2";'
sleep 1
echo 'hello'