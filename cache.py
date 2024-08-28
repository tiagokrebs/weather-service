from pymemcache.client import base
import json

# docker pull memcached
# docker run -d --name memcached -p 11211:11211 memcached
memcache_client = base.Client(('memcached', 11211))
# memcache_client = base.Client(('localhost', 11211))

def get_cache(key):
    cached_response = memcache_client.get(key)
    if cached_response:
        return json.loads(cached_response)
    return None

def set_cache(key, data, expire=3600):
    memcache_client.set(key, json.dumps(data), expire=expire)