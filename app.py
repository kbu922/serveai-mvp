import os
import random
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from models import db, User, Post, Comment

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tennis-serve-ai-secret-key-12345'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tennis_serve_ai.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # Max 100MB upload size

db.init_app(app)

# Create database tables automatically
with app.app_context():
    db.create_all()

# Helper function: NTRP mapping logic
def calculate_ntrp(score):
    if score >= 88:
        return "NTRP 4.5+ (Advanced)"
    elif score >= 78:
        return "NTRP 4.0 (Intermediate-High)"
    elif score >= 68:
        return "NTRP 3.5 (Intermediate)"
    elif score >= 60:
        return "NTRP 3.0 (Solid Rally)"
    else:
        return "NTRP 2.5 (Beginner)"

# -----------------------------------------------------------------------------
# SUBPAGE 1: REGISTER & LOGIN
# -----------------------------------------------------------------------------
@app.route('/', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        action = request.form.get('action')
        
        # Handle Registration
        if action == 'register':
            username = request.form['username'].strip()
            email = request.form['email'].strip()
            password = request.form['password'].strip()
            
            existing_user = User.query.filter(
                (User.username == username) | (User.email == email)
            ).first()
            
            if existing_user:
                flash('Username or Email already registered.', 'danger')
            else:
                new_user = User(username=username, email=email, password=password)
                db.session.add(new_user)
                db.session.commit()
                flash('Registration successful! Please log in.', 'success')
                
        # Handle Login
        elif action == 'login':
            username = request.form['username'].strip()
            password = request.form['password'].strip()
            
            user = User.query.filter_by(username=username, password=password).first()
            if user:
                session['user_id'] = user.id
                session['username'] = user.username
                flash(f'Welcome back, {user.username}!', 'success')
                return redirect(url_for('analysis_and_match'))
            else:
                flash('Invalid username or password.', 'danger')
                
    return render_template('auth.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('auth'))

# -----------------------------------------------------------------------------
# SUBPAGE 2: AI VIDEO ANALYSIS & PLAYER MATCHMAKING
# -----------------------------------------------------------------------------
@app.route('/analysis', methods=['GET', 'POST'])
def analysis_and_match():
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('auth'))
        
    current_user = User.query.get(session['user_id'])
    matched_players = []

    if request.method == 'POST':
        if 'video' in request.files:
            file = request.files['video']
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                # Simulated AI Technique Analysis Engine
                ai_score = random.randint(62, 95)
                ntrp = calculate_ntrp(ai_score)

                current_user.skill_score = ai_score
                current_user.ntrp_level = ntrp
                current_user.uploaded_video = filepath
                db.session.commit()
                flash('Video analyzed successfully! Skill level updated.', 'success')

    # Matchmaking Engine: Fetch users with skill level within +-12 points
    if current_user.skill_score > 0:
        matched_players = User.query.filter(
            User.id != current_user.id,
            User.skill_score.between(current_user.skill_score - 12, current_user.skill_score + 12)
        ).order_by(User.skill_score.desc()).limit(200).all()

    return render_template('analysis.html', user=current_user, matches=matched_players)

# -----------------------------------------------------------------------------
# SUBPAGE 3: DISCUSSION ZONE & COMMENTS
# -----------------------------------------------------------------------------
@app.route('/forum', methods=['GET', 'POST'])
def forum():
    if 'user_id' not in session:
        flash('Please log in to access the discussion forum.', 'warning')
        return redirect(url_for('auth'))

    if request.method == 'POST':
        action = request.form.get('action')
        
        # Post a new discussion thread
        if action == 'create_post':
            title = request.form['title'].strip()
            content = request.form['content'].strip()
            if title and content:
                new_post = Post(title=title, content=content, user_id=session['user_id'])
                db.session.add(new_post)
                db.session.commit()
                flash('Discussion post published!', 'success')
                
        # Comment on an existing thread
        elif action == 'create_comment':
            content = request.form['comment_content'].strip()
            post_id = request.form['post_id']
            if content and post_id:
                new_comment = Comment(content=content, post_id=post_id, user_id=session['user_id'])
                db.session.add(new_comment)
                db.session.commit()
                flash('Comment added!', 'success')

    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('forum.html', posts=posts)

if __name__ == '__main__':
    app.run(debug=True)
