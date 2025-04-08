import unittest
from db import Database

class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = Database()

    @classmethod
    def tearDownClass(cls):
        cls.db.close()

    def test_insert_user(self):
        self.db.insert_user('John Doe', 'john@example.com')
        self.db.cursor.execute("SELECT * FROM users WHERE email = 'john@example.com';")
        user = self.db.cursor.fetchone()
        self.assertIsNotNone(user)
        self.assertEqual(user[1], 'John Doe')

    def test_insert_user_duplicate(self):
        self.db.insert_user('Jane Doe', 'john@example.com')  # Should not insert duplicate
        self.db.cursor.execute("SELECT COUNT(*) FROM users WHERE email = 'john@example.com';")
        count = self.db.cursor.fetchone()[0]
        self.assertEqual(count, 1)

    def test_get_topics(self):
        topics = self.db.get_topics()
        self.assertIsInstance(topics, list)

    def test_get_difficulties(self):
        difficulties = self.db.get_difficulties()
        self.assertIsInstance(difficulties, list)

    def test_get_topic_id(self):
        self.db.cursor.execute("INSERT INTO quiz_topic (topic_name) VALUES ('Math') RETURNING id;")
        topic_id = self.db.cursor.fetchone()[0]
        self.db.conn.commit()
        self.assertEqual(self.db.get_topic_id('Math'), topic_id)

    def test_get_difficulty_id(self):
        self.db.cursor.execute("INSERT INTO difficulty (level) VALUES ('Easy') RETURNING id;")
        difficulty_id = self.db.cursor.fetchone()[0]
        self.db.conn.commit()
        self.assertEqual(self.db.get_difficulty_id('Easy'), difficulty_id)
