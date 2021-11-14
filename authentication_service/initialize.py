import redis

# pool = redis.ConnectionPool(host='redis-authentication-service', port=6379, decode_responses=True)
pool = redis.ConnectionPool(host='localhost', port=6383, decode_responses=True)
db = redis.Redis(connection_pool=pool)
db.hset("user", "comp3122", "comp3122")