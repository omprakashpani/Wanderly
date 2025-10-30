from flask import Flask, render_template, request, redirect, url_for, session, flash
from modules.db import query_one, query_all, execute, close_db

app = Flask(__name__)
app.secret_key = "wandely_dev_secret_change_me"

@app.route('/')
def home():
    from modules.monasteries import get_monasteries
    monasteries = get_monasteries(limit=6)
    return render_template('home.html', monasteries=monasteries)

@app.route('/foods')
def foods_page():
    from modules.foods_cuisines import get_foods, get_cuisines
    foods = get_foods()
    cuisines = get_cuisines()
    return render_template('foods_cuisines.html', foods=foods, cuisines=cuisines)

@app.route('/monasteries')
def monasteries_page():
    from modules.monasteries import get_monasteries
    monasteries = get_monasteries(limit=100)
    return render_template('monasteries.html', monasteries=monasteries)

@app.route('/community')
def community_page():
    from modules.trips import get_trips
    trips = get_trips()
    return render_template('community.html', trips=trips)

@app.route('/trip/<int:trip_id>', methods=['GET','POST'])
def trip_detail(trip_id):
    from modules.trips import get_trip_by_id
    from modules.comments import get_comments, add_comment
    trip = get_trip_by_id(trip_id)
    if not trip:
        return "Trip not found", 404
    if request.method == 'POST':
        if 'user_id' not in session:
            flash('Please login to post comments.')
            return redirect(url_for('login'))
        comment = request.form.get('comment','').strip()
        if comment:
            add_comment(trip_id, session['user_id'], comment)
            return redirect(url_for('trip_detail', trip_id=trip_id))
    comments = get_comments(trip_id)
    return render_template('trip_detail.html', trip=trip, comments=comments)

@app.route('/trip-planner', methods=['GET','POST'])
def trip_planner():
    from modules.trip_planner import save_plan, recent_plans
    from modules.monasteries import get_monasteries
    if request.method == 'POST':
        if 'user_id' not in session:
            flash('Please login to save a plan.')
            return redirect(url_for('login'))
        user_id = session['user_id']
        trip_name = request.form.get('trip_name') or 'My Trip'
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        monasteries = request.form.getlist('monasteries') or []
        preferences = request.form.get('preferences','')
        mons_csv = ",".join(monasteries)
        save_plan(user_id, trip_name, start_date, end_date, mons_csv, preferences)
        flash('Plan saved.')
        return redirect(url_for('trip_planner'))
    monasteries = get_monasteries(limit=100)
    plans = []
    if 'user_id' in session:
        plans = recent_plans(session['user_id'])
    return render_template('trip_planner.html', monasteries=monasteries, plans=plans)

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username','').strip()
        password = request.form.get('password','').strip()
        if not username or not password:
            flash('Username and password required.')
            return render_template('signup.html')
        if query_one('SELECT id FROM users WHERE username=%s', (username,)):
            flash('Username already taken.')
            return render_template('signup.html')
        execute('INSERT INTO users (username,password) VALUES (%s,%s)', (username, password))
        flash('Account created. Please login.')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username','').strip()
        password = request.form.get('password','').strip()
        user = query_one('SELECT * FROM users WHERE username=%s AND password=%s', (username, password))
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Logged in successfully.')
            return redirect(url_for('home'))
        flash('Invalid credentials.')
        return render_template('login.html')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out.')
    return redirect(url_for('home'))

@app.route('/delete-account', methods=['GET','POST'])
def delete_account():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        uid = session['user_id']
        execute('DELETE FROM users WHERE id=%s', (uid,))
        session.clear()
        flash('Account deleted.')
        return redirect(url_for('home'))
    return render_template('delete_account.html')

@app.teardown_appcontext
def teardown_db(exception):
    close_db()

if __name__ == '__main__':
    app.run(debug=True)
