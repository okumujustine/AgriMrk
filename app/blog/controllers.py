from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import secrets

from app import app, db, photos
from app.blog.models import (Blog, getBlogs, addBlog, delBlog, addComment, getComments, addBlogSeen, getBlogsFiltered)
from app.helper_functions import (token_required, admin_required, agronomist_required, error_return)

blog = Blueprint('blog', __name__)

@blog.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    title = request.args.get('qtitle')
    
    if not title:
        print("no search query provided",title)
        return jsonify(getBlogs(page)), 200

    print("the search query is staedily avaialable",title)
    return jsonify(getBlogsFiltered(page, title)), 200


@blog.route("/add", methods=["POST", "GET"])
@jwt_required
def add_blog():
    try:
        current_user = get_jwt_identity()
        blog_form = request.form
        title = blog_form["title"]
        content = blog_form["content"]
        uid = current_user["id"]
        banner = request.files['banner']

        if not banner.filename:
            return jsonify(error_return(400, 'Prove banner please!')), 400

        blog_banner = photos.save(banner, name =  secrets.token_hex(10) + '.')
        print("file name "+banner.filename)    
        print(current_user)
        try:
            addBlog(title, content, uid, blog_banner)
        except:
            print("Failed to add blog, try again later!")
            return jsonify(error_return(400, 'Failed to add blog, try again later!')), 400
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
@jwt_required
def add_blog_comment():
    try:
        current_user = get_jwt_identity()
        blog_id = request.args.get('blog_id')
        comment = request.json["comment"]
        user_id = current_user["id"]
        addComment(comment, blog_id, user_id)
        return jsonify({"success": "comment added"}),200
    except Exception as e:
        return jsonify({"error": "Server error"}), 5000


@blog.route("/comment", methods=["GET"])
# @jwt_required
def get_blog_comment():
    try:
         blog_id = request.args.get('blog_id')
         addBlogSeen(blog_id)
         return jsonify(getComments(blog_id)), 200
    except Exception as e:
        return jsonify({"error": "Server error"}), 5000
    