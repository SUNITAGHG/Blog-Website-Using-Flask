from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import os

app = Flask(__name__, static_url_path='/static')

posts = [
]

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html', posts=posts)


@app.route('/post/<int:post_id>')
def post_detail(post_id):
    post = next((p for p in posts if p['id'] == post_id), None)
    if post:
        return render_template('posts/post_detail.html', post=post)
    return "Post not found"


@app.route('/new_post')
def new_post():
    return render_template('new_post.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/add_post', methods=['POST'])
def add_post():
    title = request.form.get('title')
    content = request.form.get('content')
    image_path = None

    if 'image' in request.files:
        image = request.files['image']
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_path = os.path.join('uploads', filename)

    new_post = {"id": len(posts) + 1, "title": title, "content": content, "image_path": image_path, "likes": 0}
    posts.append(new_post)

    return redirect(url_for('index'))


@app.route('/like_post/<int:post_id>', methods=['POST'])
def like_post(post_id):
    post = next((p for p in posts if p['id'] == post_id), None)
    if post:
        post['likes'] += 1
        return jsonify({'likes': post['likes']})
    return jsonify({'error': 'Post not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)
