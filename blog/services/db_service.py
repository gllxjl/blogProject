from blog.models import Blog
from django.db.models import F

class DBService:
    def get_read_count(self, blog_id):
        blog = Blog.objects.get(id=blog_id)
        return blog.read_count

    def update_read_count(self, blog_id, count):
        Blog.objects.filter(id=blog_id).update(read_count=count)

    def increment_read_count(self, blog_id):
        Blog.objects.filter(id=blog_id).update(read_count=F('read_count') + 1)
