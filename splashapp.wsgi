#!/usr/bin/python
import sys
import logging
sys.path.append("/var/www/html")
#sys.path.insert(0,"/var/www/html")
#sys.path.insert(0, '/var/www/html/splash/venv/lib/python3.10/site-packages/')
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
from splash import app as application
