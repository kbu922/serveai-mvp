import os
import random
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from models import db, User, ForumPost, Comment, RacketListing

app = Flask(__name__)
app.config['SECRET_KEY'] = 'serve-ai-secret-key-123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///serve_ai.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'

db.init_app(app)

with app.app_context():
    db.create_all()

def calculate_ntrp(score):
    if score >= 85:
        return "4.5+"
    elif score >= 75:
        return "4.0"
    elif score >= 65:
        return "3.5"
    else:
        return "3.0"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        action = request.form.get('action')
        username = request.form.get('username')
        password = request.form.get('password')

        if action == 'register':
            email = request.form.get('email')
            if User.query.filter_by(username=username).first():
                flash('Username already exists.', 'danger')
            else:
                new_user = User(username=username, email=email, password=password)
                db.session.add(new_user)
                db.session.commit()
                session['user_id'] = new_user.id
                session['username'] = new_user.username
                flash('Registration successful!', 'success')
                return redirect(url_for('analysis_and_match'))

        elif action == 'login':
            user = User.query.filter_by(username=username, password=password).first()
            if user:
                session['user_id'] = user.id
                session['username'] = user.username
                flash('Logged in successfully!', 'success')
                return redirect(url_for('analysis_and_match'))
            else:
                flash('Invalid credentials.', 'danger')

    return render_template('auth.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('index'))

@app.route('/analysis', methods=['GET', 'POST'])
def analysis_and_match():
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('auth'))
        
    current_user = User.query.get(session['user_id'])
    if not current_user:
        session.pop('user_id', None)
        flash('Session expired. Please log in again.', 'warning')
        return redirect(url_for('auth'))

    matched_players = []

    if request.method == 'POST':
        if 'video' in request.files:
            file = request.files['video']
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                ai_score = random.randint(62, 95)
                ntrp = calculate_ntrp(ai_score)

                current_user.skill_score = ai_score
                current_user.ntrp_level = ntrp
                current_user.uploaded_video = filepath
                db.session.commit()
                flash('Video analyzed successfully! Skill level updated.', 'success')

    if current_user.skill_score and current_user.skill_score > 0:
        matched_players = User.query.filter(
            User.id != current_user.id,
            User.skill_score.between(current_user.skill_score - 12, current_user.skill_score + 12)
        ).order_by(User.skill_score.desc()).limit(200).all()

    return render_template('analysis.html', user=current_user, matches=matched_players)

@app.route('/forum', methods=['GET', 'POST'])
def forum():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        author = session.get('username', 'Anonymous')
        
        new_post = ForumPost(title=title, content=content, author=author)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('forum'))
        
    posts = ForumPost.query.order_by(ForumPost.id.desc()).all()
    return render_template('forum.html', posts=posts)

@app.route('/marketplace', methods=['GET', 'POST'])
def marketplace():
    if 'user_id' not in session:
        flash('Please log in to access the marketplace.', 'warning')
        return redirect(url_for('auth'))

    if request.method == 'POST':
        title = request.form.get('title')
        brand = request.form.get('brand')
        price = request.form.get('price')
        condition = request.form.get('condition')
        description = request.form.get('description')
        seller_contact = request.form.get('seller_contact')

        new_item = RacketListing(
            title=title,
            brand=brand,
            price=int(price) if price else 0,
            condition=condition,
            description=description,
            seller_contact=seller_contact
        )
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('marketplace'))

    listings = RacketListing.query.order_by(RacketListing.id.desc()).all()
    return render_template('marketplace.html', listings=listings)

if __name__ == '__main__':
    app.run(debug=True)
