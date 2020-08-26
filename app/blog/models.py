from app import db, app

from app.models import Base
from app.authentication.models import getUser, User

class Blog(Base):
    uid = db.Column(db.BigInteger, db.ForeignKey("user.id"))
    user = db.relationship('User', foreign_keys=uid)
    title = db.Column(db.String(256))
    content = db.Column(db.Text)



def getBlogs():
    blogs = Blog.query.all()
    return [{"id": i.id, "title": i.title, "content": i.content, "user": getUser(i.uid)} for i in blogs]

def getUserBlogs(uid):
    blogs = Blog.query.all()
    return [{"id": item.id, "userid": item.user_id, "title": item.title, "content": item.content} for item in filter(lambda i: i.user_id == uid, blogs)]

def addBlog(title, content, uid):
    if (title and content and uid):
        try:
            user = list(filter(lambda i: i.id == uid, User.query.all()))[0]
            blog = Blog(title=title, content=content, user=user)
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