import mysql.connector
from app.config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

# Create table if it does not exist
def create_table_if_not_exists():
    connection = get_connection()
    cursor = connection.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS profile_details  (
      id INT NOT NULL AUTO_INCREMENT,
      client_id int not null,
      group_id INT ,
      name VARCHAR(255) NOT NULL,
      department VARCHAR(255) NOT NULL,
      face_encoding TEXT NOT NULL,
      PRIMARY KEY (id)
    );
    """)
    
    connection.commit()
    cursor.close()
    connection.close()

# Call the function to ensure table is created
create_table_if_not_exists()
