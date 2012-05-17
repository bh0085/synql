# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 6
_modified_time = 1337176948.41149
_template_filename='/Users/bh0085/Programming/class/db/project/synql/synql/templates/demo.mako'
_template_uri='demo.mako'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding='utf-8'
from webhelpers.html import escape
_exports = []


def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'<html>\n<head>\n<link rel="stylesheet" href="/css/jquery.tooltip.css" />\n<link rel="stylesheet" href="/css/demo.css" />\n<link rel="stylesheet" href="/css/suggest.css" />\n<script src="/js/jquery.min.js"></script>\n<script src="/js/jquery.tooltip.min.js"></script>\n<script src="/js/demo.js"></script>\n<script src="/js/map.js"></script>\n<script src="/js/suggest.min.js"></script>\n\n\n<meta name="viewport" content="initial-scale=1.0, user-scalable=no" />\n<meta http-equiv="content-type" content="text/html; charset=UTF-8"/>\n<title>Google Maps JavaScript API v3 Example: KmlLayer KML</title>\n<script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>\n\n\n</head>\n<body>\n<div id=content>\n</div>\n<div id=footer>\n<div id=map_canvas></div>\n</div>\n</body>\n</html>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


