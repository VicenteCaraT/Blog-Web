from flask import (
    render_template, Blueprint, flash, g, redirect, request, url_for
)
#manejo de errores
from werkzeug.exceptions import abort

from myblog.models.post import Post
from myblog.models.user import User

from myblog.views.auth import login_required
from myblog import db

blog = Blueprint('blog', __name__)

#Obtener un usuario
def get_user(id):
    user = User.query.get_or_404(id)
    return user

#Litar todos los Post

@blog.route('/')
def index():
    posts = Post.query.all()
    db.session.commit()
    return render_template('blog/index.html', posts = posts, get_user=get_user)

@blog.route('/blog/create', methods=['GET','POST'])
@login_required
def create():
    if request.method == 'POST':
        #capturar datos de POST
        title = request.form.get('title')
        body = request.form.get('body')

        post =Post(g.user.id, title, body)

        error = None
        if not title:
            error = 'Se requiere un título'
        if error is not None:
            flash(error)
        else:
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('blog.index'))
        
        flash(error)

    return render_template('blog/create.html')