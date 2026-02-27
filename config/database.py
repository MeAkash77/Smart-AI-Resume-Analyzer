import sqlite3
from datetime import datetime

DATABASE_NAME = "resume_data.db"


# =========================
# DATABASE CONNECTION
# =========================
def get_database_connection():
    conn = sqlite3.connect(DATABASE_NAME, check_same_thread=False)
    return conn


# =========================
# INITIALIZE DATABASE
# =========================
def init_database():
    conn = get_database_connection()
    cursor = conn.cursor()

    # Resume table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resume_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL,
        linkedin TEXT,
        github TEXT,
        portfolio TEXT,
        summary TEXT,
        target_role TEXT,
        target_category TEXT,
        education TEXT,
        experience TEXT,
        projects TEXT,
        skills TEXT,
        template TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Resume analysis
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resume_analysis (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        resume_id INTEGER,
        ats_score REAL,
        keyword_match_score REAL,
        format_score REAL,
        section_score REAL,
        missing_skills TEXT,
        recommendations TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (resume_id) REFERENCES resume_data (id)
    )
    """)

    # Admin table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Admin logs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        admin_email TEXT NOT NULL,
        action TEXT NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

    # 🔥 VERY IMPORTANT
    ensure_default_admin()


# =========================
# AUTO CREATE DEFAULT ADMIN
# =========================
def ensure_default_admin():
    conn = get_database_connection()
    cursor = conn.cursor()

    default_email = "admin@example.com"
    default_password = "admin123"

    cursor.execute("SELECT * FROM admin WHERE email = ?", (default_email,))
    admin_exists = cursor.fetchone()

    if not admin_exists:
        cursor.execute(
            "INSERT INTO admin (email, password) VALUES (?, ?)",
            (default_email, default_password)
        )
        conn.commit()

    conn.close()


# =========================
# VERIFY ADMIN LOGIN
# =========================
def verify_admin(email, password):
    conn = get_database_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM admin WHERE email = ? AND password = ?",
        (email, password)
    )

    result = cursor.fetchone()
    conn.close()

    return bool(result)


# =========================
# ADD ADMIN (Optional)
# =========================
def add_admin(email, password):
    conn = get_database_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO admin (email, password) VALUES (?, ?)",
            (email, password)
        )
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()


# =========================
# ADMIN LOGGING
# =========================
def log_admin_action(admin_email, action):
    conn = get_database_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO admin_logs (admin_email, action) VALUES (?, ?)",
        (admin_email, action)
    )

    conn.commit()
    conn.close()
