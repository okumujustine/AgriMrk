from app import db, app

from app.models import Base
from app.authentication.models import getUser, User

class Blog(Base):
    uid = db.Column(db.BigInteger, db.ForeignKey("user.id"))
    user = db.relationship('User', foreign_keys=uid)
    banner = db.Column(db.String(200), nullable=False, default = 'image.jpg')
    title = db.Column(db.String(256))
    content = db.Column(db.Text)



def getBlogs(page):
    blogs = Blog.query.order_by(Blog.date_created.asc()).paginate(page, 20, False)
    return [{"id": i.id, "title": i.title, "content": i.content, "banner": i.banner, "date_created": i.date_created, "user": getUser(i.uid), "comment_count":getCommentsCount(i.id), "seen_count":getBlogsSeenCount(i.id)} for i in blogs.items]

def getUserBlogs(uid):
    blogs = Blog.query.all()
    return [{"id": item.id, "userid": item.user_id, "title": item.title, "content": item.content} for item in filter(lambda i: i.user_id == uid, blogs)]

def addBlog(title, content, uid, blog_banner):
    if (title and content and uid and blog_banner):
        try:
            user = list(filter(lambda i: i.id == uid, User.query.all()))[0]
            blog = Blog(title=title, content=content, user=user, banner=blog_banner)
            db.session.add(blog)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False
    else:
        return False

def delBlog(blog_id):
    try:
        blog = Blog.query.get(blog_id)
        db.session.delete(blog)
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False

class Comments(Base):
    uid = db.Column(db.BigInteger, db.ForeignKey("user.id"))
    user = db.relationship('User', foreign_keys=uid)
    bid = db.Column(db.BigInteger, db.ForeignKey("blog.id"))
    blog = db.relationship('Blog', foreign_keys=bid)
    comment = db.Column(db.Text)


def getComments(blog_id):
    comments = Comments.query.filter_by(bid=blog_id)
    return [{"id": i.id, "comment": i.comment, "date_created":i.date_created, "user": getUser(i.uid)} for i in comments]

def getCommentsCount(blog_id):
    comments_count = Comments.query.filter_by(bid=blog_id).count()
    return comments_count

def addComment(comment, bid, uid):
    if (uid and comment and bid):
        try:
            user = list(filter(lambda i: i.id == int(uid), User.query.all()))[0]
            
            blog = list(filter(lambda i: i.id == int(bid), Blog.query.all()))[0]

            final_comment = Comments(comment=comment, blog=blog, user=user)
            db.session.add(final_comment)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False
    else:
        return False


class BlogSeen(Base):
    bid = db.Column(db.BigInteger, db.ForeignKey("blog.id"))
    blog = db.relationship('Blog', foreign_keys=bid)
    count = db.Integer()


def addBlogSeen(bid):
    if (bid):
        try:
            
            blog = list(filter(lambda i: i.id == int(bid), Blog.query.all()))[0]

            seen_count = BlogSeen(blog=blog, count=1)
            db.session.add(seen_count)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False
    else:
        return False

def getBlogsSeenCount(blog_id):
    blogs_seen_count = BlogSeen.query.filter_by(bid=blog_id).count()
    return blogs_seen_count
