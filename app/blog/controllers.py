from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.blog.models import Blog, getBlogs, addBlog, delBlog

blog = Blueprint('blog', __name__)

@blog.route('/')
def index():
    return jsonify(getBlogs()), 200


@blog.route("/add", methods=["POST", "GET"])
# @jwt_required
def add_blog():
    try:
        current_user = get_jwt_identity()
        title = request.json["title"]
        content = request.json["content"]
        # uid = current_user["id"]
        uid = 11
  
        addBlog(title, content, uid)
        return jsonify({"success": "true"})
    except Exception as e:
        print(e)
        return jsonify({"error": "Invalid form"})


@blog.route("/delete", methods=["POST", "GET"])
# @jwt_required
def delete_blog():
    try:
        blog_id = request.args.get('blog_id')
        delBlog(blog_id)
        return jsonify({"success": "deleted"}),200
    except Exception as e:
        return jsonify({"error": "Server error"}), 5000