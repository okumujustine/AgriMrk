from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.blog.models import Blog, getBlogs, addBlog, delBlog, addComment, getComments

blog = Blueprint('blog', __name__)

@blog.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    return jsonify(getBlogs(page)), 200


@blog.route("/add", methods=["POST", "GET"])
@jwt_required
def add_blog():
    try:
        current_user = get_jwt_identity()
        title = request.json["title"]
        content = request.json["content"]
        uid = current_user["id"]
  
        addBlog(title, content, uid)
        return jsonify({"success": "true"})
    except Exception as e:
        print(e)
        return jsonify({"error": "Invalid form"})


@blog.route("/delete", methods=["POST", "GET"])
@jwt_required
def delete_blog():
    try:
        blog_id = request.args.get('blog_id')
        delBlog(blog_id)
        return jsonify({"success": "deleted"}),200
    except Exception as e:
        return jsonify({"error": "Server error"}), 5000


@blog.route("/comment/add", methods=["POST", "GET"])
# @jwt_required
def add_blog_comment():
    try:
        blog_id = request.args.get('blog_id')
        user_id = request.args.get('user_id')
        comment = request.json["comment"]
        addComment(comment, blog_id, user_id)
        return jsonify({"success": "comment added"}),200
    except Exception as e:
        return jsonify({"error": "Server error"}), 5000


@blog.route("/comment", methods=["GET"])
# @jwt_required
def get_blog_comment():
    try:
         blog_id = request.args.get('blog_id')
         return jsonify(getComments(blog_id)), 200
    except Exception as e:
        return jsonify({"error": "Server error"}), 5000
    