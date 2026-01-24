from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session, abort, g
import bcrypt
import os, difflib, sys, threading, time,re
from flask_mysqldb import MySQL
from mysql.connector import MySQLConnection
from jinja2 import ChoiceLoader, FileSystemLoader
from bs4 import BeautifulSoup
import traceback
from datetime import datetime

app = Flask(__name__, template_folder=os.path.abspath("templates"))
app.jinja_loader = ChoiceLoader([
    FileSystemLoader(os.path.abspath("templates")),
    FileSystemLoader(os.path.abspath("main_files"))
])

app.secret_key = "recipebook"
app.config['MYSQL_HOST'] = 'localhost'  
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'smith49'  
app.config['MYSQL_DB'] = 'userdb' 
mysql = MySQL(app)
 
config1 = {
    "host": "localhost",
    "user": "root",
    "password": "smith49",
    "database": "recipes"
}
db = MySQLConnection(**config1)
cursor = db.cursor()
db.commit()

TEMPLATE_DIR = "templates"
allowed_pages = {file[:-5] for file in os.listdir(TEMPLATE_DIR) if file.endswith('.html')}

# Helper functions
def get_recipe_image_url(recipe_name):
    """Find image URL for recipe with any supported extension"""
    static_images_dir = os.path.join(app.static_folder, 'images')
    base_name = recipe_name.lower()
    extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    
    for ext in extensions:
        image_path = os.path.join(static_images_dir, f"{base_name}{ext}")
        if os.path.exists(image_path):
            return f"/static/images/{base_name}{ext}"
    
    return "/static/images/default.jpg"

def format_recipe_data(tables):
    """Format recipe data while fixing case mismatch"""
    return [
        {
            "name": table.capitalize(),  # Capitalize for display
            "image_url": get_recipe_image_url(table),
            # Generate URL with capitalized version but keep table name original
            "url": url_for('show_page', page=table.capitalize())
        }
        for table in tables
    ]

#login
@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username == 'admin' and password == 't1':
        session['admin'] = True
        return redirect(url_for('admin_dashboard'))
    
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM users WHERE username = %s', (username,))
    user = cur.fetchone()
    cur.close()
    if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
        session['user_id'] = user[0]
        session['username'] = user[1]
        return redirect(url_for('main'))
    else:
        flash('Invalid credentials. Please try again.', 'danger')
        return redirect(url_for('home'))

#register
@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register_user():
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    
    # Enhanced Email validation
    if '@' not in email or ('.com' not in email and '.ac.in' not in email):
        flash('Please enter a valid email address (must contain @ and end with .com or .ac.in)', 'danger')
        return redirect(url_for('register'))
    
    # Password length validation
    if len(password) < 6:
        flash('Password must be at least 6 characters long', 'danger')
        return redirect(url_for('register'))
    
    # Password complexity validation
    has_number = any(char.isdigit() for char in password)
    has_upper = any(char.isupper() for char in password)
    if not has_number or not has_upper:
        flash('Password must contain at least 1 number and 1 capital letter', 'danger')
        return redirect(url_for('register'))

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    cur = mysql.connection.cursor()
    try:
        # Check for existing username
        cur.execute('SELECT * FROM users WHERE username = %s', (username,))
        existing_user = cur.fetchone()
        if existing_user:
            flash('Username already exists, try a different one.', 'danger')
            return redirect(url_for('register'))
        
        # Check for existing email
        cur.execute('SELECT * FROM users WHERE email = %s', (email,))
        existing_email = cur.fetchone()
        if existing_email:
            flash('Email already exists, try a different one.', 'danger')
            return redirect(url_for('register'))

        # Insert new user
        cur.execute('INSERT INTO users (username, password, email) VALUES (%s, %s, %s)', 
                   (username, hashed_password, email))
        mysql.connection.commit()
        
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('home'))
        
    except Exception as e:
        mysql.connection.rollback()
        flash('An error occurred during registration. Please try again.', 'danger')
        return redirect(url_for('register'))
        
    finally:
        cur.close()


#forgot pass
@app.route('/forgot', methods=['GET'])
def forgot_page():
    return render_template('forgot.html')

@app.route('/forgot', methods=['POST'])
def forgot():
    email = request.form['email']
    pass1 = request.form['username']
    pass2 = request.form['password'] 
    if pass1 != pass2:
        flash("Passwords do not match.", "error") 
        return redirect(url_for('forgot'))
    hashed_pass1 = bcrypt.hashpw(pass1.encode('utf-8'), bcrypt.gensalt()).decode('utf-8') 
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM users WHERE email= %s', (email,))
    user = cur.fetchone()
    if user:
        cur.execute('UPDATE users SET password = %s WHERE email = %s', (hashed_pass1, email))
        mysql.connection.commit()
        flash("Password updated successfully.", "success") 
        return redirect(url_for('login'))
    else:
        flash("Email Not found!.", "error") 
        return render_template('forgot.html')
        
@app.route('/main')
def main():
    if 'user_id' not in session:
        return redirect(url_for('home'))  
    
    username = session['username'] 
    return render_template('main.html', username=username)

#search section
@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    search_query = data.get("search")
    return search_recipe(search_query, cursor, allowed_pages)
@app.route('/<page>')
def show_page(page):
    if page in allowed_pages:
        return render_template(f'{page}.html')
    else:
        abort(404)
         
@app.route('/options')
def options_page():
    options = request.args.getlist('options')
    recipes = [
        {
            "name": option.replace('_', ' ').title(),  # Proper capitalization
            "url": url_for('show_page', page=option),
            "image": url_for('static', filename=f'images/{option.capitalize()}.png'),  # Image based on table name
            "default_image": url_for('static', filename='images/default.jpg')
        }
        for option in options
    ]
    return render_template('options.html', recipes=recipes)

def search_recipe(search_query, cursor, allowed_pages):
    if search_query:
        search_query = search_query.strip().lower().replace(" ", "")

        cursor.execute("SHOW TABLES FROM recipes")
        all_queries = [row[0] for row in cursor.fetchall()]
        
        # 🔹 Normalize table names
        normalized_tables = {
            table.lower().replace(" ", ""): table for table in all_queries
        }

        # 🔹 Check for exact match
        if search_query in normalized_tables:
            exact_match = [normalized_tables[search_query]]
        else:
            exact_match = []

        # 🔹 If no exact match, try partial match
        if not exact_match:
            similar_tables = difflib.get_close_matches(search_query, normalized_tables.keys(), n=5, cutoff=0.4)
            exact_match = [normalized_tables[match] for match in similar_tables]

        # 🔹 If still no match, return 404
        if not exact_match:
            return jsonify({"message": "Sorry, Recipe Not Found!"}), 404

        # 🔹 If exactly one matching recipe is found, redirect directly
        if len(exact_match) == 1:
            capitalized_recipe = exact_match[0].capitalize()  # Ensure first letter is capitalized
            return jsonify({"redirect": url_for('show_page', page=capitalized_recipe)})

        # 🔹 If multiple matches, properly format options
        formatted_options = [opt.capitalize() for opt in exact_match]  # Capitalizing first letter
        query_params = "&".join([f"options={opt}" for opt in formatted_options])
        
        return jsonify({"redirect": url_for('options_page') + "?" + query_params})

    return jsonify({"message": "Invalid input"}), 400

#ingredients based search
@app.route('/ingredients')
def select_ingredients():
    return render_template("ingredients.html")

@app.route('/find_recipes', methods=['POST'])
def find_recipes():
    try:
        data = request.get_json()
        selected_ingredients = [ing.lower().strip() for ing in data.get('ingredients', [])]
        
        if not selected_ingredients:
            return jsonify({'success': False, 'message': 'Please select at least one ingredient.'}), 400
        
        cursor.execute("SHOW TABLES")
        recipe_tables = [row[0] for row in cursor.fetchall()]
        
        matching_recipes = []
        
        for table in recipe_tables:
            try:
                cursor.execute(f"SHOW COLUMNS FROM `{table}` LIKE 'ingredient'")
                if not cursor.fetchone():
                    continue
                
                conditions = []
                params = []
                for ingredient in selected_ingredients:
                    conditions.append("LOWER(TRIM(ingredient)) LIKE %s")
                    params.append(f"%{ingredient}%")
                
                query = f"""
                    SELECT COUNT(DISTINCT ingredient) as matches
                    FROM `{table}`
                    WHERE {' OR '.join(conditions)}
                """
                
                cursor.execute(query, params)
                match_count = cursor.fetchone()[0]
                
                if match_count >= len(selected_ingredients):
                    # Format name for display and URL
                    display_name = ' '.join(word.capitalize() for word in table.split('_'))
                    html_page = f"{display_name}"
                    
                    matching_recipes.append({
                        'display_name': display_name,  
                        'html_page': html_page,      
                        'image': f"/static/images/{table}.png",
                        'default_image': "/static/images/default.png"
                    })
                        
            except Exception as e:
                print(f"Error processing table {table}: {str(e)}")
                continue
        
        if not matching_recipes:
            return jsonify({'success': False, 'message': 'No recipes found with all selected ingredients!'}), 404
        
        return jsonify({
            'success': True,
            'recipes': matching_recipes
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'An error occurred: {str(e)}'
        }), 500
#recommendation system
def get_db_cursor():
    return cursor

def get_all_recipes():
    cursor = get_db_cursor()
    cursor.execute("SHOW TABLES") 
    return [row[0] for row in cursor.fetchall()]

def get_related_recipes(page):
    all_recipes = get_all_recipes()
    similar_recipes = difflib.get_close_matches(page, all_recipes, n=5, cutoff=0.4)
    return [recipe for recipe in similar_recipes if recipe.lower() != page.lower()]

@app.route('/get_related_recipes/<page>')
def fetch_related_recipes(page):
    related = get_related_recipes(page)
    formatted_related = format_recipe_data(related)
    return jsonify(formatted_related)

#comment section
@app.route('/<recipe_name>', methods=['GET', 'POST'])
def recipe(recipe_name):
    if request.method == 'POST':
        comment = request.form['comment']
        username = session['username']
        with mysql.connection.cursor() as cur:
            cur.execute(
                "INSERT INTO comments (recipe_name, comment, username, timestamp) VALUES (%s, %s, %s, NOW())", 
                (recipe_name, comment, username)
            )
            mysql.connection.commit()
        return redirect(url_for('recipe', recipe_name=recipe_name))
    
    with mysql.connection.cursor() as cur:
        cur.execute("""
            SELECT username, comment, 
                   DATE_FORMAT(timestamp, '%M %d, %Y at %h:%i %p') as formatted_time
            FROM comments 
            WHERE recipe_name = %s 
            ORDER BY timestamp DESC
        """, (recipe_name,))
        comments = [{"user": row[0], "comment": row[1], "timestamp": row[2]} for row in cur.fetchall()]
    
    return render_template(f'{recipe_name}.html', recipe_name=recipe_name, comments=comments)

@app.route('/get_comments/<recipe_name>')
def get_comments(recipe_name):
    current_user = session.get('username', None)
    app.logger.info(f"Fetching comments for recipe: {recipe_name}")
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT id, username, comment, timestamp FROM comments WHERE recipe_name = %s ORDER BY timestamp DESC", (recipe_name,))
        comments = []
        for row in cur.fetchall():
            try:
                # If timestamp is a string, parse it first
                if isinstance(row[3], str):
                    timestamp = datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S')
                else:
                    timestamp = row[3]
                comments.append({
                    "id": row[0],
                    "user": row[1],
                    "comment": row[2],
                    "timestamp": timestamp.strftime('%B %d, %Y at %I:%M %p'),
                    "canDelete": current_user and (current_user == row[1])
                })
            except Exception as e:
                app.logger.error(f"Error formatting timestamp: {e}")
                comments.append({
                    "id": row[0],
                    "user": row[0],
                    "comment": row[1],
                    "timestamp": "Unknown time",
                    "canDelete": current_user and (current_user == row[1])
                })
    return jsonify(comments)
@app.route('/delete_comment/<int:comment_id>', methods=['POST'])
def delete_comment(comment_id):
    if 'username' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401
    
    with mysql.connection.cursor() as cur:
        # First check if the comment belongs to the current user
        cur.execute("SELECT username FROM comments WHERE id = %s", (comment_id,))
        result = cur.fetchone()
        
        if not result:
            return jsonify({'success': False, 'error': 'Comment not found'}), 404
        
        if result[0] != session['username']:
            return jsonify({'success': False, 'error': 'Unauthorized'}), 403
        
        # If it does belong to the user, delete it
        cur.execute("DELETE FROM comments WHERE id = %s", (comment_id,))
        mysql.connection.commit()
    
    return jsonify({'success': True})
#admin panel
@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/admin')
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('home'))
    return render_template('admin.html')

@app.route('/add_recipe', methods=['POST'])
def add_recipe():
    if not session.get('admin'):
        return redirect(url_for('home'))
    
    recipe_name = request.form.get("recipe_name").strip()
    if not recipe_name:
        flash("Recipe name cannot be empty!", "error")
        return redirect(url_for("admin_dashboard"))
    category = request.form.get("category")
    if not category:
        flash("Please select a category (Veg or NonVeg)!", "error")
        return redirect(url_for("admin_dashboard"))
    
    filename = recipe_name + ".html"
    template_file = os.path.join(TEMPLATE_DIR, "tes.html")
    
    if not os.path.exists(template_file):
        flash("Template file not found!", "error")
        return redirect(url_for("admin_dashboard"))
    
    with open(template_file, "r", encoding="utf-8") as f:
        new_content = f.read()
        
    def format_as_list(text):
        lines = text.strip().split("\n")
        formatted_lines = []
        for line in lines:
            if line.strip():
                cleaned_line = re.sub(r'^\s*\d+[.)]\s*', '', line.strip())
                formatted_lines.append(f"<li><i class='bi bi-check-circle-fill'></i> <span>{cleaned_line}</span></li>")
        return "<ul>" + "".join(formatted_lines) + "</ul>"
    
    replacements = {
        "{{recipe_name}}": recipe_name,
        "{{head}}": request.form.get("head"),
        "{{image}}": request.form.get("image"),
        "{{description}}": request.form.get("description"),
        "{{time}}": request.form.get("time"),
        "{{ingredients}}": format_as_list(request.form.get("ingredients", "")),
        "{{nutrition}}": format_as_list(request.form.get("nutrition", "")),
        "{{instructions}}": format_as_list(request.form.get("instructions", "")),
        "{{tips}}": format_as_list(request.form.get("tips")),
        "{{fun}}": format_as_list(request.form.get("fun")),
        "{{video}}": request.form.get("video"),
        "{{meal_type}}": get_meal_type(request.form.get("meal-type"))
    }
    for key, value in replacements.items():
        new_content = new_content.replace(key, value)
    
    with open(os.path.join(TEMPLATE_DIR, filename), "w", encoding="utf-8") as f:
        f.write(new_content)
    
    # Create the table with an additional flag column for metadata
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS `{recipe_name}` (
            id INT AUTO_INCREMENT PRIMARY KEY,
            ingredient VARCHAR(255),
            time VARCHAR(50),
            nutrition VARCHAR(50),
            value VARCHAR(50),
            category VARCHAR(50),
            meal_type VARCHAR(50),
            is_metadata BOOLEAN DEFAULT FALSE
        )
    """)
    
    # Get form data
    ingredients = request.form.get("ingredients").strip().split("\n")
    time_value = request.form.get("time").strip()
    nutrition_data = request.form.get("nutrition").strip().split("\n")
    category = request.form.get("category")
    meal_type = get_meal_type(request.form.get("meal-type"))
    
    # First insert metadata (time, category, meal_type) as a single record
    cursor.execute(f"""
        INSERT INTO `{recipe_name}` 
        (time, category, meal_type, is_metadata)
        VALUES (%s, %s, %s, TRUE)
    """, (time_value, category, meal_type))
    
    # Then insert all ingredients with their nutrition data
    for i, ingredient in enumerate(ingredients):
        if ingredient.strip():
            nutrition_name, nutrition_value = "", ""
            if i < len(nutrition_data):
                parts = nutrition_data[i].strip().split(":")
                if len(parts) == 2:
                    nutrition_name = parts[0].strip()
                    nutrition_value = parts[1].strip()
            
            cursor.execute(f"""
                INSERT INTO `{recipe_name}` 
                (ingredient, nutrition, value, is_metadata)
                VALUES (%s, %s, %s, FALSE)
            """, (ingredient.strip(), nutrition_name, nutrition_value))
    
    db.commit()
    flash("Recipe added successfully!", "success")
    threading.Thread(target=restart_server, daemon=True).start()
    return redirect(url_for('form'))

def get_meal_type(value):
    meal_types = ["Breakfast", "Brunch", "Lunch","Dessert","Dinner","Drinks"]
    try:
        return meal_types[int(value)]
    except (ValueError, TypeError):
        return "Unknown"

@app.route('/delete_recipe', methods=['POST'])
def delete_recipe():
    if not session.get('admin'):
        return redirect(url_for('home'))
    
    recipe_name = request.form.get("recipe_name").strip()
    filename = recipe_name + ".html"
    file_path = os.path.join(TEMPLATE_DIR, filename)
    
    if os.path.exists(file_path):
        os.remove(file_path)
        cursor.execute(f"DROP TABLE IF EXISTS `{recipe_name}`")
        db.commit()
        flash(" Recipe deleted successfully!", "success")
    else:
        flash("File does not exist!", "error")
    threading.Thread(target=restart_server, daemon=True).start()
    return redirect(url_for('form'))

#edit panel
@app.route('/editor/')
def editor_home():
    excluded_files = {"tes.html","login.html","category.html","filtered_recipes.html","liked.html",}
    files = [f[:-5] for f in os.listdir(TEMPLATE_DIR) if f.endswith(".html") and f not in excluded_files]
    return render_template('edit.html', files=files)

def load_recipe(filename):
    file_path = os.path.join(TEMPLATE_DIR, filename)
    if not os.path.exists(file_path):
        return None
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")
    return soup

@app.route('/edit', methods=['POST'])
def edit_recipe():
    filename = request.form.get("filename") + ".html"
    soup = load_recipe(filename)
    if not soup:
        flash("File not found!", "error")
        return redirect(url_for("editor_home"))

    # Helper function to extract list items as newline-separated string (removing the HTML tags)
    def extract_list_text(section_id):
        section = soup.find(id=section_id)
        if not section:
            return ""
        items = []
        for li in section.find_all('li'):
            # Extract just the text content, ignoring the icon and span tags
            span = li.find('span')
            if span:
                items.append(span.get_text(strip=True))
            else:
                items.append(li.get_text(strip=True))
        return "\n".join(items)

    data = {
        "recipe_name": soup.title.string if soup.title else "",
        "head": soup.find(id="head").get_text(strip=True) if soup.find(id="head") else "",
        "image": soup.find(id="image")["src"] if soup.find(id="image") else "",
        "description": soup.find(id="description").get_text(strip=True) if soup.find(id="description") else "",
        "ingredients": extract_list_text("ingredients"),
        "nutrition": extract_list_text("nutrition"),
        "fun": soup.find(id="fun").get_text(strip=True) if soup.find(id="fun") else "",
        "instructions": extract_list_text("instructions"),
        "tips": soup.find(id="tips").get_text(strip=True) if soup.find(id="tips") else "",
        "video": soup.find(id="video")["src"] if soup.find(id="video") else ""
    }
    return render_template('edit.html', files=[f[:-5] for f in os.listdir(TEMPLATE_DIR)], data=data, filename=filename[:-5])

@app.route('/save', methods=['POST'])
def save_recipe():
    filename = request.form.get("filename") + ".html"
    recipe_name = filename[:-5]  # Remove .html extension
    soup = load_recipe(filename)
    if not soup:
        flash("File not found!", "error")
        return redirect(url_for("editor_home"))

    # Update HTML content (your working version)
    updates = {
        "head": request.form.get("head"),
        "image": request.form.get("image"),
        "description": request.form.get("description"),
        "fun": request.form.get("fun"),
        "tips": request.form.get("tips"),
        "video": request.form.get("video")
    }
    
    # Update simple text fields
    for section, value in updates.items():
        tag = soup.find(id=section)
        if tag:
            if section in ["image", "video"]:
                tag["src"] = value
            else:
                tag.string = value
    
    # Update list sections with the new HTML structure
    list_sections = {
        "ingredients": request.form.get("ingredients", ""),
        "nutrition": request.form.get("nutrition", ""),
        "instructions": request.form.get("instructions", "")
    }
    
    for section_id, text in list_sections.items():
        tag = soup.find(id=section_id)
        if tag:
            tag.clear()
            ul = soup.new_tag("ul")
            for line in text.split('\n'):
                if line.strip():
                    li = soup.new_tag("li")
                    
                    # Add icon
                    icon = soup.new_tag("i", attrs={"class": "bi bi-check-circle-fill"})
                    li.append(icon)
                    
                    # Add space
                    li.append(" ")
                    
                    # Add span with the text
                    span = soup.new_tag("span")
                    span.string = line.strip()
                    li.append(span)
                    
                    ul.append(li)
            tag.append(ul)

    # Save the updated HTML file
    with open(os.path.join(TEMPLATE_DIR, filename), "w", encoding="utf-8") as file:
        file.write(str(soup))
    
    # Database update for only 3 columns (ingredient, nutrition, value)
    try:
        # Check if table exists
        cursor.execute(f"SHOW TABLES LIKE '{recipe_name}'")
        if not cursor.fetchone():
            flash("Database table not found for this recipe!", "warning")
        else:
            # Get form data for database update
            ingredients = request.form.get("ingredients", "").strip().split("\n")
            nutrition_data = request.form.get("nutrition", "").strip().split("\n")
            
            # Get all existing rows
            cursor.execute(f"SELECT * FROM `{recipe_name}`")
            existing_rows = cursor.fetchall()
            
            # Update existing rows
            for i, row in enumerate(existing_rows):
                if i < len(ingredients) and ingredients[i].strip():
                    # Get nutrition data if available
                    nutrition_name, nutrition_value = "", ""
                    if i < len(nutrition_data):
                        parts = nutrition_data[i].strip().split(":")
                        if len(parts) == 2:
                            nutrition_name = parts[0].strip()
                            nutrition_value = parts[1].strip()
                    
                    # Update only the three columns
                    cursor.execute(f"""
                        UPDATE `{recipe_name}` 
                        SET ingredient = %s, nutrition = %s, value = %s
                        WHERE ingredient = %s AND nutrition = %s AND value = %s
                    """, (
                        ingredients[i].strip(),
                        nutrition_name,
                        nutrition_value,
                        row[0],  # current ingredient
                        row[2],  # current nutrition
                        row[3]   # current value
                    ))
            
            # Add new rows if there are more ingredients than existing rows
            for i in range(len(existing_rows), len(ingredients)):
                if ingredients[i].strip():
                    nutrition_name, nutrition_value = "", ""
                    if i < len(nutrition_data):
                        parts = nutrition_data[i].strip().split(":")
                        if len(parts) == 2:
                            nutrition_name = parts[0].strip()
                            nutrition_value = parts[1].strip()
                    
                    # Insert new row with only the 3 columns (others will get default/null values)
                    cursor.execute(f"""
                        INSERT INTO `{recipe_name}` 
                        (ingredient, nutrition, value)
                        VALUES (%s, %s, %s)
                    """, (
                        ingredients[i].strip(),
                        nutrition_name,
                        nutrition_value
                    ))
            
            db.commit()
    except Exception as e:
        db.rollback()
        flash(f"Database update failed: {str(e)}", "error")
    
    flash("Recipe updated successfully!", "success")
    threading.Thread(target=restart_server, daemon=True).start()
    return redirect(url_for("editor_home"))

#recipe categories
def get_tables_by_category():
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    veg_tables = []
    non_veg_tables = []
    
    for (table_name,) in tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM `{table_name}` WHERE category = 'veg' AND meal_type NOT IN ('dessert', 'snacks')")
            veg_count = cursor.fetchone()[0]
            if veg_count > 0:
                veg_tables.append(table_name)
            
            cursor.execute(f"SELECT COUNT(*) FROM `{table_name}` WHERE category = 'nonveg' AND meal_type NOT IN ('dessert', 'snacks')")
            non_veg_count = cursor.fetchone()[0]
            if non_veg_count > 0:
                non_veg_tables.append(table_name)
        except Exception as e:
            print(f"Skipping table {table_name} due to error: {e}") 
    
    return veg_tables, non_veg_tables

def format_veg_data(table_names):
    recipes = []
    for table_name in table_names:
        url_name = table_name[0].upper() + table_name[1:] if table_name else table_name
        
        recipes.append({
            'name': table_name.replace('_', ' ').title(),
            'url': url_for('show_page', page=url_name),
            'image': get_recipe_image_url(table_name),
            'default_image': url_for('static', filename='images/default.jpg')
        })
    return recipes

def format_non_veg_data(table_names):
    recipes = []
    for table_name in table_names:
        url_name = table_name[0].upper() + table_name[1:] if table_name else table_name
        
        recipes.append({
            'name': table_name.replace('_', ' ').title(),
            'url': url_for('show_page', page=url_name),
            'image': get_recipe_image_url(table_name),
            'default_image': url_for('static', filename='images/default.jpg')
        })
    return recipes

@app.route("/category")
def category():
    return render_template("category.html")

@app.route("/veg")
def veg():
    veg_tables, _ = get_tables_by_category()
    recipes = format_veg_data(veg_tables)
    return render_template("veg.html", veg_recipes=recipes)

@app.route("/non_veg")
def non_veg():
    _, non_veg_tables = get_tables_by_category()
    recipes = format_non_veg_data(non_veg_tables)
    return render_template("non_veg.html", non_veg_recipes=recipes)

def get_dessert_tables():
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    dessert_tables = []
    
    for (table_name,) in tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM `{table_name}` WHERE meal_type IN ('dessert')")
            dessert_count = cursor.fetchone()[0]
            if dessert_count > 0:
                dessert_tables.append(table_name)
        except Exception as e:
            print(f"Skipping table {table_name} due to error: {e}")
    
    return dessert_tables

def format_dessert_data(table_names):
    recipes = []
    for table_name in table_names:
        # Ensure first letter is capitalized for URL
        url_name = table_name[0].upper() + table_name[1:] if table_name else table_name
        
        recipes.append({
            'name': table_name.replace('_', ' ').title(),  # Display name
            'url': url_for('show_page', page=url_name),    # URL with capitalized first letter
            'image': get_recipe_image_url(table_name),
            'default_image': url_for('static', filename='images/default.jpg')
        })
    return recipes

@app.route("/dessert")
def dessert():
    dessert_tables = get_dessert_tables()
    recipes = format_dessert_data(dessert_tables)
    return render_template("desserts.html", dessert_recipes=recipes)

def get_breakfast_tables():
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    breakfast_tables = []
    
    for (table_name,) in tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM `{table_name}` WHERE meal_type = 'breakfast'")
            breakfast_count = cursor.fetchone()[0]
            if breakfast_count > 0:
                breakfast_tables.append(table_name)
        except Exception as e:
            print(f"Skipping table {table_name} due to error: {e}")
    return breakfast_tables

def format_breakfast_data(table_names):
    recipes = []
    for table_name in table_names:
        url_name = table_name[0].upper() + table_name[1:] if table_name else table_name
        
        recipes.append({
            'name': table_name.replace('_', ' ').title(),
            'url': url_for('show_page', page=url_name),
            'image': get_recipe_image_url(table_name),
            'default_image': url_for('static', filename='images/default.jpg')
        })
    return recipes

@app.route("/breakfast")
def breakfast():
    breakfast_tables = get_breakfast_tables()
    recipes = format_breakfast_data(breakfast_tables)
    return render_template("breakfast.html", breakfast_recipes=recipes)

def get_lunch_tables():
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    lunch_tables = []
    
    for (table_name,) in tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM `{table_name}` WHERE meal_type = 'lunch'")
            lunch_count = cursor.fetchone()[0]
            if lunch_count > 0:
                lunch_tables.append(table_name)
        except Exception as e:
            print(f"Skipping table {table_name} due to error: {e}")
    
    return lunch_tables

def format_lunch_data(table_names):
    recipes = []
    for table_name in table_names:
        url_name = table_name[0].upper() + table_name[1:] if table_name else table_name
        
        recipes.append({
            'name': table_name.replace('_', ' ').title(),
            'url': url_for('show_page', page=url_name),
            'image': get_recipe_image_url(table_name),
            'default_image': url_for('static', filename='images/default.jpg')
        })
    return recipes
@app.route("/lunch")
def lunch():
    lunch_tables = get_lunch_tables()
    recipes = format_lunch_data(lunch_tables)
    return render_template("lunch.html", lunch_recipes=recipes)



def get_dinner_tables():
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    dinner_tables = []
    
    for (table_name,) in tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM `{table_name}` WHERE meal_type = 'dinner'")
            dinner_count = cursor.fetchone()[0]
            if dinner_count > 0:
                dinner_tables.append(table_name)
        except Exception as e:
            print(f"Skipping table {table_name} due to error: {e}")
    
    return dinner_tables

def format_dinner_data(table_names):
    recipes = []
    for table_name in table_names:
        url_name = table_name[0].upper() + table_name[1:] if table_name else table_name
        
        recipes.append({
            'name': table_name.replace('_', ' ').title(),
            'url': url_for('show_page', page=url_name),
            'image': get_recipe_image_url(table_name),
            'default_image': url_for('static', filename='images/default.jpg')
        })
    return recipes

@app.route("/dinner")
def dinner():
    dinner_tables = get_dinner_tables()
    recipes = format_dinner_data(dinner_tables)
    return render_template("dinner.html", dinner_recipes=recipes)

def get_drinks_tables():
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    drinks_tables = []
    
    for (table_name,) in tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM `{table_name}` WHERE meal_type = 'drinks'")
            drinks_count = cursor.fetchone()[0]
            if drinks_count > 0:
                drinks_tables.append(table_name)
        except Exception as e:
            print(f"Skipping table {table_name} due to error: {e}")
    
    return drinks_tables

def format_drinks_data(table_names):
    recipes = []
    for table_name in table_names:
        # Ensure first letter is capitalized for URL
        url_name = table_name[0].upper() + table_name[1:] if table_name else table_name
        
        recipes.append({
            'name': table_name.replace('_', ' ').title(),  # Display name
            'url': url_for('show_page', page=url_name),    # URL with capitalized first letter
            'image': get_recipe_image_url(table_name),
            'default_image': url_for('static', filename='images/default.jpg')
        })
    return recipes

@app.route("/drinks")
def drinks():
    drinks_tables = get_drinks_tables()
    recipes = format_drinks_data(drinks_tables)
    return render_template("drinks.html", drinks_recipes=recipes)
#nutrition filtering

NUTRITION_ALIASES = {
    "calories": ["calories", "kcal"],
    "protein": ["protein", "prot"],
    "carbs": ["carbs", "carbohydrates"],
    "fats": ["fats", "fat"],
    "sugar": ["sugar", "sugars"],
    "fiber": ["fiber", "fibr", "fibres"],
    "cholesterol": ["cholesterol", "cholestrol"]
}

UNIT_CONVERSIONS = {
    "carbs": "kcal",
    "cholesterol": "mg",
    "calories": "kcal",
    "protein": "g",
    "fats": "g",
    "sugar": "g",
    "fiber": "g"
}

def parse_nutrition_value(value):
    """Extract numeric value or range from nutrition string."""
    numbers = re.findall(r"\d+", value)
    return int(numbers[0]) if numbers else None

def format_filtered_data(table_names):
    """Format recipe data with consistent structure"""
    recipes = []
    for table_name in table_names:
        url_name = table_name[0].upper() + table_name[1:] if table_name else table_name
        
        recipes.append({
            'name': table_name.replace('_', ' ').title(),
            'url': url_for('show_page', page=url_name),
            'image': get_recipe_image_url(table_name),
            'default_image': url_for('static', filename='images/default.jpg')
        })
    return recipes

def get_filtered_recipes(filters):
    """Filter recipes based on user-selected filters with ±10 range tolerance."""
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    matching_recipes = []

    # Remove filters with value 0 (ignore them)
    active_filters = {k: v for k, v in filters.items() if v != 0}
    
    for (table_name,) in tables:
        try:
            cursor.execute(f"SELECT nutrition, value FROM `{table_name}`")
            nutrition_data = cursor.fetchall()
            
            recipe_values = {}

            # Map database nutrition names to standardized keys
            for nutrition, value in nutrition_data:
                for key, aliases in NUTRITION_ALIASES.items():
                    if nutrition.lower() in aliases:
                        recipe_values[key] = parse_nutrition_value(value)
                        break

            # Validate against active filters with ±10 range
            valid = True
            for key, user_value in active_filters.items():
                recipe_value = recipe_values.get(key)
                if recipe_value is None:
                    # Recipe doesn't have this nutrition info - exclude it
                    valid = False
                    break
                if not (user_value - 20 <= recipe_value <= user_value + 20):
                    valid = False
                    break

            # Only include if matches ALL active filters (or if no active filters)
            if valid:
                matching_recipes.append(table_name)

        except Exception as e:
            print(f"Skipping table {table_name} due to error: {e}")
            continue

    return matching_recipes

@app.route("/filter_recipes", methods=["POST"])
def filter_recipes():
    """Handle recipe filtering with range tolerance and zero-value ignoring."""
    try:
        # Get JSON data from the request
        if request.is_json:
            filters = request.get_json()
        else:
            filters = request.form.to_dict()
        
        print("Received filters:", filters)

        # Convert string values to integers and filter out None/0 values
        user_filters = {}
        for nutrient in ["calories", "protein", "carbs", "fats", "sugar", "fiber", "cholesterol"]:
            value = filters.get(nutrient)
            if value:
                try:
                    num_value = int(value)
                    # Include all values (including 0, which will be ignored later)
                    # Apply carbs multiplier if needed (remove if not necessary)
                    user_filters[nutrient] = num_value * 4 if nutrient == "carbs" else num_value
                except (ValueError, TypeError):
                    continue

        print("Processed filters:", user_filters)

        filtered_tables = get_filtered_recipes(user_filters) if user_filters else []
        filtered_recipes = format_filtered_data(filtered_tables)

        print(f"Found {len(filtered_recipes)} matching recipes")
        return jsonify({
            'success': True,
            'filtered_recipes': filtered_recipes,
            'filters': user_filters,
            'message': f"Found {len(filtered_recipes)} matching recipes"
        })

    except Exception as e:
        print(f"Error in filter_recipes: {str(e)}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e),
            'message': "Failed to apply filters"
        }), 500
    
#like system
@app.route('/like_recipe', methods=['POST'])
def like_recipe():
    if 'username' not in session:
        return jsonify({'status': 'error', 'message': 'User not logged in'}), 401

    data = request.get_json()
    recipe_name = data.get('recipe_name')
    username = session['username']

    try:
        with mysql.connection.cursor() as cur:
            cur.execute(
                "SELECT * FROM liked_recipes WHERE recipe = %s AND username = %s",
                (recipe_name, username)
            )
            liked = cur.fetchone()

            if liked:
                cur.execute(
                    "DELETE FROM liked_recipes WHERE recipe = %s AND username = %s",
                    (recipe_name, username)
                )
                mysql.connection.commit()
                return jsonify({'status': 'success', 'message': 'Recipe disliked', 'liked': False})
            else:
                cur.execute(
                    "INSERT INTO liked_recipes (recipe, username) VALUES (%s, %s)",
                    (recipe_name, username)
                )
                mysql.connection.commit()
                return jsonify({'status': 'success', 'message': 'Recipe liked', 'liked': True})
    except Exception as e:
        mysql.connection.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    
@app.route('/liked')
def liked_recipes():
    if 'username' not in session:
        flash('Please log in to view your liked recipes', 'error')
        return redirect(url_for('home'))

    username = session['username']

    try:
        with mysql.connection.cursor() as cur:
            cur.execute(
                "SELECT recipe FROM liked_recipes WHERE username = %s",
                (username,))
            liked_recipes = []
            for row in cur.fetchall():
                recipe_name = row[0]
                liked_recipes.append({
                    'name': recipe_name,
                    'url': url_for('show_page', page=recipe_name),
                    'image': get_recipe_image_url(recipe_name),
                    'default_image': url_for('static', filename='images/default.jpg')
                })

        return render_template('liked.html', liked_recipes=liked_recipes)
        
    except Exception as e:
        flash('An error occurred while loading your liked recipes', 'error')
        app.logger.error(f"Error in liked_recipes: {str(e)}")
        return redirect(url_for('main'))

def restart_server():
    """Restart the Flask application in a background thread"""
    time.sleep(2) 
    os.execv(sys.executable, ['python'] + sys.argv)

if __name__ == '__main__':
    # host='0.0.0.0' makes it accessible to other devices
    app.run(host='0.0.0.0', port=5000, debug=True)