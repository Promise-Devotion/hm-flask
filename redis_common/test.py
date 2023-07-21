import redis_common

r = redis_common.Redis(host='localhost', port=6379, db=3)
r.set('foo', 'bar')

print(r.append('foo', ' bar'))
print(r.get('foo'))