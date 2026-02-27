def ensure_default_admin():
    """Ensure a default admin exists"""
    conn = get_database_connection()
    cursor = conn.cursor()

    default_email = "admin@example.com"
    default_password = "admin123"

    cursor.execute("SELECT * FROM admin WHERE email = ?", (default_email,))
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO admin (email, password) VALUES (?, ?)",
            (default_email, default_password)
        )
        conn.commit()

    conn.close()
from .dashboard import DashboardManager
