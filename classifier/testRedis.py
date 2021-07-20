# import redis
# rs = redis.Redis("localhost:6380")
# rs.ping()
# print (rs)
# https://stackabuse.com/asynchronous-tasks-using-flask-redis-and-celery

from redis import Redis
redis = Redis(host='localhost', port=6379)
redis.incr('hits')
redis.get('hits')
redis.ping()
print (redis.ping())
