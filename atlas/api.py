# Atlas client library
# Copyright 2010-2013 - Seyi Ogunyemi
# See LICENSE for details

import urllib
from types import MethodType

from atlas.error import AtlasError
from atlas.utils import *

BASE_URL = 'https://atlas.metabroadcast.com/3.0/%s.json'

class API(object):
    """Atlas API"""

    def find(self):
        print 'found'

    def __getattr__(self, name):
        try:
            fn = super(API).__getattr__(name)
        except AttributeError:
            fn = makeFunc(name)
            setattr(self, name, MethodType(fn, self))
        return fn
        
def makeFunc(name):
    def call(self, **kw):
        """
        Makes a call to Atlas

        name = Endpoint for Atlas queries
        **kw = Query string arguments to be appended to the base URL
        """
        url = BASE_URL % name
        json = import_simplejson()
        if kw:
            url = url + '?' + urllib.urlencode(kw)
        try:
            response =  urllib.urlopen(url)
        except:
            raise AtlasError("Atlas API IO error")
        mime_type = response.info().type
        if (response and mime_type.startswith('application/') and mime_type.endswith('json')):
            result = json.load(response)
            return result
        else:
            return None
        
    return call
