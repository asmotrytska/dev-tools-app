import sqlite3

DB_NAME = "devtools.db"

def init_db():
    """Створення таблиць та заповнення початковими демо-даними"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS libraries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            url TEXT NOT NULL,
            description TEXT NOT NULL,
            rating INTEGER CHECK(rating BETWEEN 1 AND 5),
            category_id INTEGER,
            FOREIGN KEY (category_id) REFERENCES categories (id)
        )
    """)
    
    conn.commit()
    
    cursor.execute("SELECT COUNT(*) FROM categories")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO categories (name) VALUES (?)", [
            ("Веброзробка",),
            ("Штучний інтелект",),
            ("Аналіз даних",),
            ("Бази даних",)
        ])
        
        cursor.executemany("""
            INSERT INTO libraries (name, url, description, rating, category_id) 
            VALUES (?, ?, ?, ?, ?)
        """, [
            ("Streamlit", "https://streamlit.io", "Фреймворк для швидкого створення вебінтерфейсів на Python", 5, 1),
            ("FastAPI", "https://fastapi.tiangolo.com", "Сучасний швидкий вебфреймворк для створення API", 5, 1),
            ("Pandas", "https://pandas.pydata.org", "Бібліотека для аналізу та маніпуляції даними", 5, 3),
            ("SQLAlchemy", "https://www.sqlalchemy.org", "SQL-тулкіт та ORM для роботи з БД", 4, 4),
            ("Scikit-learn", "https://scikit-learn.org", "Популярна бібліотека машинного навчання", 5, 2)
        ])
        conn.commit()
        
    conn.close()

def get_categories():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM categories")
    data = cursor.fetchall()
    conn.close()
    return data

def get_libraries(search_query="", category_filter="Усі"):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    query = """
        SELECT l.id, l.name, l.url, l.description, l.rating, c.name 
        FROM libraries l 
        JOIN categories c ON l.category_id = c.id
        WHERE 1=1
    """
    params = []
    
    if search_query:
        query += " AND (l.name LIKE ? OR l.description LIKE ?)"
        params.extend([f"%{search_query}%", f"%{search_query}%"])
        
    if category_filter != "Усі":
        query += " AND c.name = ?"
        params.append(category_filter)
        
    cursor.execute(query, params)
    data = cursor.fetchall()
    conn.close()
    return data

def add_library(name, url, description, rating, category_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO libraries (name, url, description, rating, category_id) 
        VALUES (?, ?, ?, ?, ?)
    """, (name, url, description, rating, category_id))
    conn.commit()
    conn.close()