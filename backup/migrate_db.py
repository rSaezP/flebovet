import sqlite3
import mysql.connector
import os

# Conexiones
sqlite_conn = sqlite3.connect('db.sqlite3')
sqlite_cursor = sqlite_conn.cursor()

mysql_conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="flebovet_db"
)
mysql_cursor = mysql_conn.cursor()

try:
    # Desactivar foreign key checks
    mysql_cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    
    # Limpiar tablas
    mysql_cursor.execute("TRUNCATE TABLE auth_user")
    mysql_cursor.execute("TRUNCATE TABLE vetweb_producto")
    mysql_cursor.execute("TRUNCATE TABLE vetweb_userprofile")
    
    # Migrar usuarios
    print("Migrando usuarios...")
    sqlite_cursor.execute('''
        SELECT id, password, last_login, is_superuser, username, 
               first_name, last_name, email, is_staff, is_active, date_joined 
        FROM auth_user
    ''')
    for user in sqlite_cursor.fetchall():
        mysql_cursor.execute('''
            INSERT INTO auth_user 
            (id, password, last_login, is_superuser, username, 
             first_name, last_name, email, is_staff, is_active, date_joined)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', user)

    # Migrar productos
    print("Migrando productos...")
    sqlite_cursor.execute('''
        SELECT id, nombre, descripcion, imagen, stock, fecha_creacion, pdf, es_estatico 
        FROM vetweb_producto
    ''')
    for prod in sqlite_cursor.fetchall():
        mysql_cursor.execute('''
            INSERT INTO vetweb_producto 
            (id, nombre, descripcion, imagen, stock, fecha_creacion, pdf, es_estatico)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', prod)

    # Migrar perfiles
    print("Migrando perfiles...")
    sqlite_cursor.execute('SELECT id, role, user_id, created_at FROM vetweb_userprofile')
    for profile in sqlite_cursor.fetchall():
        mysql_cursor.execute('''
            INSERT INTO vetweb_userprofile 
            (id, role, user_id, created_at)
            VALUES (%s, %s, %s, %s)
        ''', profile)

    # Reactivar foreign key checks
    mysql_cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    
    mysql_conn.commit()
    print("¡Migración completada!")

except Exception as e:
    print(f"Error: {e}")
    mysql_conn.rollback()

finally:
    mysql_cursor.close()
    mysql_conn.close()
    sqlite_conn.close()