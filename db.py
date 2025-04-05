import psycopg2

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname="QuizBot",
            user="postgres",
            password="98422",
            host="localhost",
            port="5432"
        )
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """Creates users table if not exists."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100) UNIQUE,
                topic VARCHAR(50),
                difficulty VARCHAR(20),
                score INTEGER
            );
        """)
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS quiz_topic (
                id SERIAL PRIMARY KEY,
                topic_name VARCHAR(100) UNIQUE,
                uniqueId UUID DEFAULT gen_random_uuid()
            );
        """)
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS difficulty (
                id SERIAL PRIMARY KEY,
                level VARCHAR(50) UNIQUE,
                uniqueId UUID DEFAULT gen_random_uuid()
            );
        """)
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS score (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                score INTEGER,
                uniqueId UUID DEFAULT gen_random_uuid()
            );
        """)
        
        self.conn.commit()

    def insert_user(self, name, email):
        """Inserts user data if not already exists."""
        try:
            self.cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s) ON CONFLICT (email) DO NOTHING;", (name, email))
            self.conn.commit()
        except Exception as e:
            print("Error inserting user:", e)

    def insert_quiz_result(self, name, email, topic, difficulty, score):
        """Saves quiz results to database."""
        try:
            self.cursor.execute("UPDATE users SET topic=%s, difficulty=%s, score=%s WHERE email=%s;", (topic, difficulty, score, email))
            self.conn.commit()
        except Exception as e:
            print("Error saving quiz result:", e)


    def get_topics(self):
        """Fetch all quiz topics."""
        self.cursor.execute("SELECT topic_name FROM quiz_topic;")
        return [row[0] for row in self.cursor.fetchall()]
    
    def get_difficulties(self):
        """Fetch all difficulty levels."""
        self.cursor.execute("SELECT level FROM difficulty;")
        return [row[0] for row in self.cursor.fetchall()]
    
    def get_topic_id(self, topic_name):
        """Fetch topic ID based on topic name."""
        self.cursor.execute("SELECT id FROM quiz_topic WHERE topic_name = %s;", (topic_name,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def get_difficulty_id(self, level):
        """Fetch difficulty ID based on level name."""
        self.cursor.execute("SELECT id FROM difficulty WHERE level = %s;", (level,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def close(self):
        self.cursor.close()
        self.conn.close()

