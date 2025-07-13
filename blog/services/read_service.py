import threading
from .cache_service import CacheService
from .db_service import DBService

class ReadService:
    def __init__(self):
        self.cache = CacheService()
        self.db = DBService()

    def increase_read_count(self, blog_id):
        try:
            count = self.cache.get_read_count(blog_id)
            if count is not None:
                self.cache.incr_read_count(blog_id)
            else:
                db_count = self.db.get_read_count(blog_id)
                self.cache.set_read_count(blog_id, db_count + 1)
        except Exception as e:
            print(f"[WARN] Redis异常：{e}，降级为数据库操作")
            self.db.increment_read_count(blog_id)

        threading.Thread(target=self._async_db_update, args=(blog_id,)).start()

    def _async_db_update(self, blog_id):
        try:
            count = self.cache.get_read_count(blog_id)
            if count is not None:
                self.db.update_read_count(blog_id, int(count))
        except Exception as e:
            print(f"[ERROR] 异步数据库更新失败：{e}")
