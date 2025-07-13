import redis

class CacheService:
    def __init__(self):
        self.client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        self.key_prefix = 'blog_read_count_'

    def get_read_count(self, blog_id):
        key = self.key_prefix + str(blog_id)
        return self.client.get(key)

    def incr_read_count(self, blog_id):
        key = self.key_prefix + str(blog_id)
        return self.client.incr(key)

    def set_read_count(self, blog_id, count):
        key = self.key_prefix + str(blog_id)
        self.client.set(key, count, ex=3600)

    def delete_read_count(self, blog_id):
        key = self.key_prefix + str(blog_id)
        self.client.delete(key)

    def get_cache_hit_rate(self):
        info = self.client.info()
        hits = info.get('缓存命中：', 0)
        misses = info.get('缓存未命中：', 0)
        total = hits + misses
        return hits / total if total else 0
