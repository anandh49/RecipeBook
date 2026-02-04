import sqlite3
import os
import bcrypt
import re
from functools import wraps
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session, abort
from werkzeug.utils import secure_filename

# --- CONFIGURATION & PATHS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "recipebook.db")
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")
UPLOAD_FOLDER = os.path.join(STATIC_DIR, 'images')

app = Flask(__name__, template_folder=TEMPLATE_DIR)
app.secret_key = "recipebook"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
MEAL_TYPES = ["Breakfast", "Brunch", "Lunch", "Dessert", "Dinner", "Drinks"]

# --- SECURITY DECORATOR ---
def admin_required(f):
    """Decorator to protect admin routes from unauthorized access."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            flash("Access denied. Admin privileges required.", "danger")
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

# --- DATABASE SETUP ---
def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # 1. Users Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        is_admin INTEGER DEFAULT 0
    )''')

    # Ensure admin user exists
    cursor.execute("SELECT * FROM users WHERE is_admin = 1")
    if not cursor.fetchone():
        admin_pass = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        cursor.execute("INSERT INTO users (username, password, email, is_admin) VALUES (?, ?, ?, ?)",
                       ("admin_secure", admin_pass, "admin@recipebook.com", 1))

    # 2. Recipes Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        slug TEXT NOT NULL UNIQUE,
        title TEXT NOT NULL,
        description TEXT,
        image_url TEXT,
        video_url TEXT,
        prep_time TEXT,
        meal_type TEXT,
        category TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')

    # 3. Ingredients Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS ingredients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipe_id INTEGER,
        item_text TEXT,
        FOREIGN KEY(recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
    )''')

    # 4. Instructions Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS instructions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipe_id INTEGER,
        step_text TEXT,
        step_order INTEGER,
        FOREIGN KEY(recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
    )''')

    # 5. Nutrition Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS nutrition (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipe_id INTEGER,
        name TEXT,
        value_text TEXT,
        value_int INTEGER,
        FOREIGN KEY(recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
    )''')

    # 6. Extra Info
    cursor.execute('''CREATE TABLE IF NOT EXISTS extra_info (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipe_id INTEGER,
        info_type TEXT,
        content TEXT,
        FOREIGN KEY(recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
    )''')

    # 7. Comments
    cursor.execute('''CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipe_id INTEGER,
        comment TEXT,
        username TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
    )''')

    # 8. Likes
    cursor.execute('''CREATE TABLE IF NOT EXISTS likes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipe_id INTEGER,
        username TEXT,
        UNIQUE(recipe_id, username),
        FOREIGN KEY(recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
    )''')

    conn.commit()
    conn.close()

init_db()

# --- HELPER FUNCTIONS ---
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_int(text):
    if not text: return 0
    nums = re.findall(r"\d+", text)
    return int(nums[0]) if nums else 0

def create_slug(title):
    return title.lower().strip().replace(" ", "-").replace("_", "-")

def get_recipe_full_data(recipe_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT item_text FROM ingredients WHERE recipe_id=?", (recipe_id,))
    ingredients = [r['item_text'] for r in cur.fetchall()]
    cur.execute("SELECT step_text FROM instructions WHERE recipe_id=? ORDER BY step_order ASC", (recipe_id,))
    instructions = [r['step_text'] for r in cur.fetchall()]
    cur.execute("SELECT name, value_text FROM nutrition WHERE recipe_id=?", (recipe_id,))
    nutrition = {r['name']: r['value_text'] for r in cur.fetchall()}
    cur.execute("SELECT content FROM extra_info WHERE recipe_id=? AND info_type='fun'", (recipe_id,))
    fun_facts = [r['content'] for r in cur.fetchall()]
    cur.execute("SELECT content FROM extra_info WHERE recipe_id=? AND info_type='tip'", (recipe_id,))
    tips = [r['content'] for r in cur.fetchall()]
    conn.close()
    return {'ingredients': ingredients, 'instructions': instructions, 'nutrition': nutrition, 'fun_facts': fun_facts, 'tips': tips}

# --- AUTH ROUTES ---
@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET': return redirect(url_for('home'))
    username = request.form['username']
    password = request.form['password']

    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE LOWER(username) = LOWER(?)', (username,))
    user = cur.fetchone()
    conn.close()

    if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['is_admin'] = (user['is_admin'] == 1)

        if session['is_admin']:
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('main'))
    else:
        flash('Invalid username or password.', 'danger')
        return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET': return render_template('register.html')
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    conn = get_db()
    try:
        conn.execute('INSERT INTO users (username, password, email, is_admin) VALUES (?, ?, ?, ?)', (username, hashed_password, email, 0))
        conn.commit()
        return redirect(url_for('home'))
    except Exception as e:
        flash("Registration failed. Email or Username may already exist.", "danger")
        return redirect(url_for('register'))
    finally:
        conn.close()

@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    if request.method == 'GET': return render_template('forgot.html')
    email = request.form.get('email')
    new_pass = request.form.get('new_password')
    confirm_pass = request.form.get('confirm_password')
    if new_pass != confirm_pass:
        flash("Passwords do not match.", "danger")
        return redirect(url_for('forgot'))
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE LOWER(email) = LOWER(?)', (email,))
    user = cur.fetchone()
    if user:
        hashed_password = bcrypt.hashpw(new_pass.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        cur.execute('UPDATE users SET password = ? WHERE id = ?', (hashed_password, user['id']))
        conn.commit()
        conn.close()
        flash("Password updated successfully. Please login.", "success")
        return redirect(url_for('home'))
    else:
        conn.close()
        flash("Email not found!", "danger")
        return redirect(url_for('forgot'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# --- MAIN ROUTES ---
@app.route('/main')
def main():
    if 'user_id' not in session: return redirect(url_for('home'))
    conn = get_db()
    categories = ['Dessert', 'Breakfast', 'Lunch', 'Dinner', 'Drinks']
    menu_data = {}
    image_dir = os.path.join(STATIC_DIR, 'images')
    for cat in categories:
        cur = conn.execute("SELECT * FROM recipes WHERE meal_type = ? ORDER BY created_at DESC LIMIT 3", (cat,))
        recipes = cur.fetchall()
        processed_recipes = []
        for r in recipes:
            r_dict = dict(r)
            if r_dict.get('image_url') and not r_dict['image_url'].startswith('http'):
                 r_dict['image_url'] = url_for('static', filename=f'images/{r_dict["image_url"]}')
            else:
                target_title = r_dict['title'].lower().strip()
                found_image = None
                if os.path.exists(image_dir):
                    for filename in os.listdir(image_dir):
                        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                            file_base = os.path.splitext(filename)[0].lower().strip()
                            if file_base == target_title:
                                found_image = filename
                                break
                if found_image:
                    r_dict['image_url'] = url_for('static', filename=f'images/{found_image}')
            processed_recipes.append(r_dict)
        menu_data[cat] = processed_recipes
    conn.close()
    return render_template('main.html', username=session['username'], menu=menu_data)

# MODIFIED: Veg/Non-Veg Logic updated to normalize category and exclude Drinks/Dessert
@app.route('/category/<category_name>')
def show_category(category_name):
    if 'user_id' not in session: return redirect(url_for('home'))
    conn = get_db()
    
    db_cat = category_name.lower()
    if db_cat in ['veg', 'nonveg']:
        # Ensure category matches DB exactly and filters out specific meal types
        recipes = conn.execute("""
            SELECT * FROM recipes 
            WHERE category = ? 
            AND meal_type NOT IN ('Drinks', 'Dessert') 
            COLLATE NOCASE""", (db_cat,)).fetchall()
        display_name = "Vegetarian" if db_cat == 'veg' else "Non-Vegetarian"
    else:
        recipes = conn.execute("SELECT * FROM recipes WHERE meal_type = ? COLLATE NOCASE", (category_name,)).fetchall()
        display_name = category_name.capitalize()
        
    image_dir = os.path.join(STATIC_DIR, 'images')
    processed_recipes = []
    for r in recipes:
        r_dict = dict(r)
        if r_dict.get('image_url') and not r_dict['image_url'].startswith('http'):
             r_dict['image_url'] = url_for('static', filename=f'images/{r_dict["image_url"]}')
        else:
            target_title = r_dict['title'].lower().strip()
            found_image = None
            if os.path.exists(image_dir):
                for filename in os.listdir(image_dir):
                    if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                        file_base = os.path.splitext(filename)[0].lower().strip()
                        if file_base == target_title:
                            found_image = filename
                            break
            if found_image:
                r_dict['image_url'] = url_for('static', filename=f'images/{found_image}')
        processed_recipes.append(r_dict)
    conn.close()
    return render_template('category_list.html', category_name=display_name, recipes=processed_recipes)

@app.route('/recipe/<slug>', methods=['GET', 'POST'])
def show_page(slug):
    if slug in ['ingredients', 'category', 'filtered_recipes', 'liked', 'admin', 'editor', 'about']:
        if slug == 'admin': return redirect(url_for('admin_dashboard'))
        if slug == 'editor': return redirect(url_for('editor_dashboard'))
        if slug == 'liked': return redirect(url_for('liked_recipes'))
        return render_template(f'{slug}.html')
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM recipes WHERE slug = ?", (slug,))
    recipe = cur.fetchone()
    if not recipe:
        conn.close()
        abort(404)
    if request.method == 'POST':
        if 'username' in session:
            cur.execute("INSERT INTO comments (recipe_id, comment, username) VALUES (?, ?, ?)",
                        (recipe['id'], request.form.get('comment'), session['username']))
            conn.commit()
            return redirect(url_for('show_page', slug=slug))
        else:
            return redirect(url_for('home'))
    details = get_recipe_full_data(recipe['id'])
    cur.execute("SELECT * FROM comments WHERE recipe_id = ? ORDER BY timestamp DESC", (recipe['id'],))
    comments = cur.fetchall()
    conn.close()
    recipe_data = dict(recipe)
    original_image = recipe['image_url']
    target_title = recipe['title'].lower().strip()
    image_dir = os.path.join(STATIC_DIR, 'images')
    found_image = None
    if os.path.exists(image_dir):
        for filename in os.listdir(image_dir):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                file_base = os.path.splitext(filename)[0].lower().strip()
                if file_base == target_title:
                    found_image = filename
                    break
    if found_image:
        recipe_data['image_url'] = url_for('static', filename=f'images/{found_image}')
    else:
        recipe_data['image_url'] = original_image
    return render_template('recipe_detail.html', recipe=recipe_data, original_image=original_image, ingredients=details['ingredients'], instructions=details['instructions'], nutrition=details['nutrition'], fun_facts=details['fun_facts'], tips=details['tips'], comments=comments, user=session.get('username'), is_admin=session.get('is_admin'))

@app.route('/delete_comment/<int:comment_id>', methods=['POST'])
def delete_comment(comment_id):
    if 'username' not in session: return jsonify({'success': False}), 401
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT username FROM comments WHERE id = ?", (comment_id,))
    row = cur.fetchone()
    if row:
        is_owner = (row['username'] == session['username'])
        is_admin = session.get('is_admin') == True
        if is_owner or is_admin:
            cur.execute("DELETE FROM comments WHERE id = ?", (comment_id,))
            conn.commit()
            conn.close()
            return jsonify({'success': True})
    conn.close()
    return jsonify({'success': False}), 403

# --- PROTECTED ADMIN ROUTES ---
@app.route('/admin')
@admin_required
def admin_dashboard():
    return render_template('admin.html')

@app.route('/editor')
@admin_required
def editor_dashboard():
    conn = get_db()
    recipes = conn.execute("SELECT title FROM recipes ORDER BY title ASC").fetchall()
    conn.close()
    files = [r['title'] for r in recipes]
    return render_template('edit.html', files=files, data=None)

@app.route('/add_recipe', methods=['GET', 'POST'])
@admin_required
def add_recipe():
    if request.method == 'GET':
        return render_template('form.html')

    slug_base = request.form.get('recipe_name', 'Untitled')
    title = request.form.get('head', slug_base)
    slug = create_slug(slug_base)

    try:
        meal_idx = int(request.form.get('meal-type', 0))
        meal_type = MEAL_TYPES[meal_idx]
    except:
        meal_type = "Breakfast"
    category = request.form.get('category', 'veg')

    image_url_for_db = request.form.get('image', '')
    file = request.files.get('image_file')
    if file and allowed_file(file.filename):
        ext = file.filename.rsplit('.', 1)[1].lower()
        new_filename = f"{title}.{ext}"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))

    conn = get_db()
    cur = conn.cursor()
    try:
        if cur.execute("SELECT id FROM recipes WHERE slug = ?", (slug,)).fetchone():
            flash("Recipe ID already exists.", "warning")
            return redirect(url_for('add_recipe'))
        cur.execute('''INSERT INTO recipes (slug, title, description, image_url, video_url, prep_time, meal_type, category) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (slug, title, request.form.get('description'), image_url_for_db, request.form.get('video'), request.form.get('time'), meal_type, category))
        recipe_id = cur.lastrowid
        for line in request.form.get('ingredients', '').splitlines():
            if line.strip(): cur.execute("INSERT INTO ingredients (recipe_id, item_text) VALUES (?, ?)", (recipe_id, line.strip()))
        for idx, line in enumerate(request.form.get('instructions', '').splitlines()):
            if line.strip(): cur.execute("INSERT INTO instructions (recipe_id, step_text, step_order) VALUES (?, ?, ?)", (recipe_id, line.strip(), idx+1))
        for line in request.form.get('nutrition', '').splitlines():
            if ':' in line:
                name, val = line.split(':', 1)
                cur.execute("INSERT INTO nutrition (recipe_id, name, value_text, value_int) VALUES (?, ?, ?, ?)", (recipe_id, name.strip(), val.strip(), extract_int(val)))
            elif line.strip():
                 cur.execute("INSERT INTO nutrition (recipe_id, name, value_text, value_int) VALUES (?, ?, ?, ?)", (recipe_id, "Note", line.strip(), 0))
        for line in request.form.get('fun', '').splitlines():
            if line.strip(): cur.execute("INSERT INTO extra_info (recipe_id, info_type, content) VALUES (?, 'fun', ?)", (recipe_id, line.strip()))
        for line in request.form.get('tips', '').splitlines():
            if line.strip(): cur.execute("INSERT INTO extra_info (recipe_id, info_type, content) VALUES (?, 'tip', ?)", (recipe_id, line.strip()))
        conn.commit()
        flash("Recipe Added Successfully!", "success")
        return redirect(url_for('add_recipe'))
    except Exception as e:
        conn.rollback()
        flash(f"Error: {e}", "danger")
        return redirect(url_for('add_recipe'))
    finally:
        conn.close()

@app.route('/edit', methods=['POST'])
@admin_required
def edit_recipe_load():
    target_title = request.form.get('filename')
    conn = get_db()
    cur = conn.cursor()
    recipe = cur.execute("SELECT * FROM recipes WHERE title = ?", (target_title,)).fetchone()
    if not recipe:
        flash("Recipe not found", "danger")
        return redirect(url_for('editor_dashboard'))
    rid = recipe['id']
    ings = [r['item_text'] for r in cur.execute("SELECT item_text FROM ingredients WHERE recipe_id=?", (rid,)).fetchall()]
    insts = [r['step_text'] for r in cur.execute("SELECT step_text FROM instructions WHERE recipe_id=? ORDER BY step_order", (rid,)).fetchall()]
    nuts = []
    for r in cur.execute("SELECT name, value_text FROM nutrition WHERE recipe_id=?", (rid,)).fetchall():
        nuts.append(f"{r['name']}: {r['value_text']}")
    funs = [r['content'] for r in cur.execute("SELECT content FROM extra_info WHERE recipe_id=? AND info_type='fun'", (rid,)).fetchall()]
    tips = [r['content'] for r in cur.execute("SELECT content FROM extra_info WHERE recipe_id=? AND info_type='tip'", (rid,)).fetchall()]
    try:
        meal_idx = MEAL_TYPES.index(recipe['meal_type'])
    except:
        meal_idx = 0
    data = {'head': recipe['title'], 'image': recipe['image_url'], 'video': recipe['video_url'], 'time': recipe['prep_time'], 'description': recipe['description'], 'meal_type': recipe['meal_type'], 'meal_idx': meal_idx, 'ingredients': "\n".join(ings), 'instructions': "\n".join(insts), 'nutrition': "\n".join(nuts), 'fun': "\n".join(funs), 'tips': "\n".join(tips)}
    conn.close()
    return render_template('edit.html', data=data, filename=recipe['slug'])

@app.route('/save', methods=['POST'])
@admin_required
def save_recipe_changes():
    slug = request.form.get('filename')
    conn = get_db()
    cur = conn.cursor()
    try:
        row = cur.execute("SELECT id, image_url FROM recipes WHERE slug=?", (slug,)).fetchone()
        if not row: raise Exception("Recipe ID lost.")
        rid = row['id']
        current_db_image = row['image_url']
        try:
            meal_idx = int(request.form.get('meal-type', 0))
            meal_type = MEAL_TYPES[meal_idx]
        except: meal_type = "Breakfast"

        new_title = request.form.get('head')
        new_db_image = current_db_image
        if request.form.get('image'):
            new_db_image = request.form.get('image')

        file = request.files.get('image_file')
        if file and allowed_file(file.filename):
            ext = file.filename.rsplit('.', 1)[1].lower()
            new_filename = f"{new_title}.{ext}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))

        cur.execute("""UPDATE recipes SET title=?, description=?, image_url=?, video_url=?, prep_time=?, meal_type=? WHERE id=?""", (new_title, request.form.get('description'), new_db_image, request.form.get('video'), request.form.get('time'), meal_type, rid))
        cur.execute("DELETE FROM ingredients WHERE recipe_id=?", (rid,))
        for line in request.form.get('ingredients', '').splitlines():
            if line.strip(): cur.execute("INSERT INTO ingredients (recipe_id, item_text) VALUES (?, ?)", (rid, line.strip()))
        cur.execute("DELETE FROM instructions WHERE recipe_id=?", (rid,))
        for idx, line in enumerate(request.form.get('instructions', '').splitlines()):
            if line.strip(): cur.execute("INSERT INTO instructions (recipe_id, step_text, step_order) VALUES (?, ?, ?)", (rid, line.strip(), idx+1))
        cur.execute("DELETE FROM nutrition WHERE recipe_id=?", (rid,))
        for line in request.form.get('nutrition', '').splitlines():
            if ':' in line:
                name, val = line.split(':', 1)
                cur.execute("INSERT INTO nutrition (recipe_id, name, value_text, value_int) VALUES (?, ?, ?, ?)", (rid, name.strip(), val.strip(), extract_int(val)))
            elif line.strip():
                 cur.execute("INSERT INTO nutrition (recipe_id, name, value_text, value_int) VALUES (?, ?, ?, ?)", (rid, "Note", line.strip(), 0))
        cur.execute("DELETE FROM extra_info WHERE recipe_id=?", (rid,))
        for line in request.form.get('fun', '').splitlines():
            if line.strip(): cur.execute("INSERT INTO extra_info (recipe_id, info_type, content) VALUES (?, 'fun', ?)", (rid, line.strip()))
        for line in request.form.get('tips', '').splitlines():
            if line.strip(): cur.execute("INSERT INTO extra_info (recipe_id, info_type, content) VALUES (?, 'tip', ?)", (rid, line.strip()))
        conn.commit()
        flash("Changes Saved!", "success")
        return redirect(url_for('show_page', slug=slug))
    except Exception as e:
        conn.rollback()
        flash(f"Save failed: {e}", "danger")
        return redirect(url_for('editor_dashboard'))
    finally:
        conn.close()

@app.route('/delete_recipe', methods=['POST'])
@admin_required
def delete_recipe():
    recipe_name = request.form.get('recipe_name')
    conn = get_db()
    conn.execute("DELETE FROM recipes WHERE title=? OR slug=?", (recipe_name, create_slug(recipe_name)))
    conn.commit()
    conn.close()
    flash("Recipe Deleted.", "warning")
    return redirect(url_for('add_recipe'))

# --- PUBLIC INTERACTIVE ROUTES ---
@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    query = data.get("search", "").strip()
    conn = get_db()
    recipes = conn.execute("SELECT * FROM recipes WHERE title LIKE ?", (f"%{query}%",)).fetchall()
    conn.close()
    if not recipes: return jsonify({"message": "Sorry, Recipe Not Found!"}), 404
    if len(recipes) == 1: return jsonify({"redirect": url_for('show_page', slug=recipes[0]['slug'])})
    options = [r['slug'] for r in recipes]
    query_params = "&".join([f"options={opt}" for opt in options])
    return jsonify({"redirect": url_for('options_page') + "?" + query_params})

@app.route('/options')
def options_page():
    slugs = request.args.getlist('options')
    conn = get_db()
    placeholders = ','.join(['?'] * len(slugs))
    recipes = conn.execute(f"SELECT * FROM recipes WHERE slug IN ({placeholders})", slugs).fetchall()
    conn.close()
    formatted_recipes = [{"name": r['title'], "url": url_for('show_page', slug=r['slug']), "image": r['image_url']} for r in recipes]
    return render_template('options.html', recipes=formatted_recipes)

# --- MODIFIED: ADVANCED INGREDIENTS SEARCH (AND logic) ---
@app.route('/find_recipes', methods=['POST'])
def find_recipes():
    data = request.get_json()
    selected_ingredients = [ing.lower().strip() for ing in data.get('ingredients', []) if ing.strip()]
    if not selected_ingredients:
        return jsonify({'success': False, 'message': 'Select at least one ingredient.'}), 400
    
    conn = get_db()
    
    # Step 1: Find candidates containing ANY of the selected items to reduce the workload
    placeholders = ' OR '.join(['i.item_text LIKE ?'] * len(selected_ingredients))
    search_terms = [f"%{ing}%" for ing in selected_ingredients]
    
    query = f"""
        SELECT DISTINCT r.id, r.title, r.slug, r.image_url 
        FROM recipes r
        JOIN ingredients i ON r.id = i.recipe_id
        WHERE {placeholders}
    """
    
    cursor = conn.execute(query, search_terms)
    candidates = cursor.fetchall()
    
    if not candidates:
        conn.close()
        return jsonify({'success': False, 'message': 'No recipes found matching these ingredients.'})

    results = []
    image_dir = os.path.join(STATIC_DIR, 'images')
    
    for row in candidates:
        rid = row['id']
        title = row['title']
        
        # Get ALL ingredients for this candidate recipe
        cur_ing = conn.execute("SELECT item_text FROM ingredients WHERE recipe_id = ?", (rid,))
        db_ingredients = [r['item_text'].lower() for r in cur_ing.fetchall()]
        
        # MODIFIED: Check for AND logic (Recipe must contain ALL selected ingredients)
        all_selected_matched = True
        for user_ing in selected_ingredients:
            found_match = False
            for db_ing in db_ingredients:
                if user_ing in db_ing:
                    found_match = True
                    break
            if not found_match:
                all_selected_matched = False
                break
        
        # Only include recipes where ALL selected ingredients are found
        if all_selected_matched:
            # Calculate missing (items in the recipe that user didn't select)
            missing_ingredients = []
            for db_ing in db_ingredients:
                was_selected = False
                for user_ing in selected_ingredients:
                    if user_ing in db_ing:
                        was_selected = True
                        break
                if not was_selected:
                    missing_ingredients.append(db_ing)

            # Process Image
            img_url = row['image_url']
            if img_url and not img_url.startswith('http'):
                 img_url = url_for('static', filename=f'images/{img_url}')
            else:
                target_title = title.lower().strip()
                found_image = None
                if os.path.exists(image_dir):
                    for filename in os.listdir(image_dir):
                        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                            if os.path.splitext(filename)[0].lower().strip() == target_title:
                                found_image = filename
                                break
                if found_image: img_url = url_for('static', filename=f'images/{found_image}')

            results.append({
                'display_name': title,
                'html_page': row['slug'],
                'image': img_url,
                'missing_count': len(missing_ingredients),
                'missing_items': missing_ingredients
            })

    conn.close()

    # Sort results by the amount of additional ingredients required (least first)
    results.sort(key=lambda x: x['missing_count'])

    if not results:
        return jsonify({'success': False, 'message': 'No recipes found containing ALL selected ingredients.'})

    return jsonify({
        'success': True,
        'recipes': results
    })

@app.route("/filter_recipes", methods=["POST"])
def filter_recipes():
    if request.is_json: filters = request.get_json()
    else: filters = request.form.to_dict()
    NUTRITION_KEYS = ["calories", "protein", "carbs", "fats", "sugar", "fiber", "cholesterol"]
    user_filters = {k: int(v) for k, v in filters.items() if k in NUTRITION_KEYS and v and int(v) > 0}
    if not user_filters: return jsonify({'success': True, 'filtered_recipes': [], 'message': "No filters selected"})
    conn = get_db()
    cursor = conn.execute("SELECT r.title, r.slug, r.image_url, n.name, n.value_int FROM recipes r JOIN nutrition n ON r.id = n.recipe_id")
    rows = cursor.fetchall()
    conn.close()
    recipe_data = {}
    image_dir = os.path.join(STATIC_DIR, 'images')
    for row in rows:
        slug = row['slug']
        if slug not in recipe_data: 
            img_url = row['image_url']
            if img_url and not img_url.startswith('http'):
                 img_url = url_for('static', filename=f'images/{img_url}')
            else:
                target_title = row['title'].lower().strip()
                found_image = None
                if os.path.exists(image_dir):
                    for filename in os.listdir(image_dir):
                        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                            if os.path.splitext(filename)[0].lower().strip() == target_title:
                                found_image = filename
                                break
                if found_image: img_url = url_for('static', filename=f'images/{found_image}')
            recipe_data[slug] = {'name': row['title'], 'url': url_for('show_page', slug=slug), 'image': img_url, 'nutrition': {}}
        
        nut_name = row['name'].lower()
        for key in NUTRITION_KEYS:
            if key in nut_name: recipe_data[slug]['nutrition'][key] = row['value_int']
    matching_recipes = []
    for slug, data in recipe_data.items():
        match = True
        r_nuts = data['nutrition']
        for key, target_val in user_filters.items():
            current_val = r_nuts.get(key, 0)
            if not (target_val - 25 <= current_val <= target_val + 25):
                match = False;
                break
        if match: matching_recipes.append({'name': data['name'], 'url': data['url'], 'image': data['image']})
    return jsonify({'success': True, 'filtered_recipes': matching_recipes})

@app.route('/like_recipe', methods=['POST'])
def like_recipe():
    if 'username' not in session: return jsonify({'status': 'error', 'message': 'User not logged in'}), 401
    data = request.get_json()
    slug = data.get('recipe_name')
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id FROM recipes WHERE slug = ?", (slug,))
    recipe = cur.fetchone()
    if not recipe: conn.close(); return jsonify({'status': 'error', 'message': 'Recipe not found'}), 404
    recipe_id = recipe['id']
    username = session['username']
    try:
        cur.execute("INSERT INTO likes (recipe_id, username) VALUES (?, ?)", (recipe_id, username))
        liked = True
    except sqlite3.IntegrityError:
        cur.execute("DELETE FROM likes WHERE recipe_id = ? AND username = ?", (recipe_id, username))
        liked = False
    conn.commit()
    conn.close()
    return jsonify({'status': 'success', 'liked': liked})

@app.route('/liked')
def liked_recipes():
    if 'username' not in session: return redirect(url_for('home'))
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""SELECT r.title, r.slug, r.image_url FROM recipes r JOIN likes l ON r.id = l.recipe_id WHERE l.username = ?""", (session['username'],))
    rows = cur.fetchall()
    conn.close()
    liked = []
    image_dir = os.path.join(STATIC_DIR, 'images')
    for row in rows:
        img_url = row['image_url']
        if img_url and not img_url.startswith('http'):
             img_url = url_for('static', filename=f'images/{img_url}')
        else:
            target_title = row['title'].lower().strip()
            found_image = None
            if os.path.exists(image_dir):
                for filename in os.listdir(image_dir):
                    if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                        if os.path.splitext(filename)[0].lower().strip() == target_title:
                            found_image = filename
                            break
            if found_image: img_url = url_for('static', filename=f'images/{found_image}')
        liked.append({'name': row['title'], 'url': url_for('show_page', slug=row['slug']), 'image': img_url})
    return render_template('liked.html', liked_recipes=liked)

@app.route('/get_related_recipes/<slug>')
def fetch_related_recipes(slug):
    conn = get_db()
    current = conn.execute("SELECT meal_type FROM recipes WHERE slug=?", (slug,)).fetchone()
    if current: related = conn.execute("SELECT title, slug, image_url FROM recipes WHERE meal_type=? AND slug!=? LIMIT 4", (current['meal_type'], slug)).fetchall()
    else: related = conn.execute("SELECT title, slug, image_url FROM recipes WHERE slug!=? ORDER BY RANDOM() LIMIT 4", (slug,)).fetchall()
    conn.close()
    return jsonify([{"name": r['title'], "url": url_for('show_page', slug=r['slug']), "image_url": r['image_url']} for r in related])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)