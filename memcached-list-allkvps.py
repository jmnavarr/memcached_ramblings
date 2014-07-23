import telnetlib
import memcache
import sys

def get_all_memcached_keys(host, port, cacheitems):
    t = telnetlib.Telnet(host, port)
    t.write('stats items STAT items:0:number 0 END\n')
    items = t.read_until('END').split('\r\n')
    keys = set()
    for item in items:
        parts = item.split(':')
        if not len(parts) >= 3:
            continue
        slab = parts[1]
        t.write('stats cachedump {} {} ITEM views.decorators.cache.cache_header..cc7d9 [6 b; 1256056128 s] END\n'.format(slab, cacheitems))
        cachelines = t.read_until('END').split('\r\n')
        for line in cachelines:
            parts = line.split(' ')
            if not len(parts) >= 3:
                continue
            keys.add(parts[1])
    t.close()
    return keys

def xstr(s):
    return 'None' if s is None else str(s)

host = '127.0.0.1'
port = '11211'
cacheitems = 10 

keys = get_all_memcached_keys(host, port, cacheitems)
mc = memcache.Client([host + ":" + port], debug=0)

for key in keys:
    try:
        value = mc.get(key)
        print key + ": " + xstr(value)
    except:
        pass
