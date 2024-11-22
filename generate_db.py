import sqlite3
from datetime import datetime
import os

class LearningDatabase:
    def __init__(self):
        db_path = os.path.join(os.path.dirname(__file__), "learning.db")
        self.db_name = db_path
        self.conn = None
        self.cursor = None
        self.setup_database()

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def close(self):
        if self.conn:
            self.conn.close()

    def setup_database(self):
        """Create all necessary tables if they don't exist"""
        self.connect()
        
        self.cursor.executescript('''
            -- Core user table
            CREATE TABLE IF NOT EXISTS user (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                fullname TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                birthdate DATE NOT NULL,
                password_hash TEXT NOT NULL,
                status TEXT DEFAULT 'off' CHECK(status in ('on', 'off')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );


            -- Flashcard topics table
            CREATE TABLE IF NOT EXISTS personal_flashcard_topic (
                topic_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                topic_name TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES user(user_id)
            );

            -- Flashcards table
            CREATE TABLE IF NOT EXISTS flashcard (
                card_id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic_id INTEGER,
                front_content TEXT NOT NULL,
                back_content TEXT NOT NULL,
                FOREIGN KEY (topic_id) REFERENCES personal_flashcard_topic(topic_id)
            );
                                  
            -- User progress tracking for review words
            CREATE TABLE IF NOT EXISTS user_review (
                user_id INTEGER,
                review_id INTEGER PRIMARY KEY AUTOINCREMENT,
                front_content TEXT NOT NULL,
                back_content TEXT NOT NULL,
                last_review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user(user_id)
            );
                                  
            
            -- User study statistics
            CREATE TABLE IF NOT EXISTS user_study_stats (
                user_id INTEGER,
                study_date DATE,
                time_spent_minutes INTEGER DEFAULT 0,
                items_completed INTEGER DEFAULT 0,
                PRIMARY KEY (user_id, study_date),
                FOREIGN KEY (user_id) REFERENCES user(user_id)
            );
        ''')
        
        self.conn.commit()
    def set_user_status_off_by_username(self):
            self.cursor.execute("UPDATE user SET status = 'off'")
            self.conn.commit()
    def active_user(self):
        try:
            self.cursor.execute('''
                SELECT user_id, username
                FROM user
                WHERE status = 'on'
            ''')
            active_user = self.cursor.fetchone()
            print("Active Users:", active_user)
            if active_user:
                user_id, username = active_user
                return username
            else:
                print("No active users found.")
            return None  # If no active user, return None
        except sqlite3.Error as e:
            print(f"Error adding flashcard: {e}")
            return None  
    def add_flashcard(self, topic_name, front_content, back_content):
        try:
            self.cursor.execute('''
                SELECT user_id 
                FROM user
                WHERE status = 'on'
            ''')
            active_user = self.cursor.fetchone()
            print("Active Users:", active_user)
            user_id = active_user[0]
           # Find the topic_id based on the topic_name and user_id
            self.cursor.execute('''
                SELECT topic_id 
                FROM personal_flashcard_topic 
                WHERE user_id = ? AND topic_name = ?
            ''', (user_id, topic_name))
        
            result = self.cursor.fetchone()
            if result is None:
                print(f"No topic found for user_id: {user_id}, topic: {topic_name}")
                return False, 'No topic found'
        
            topic_id = result[0]

            # Check if card already exists
            self.cursor.execute('''
                SELECT 1 FROM flashcard f
                JOIN personal_flashcard_topic pt ON f.topic_id = pt.topic_id
                WHERE pt.user_id = ? 
                AND pt.topic_name = ? 
                AND f.front_content = ?
            ''', (user_id, topic_name, front_content))
        
            if self.cursor.fetchone():
                print("Card already exists")
                return False, 'Card already exists'
            # Insert the flashcard using the found topic_id
            self.cursor.execute('''
                INSERT INTO flashcard (topic_id, front_content, back_content)
                VALUES (?, ?, ?)
            ''', (topic_id, front_content, back_content))
            self.conn.commit()
            album_id = self.cursor.lastrowid
        
            # Nếu chèn thành công, trả về một tuple gồm success và thông báo
            if album_id:
                return True, f"Album created successfully with ID {album_id}"
            else:
                return False, "Failed to create album"
        except sqlite3.Error as e:
            print(f"Error adding flashcard: {e}")
            return False,   'Không tìm thấy album'
        
    def add_flashcard_topic(self, topic_name):
        """Add a new flashcard topic"""
        try:
            self.cursor.execute('''
                SELECT user_id 
                FROM user
                WHERE status = 'on'
            ''')
            active_user = self.cursor.fetchone()
            if not active_user:
                return False, "No active user found"
            print("Active Users:", active_user)
            user_id = active_user[0]
            self.cursor.execute('''
                INSERT INTO personal_flashcard_topic (user_id, topic_name)
                VALUES (?, ?)
            ''', (user_id, topic_name))
            self.conn.commit()
            album_id = self.cursor.lastrowid
        
            # Nếu chèn thành công, trả về một tuple gồm success và thông báo
            if album_id:
                return True, f"Album created successfully with ID {album_id}"
            else:
                return False, "Failed to create album"
        except sqlite3.Error as e:
            print(f"Error adding flashcard topic: {e}")
            return False, f"Error adding flashcard topic: {e}"
    def get_albums(self):
        try:
            albums = {}
            self.cursor.execute('''
                SELECT user_id 
                FROM user
                WHERE status = 'on'
            ''')
            active_user = self.cursor.fetchone()
            if not active_user:
                return False
            print("Active Users:", active_user)
            user_id = active_user[0]
            # SQL query to fetch the data
            query = '''
                SELECT 
                    pft.topic_name, 
                    f.front_content AS word, 
                    f.back_content AS info
                FROM 
                    personal_flashcard_topic pft
                JOIN 
                    flashcard f ON pft.topic_id = f.topic_id
                WHERE 
                    pft.user_id = ?
            '''
    
            # Execute the query
            self.cursor.execute(query, (user_id,))
    
            # Process the results
            rows = self.cursor.fetchall()
            for row in rows:
                topic_name, word, info = row
                if topic_name not in albums:
                   albums[topic_name] = []
                albums[topic_name].append({"word": word, "info": info})
            print("Final albums dictionary:")
            print(albums)
            return albums
        except sqlite3.Error as e:
            print(f"Error loading albums: {e}")
            return []

    def load_user_personal_flashcard_topic(self):
        """Load cards for active users from personal_flashcard_topic"""
        try:
        # Find users with 'on' status from user_information table
            self.cursor.execute('''
                SELECT user_id 
                FROM user
                WHERE status = 'on'
            ''')
            active_user = self.cursor.fetchone()
            if active_user:
                pass
            else:
                return []
            print("Active Users:", active_user)
            user_id = active_user[0]
            self.cursor.execute('''
                SELECT topic_name
                FROM personal_flashcard_topic
                WHERE user_id = ?
            ''', (user_id,))
            # Lấy tất cả kết quả từ truy vấn
            rows = self.cursor.fetchall()
        
            # Lưu vào album review_album
            topics = [row[0] for row in rows]
            print(topics)
            return topics

        except sqlite3.Error as e:
            print(f"Error loading review album: {e}")
            return []
    def load_flashcards_for_topic(self, topic_name):
        try:
            # Find active user
            self.cursor.execute('''
                SELECT user_id 
                FROM user
                WHERE status = 'on'
            ''')
            active_user = self.cursor.fetchone()
            if not active_user:
                print("No active user found")
                return []
            user_id = active_user[0]

            # Find topic_id for the given topic_name and user_id in personal_flashcard_topic
            self.cursor.execute('''
                SELECT topic_id 
                FROM personal_flashcard_topic
                WHERE user_id = ? AND topic_name = ?
            ''', (user_id, topic_name))
            topic_result = self.cursor.fetchone()
            if not topic_result:
                print(f"No topic found for user {user_id} and topic {topic_name}")
                return []
            topic_id = topic_result[0]
  
            # Select flashcards for the found topic_id from flashcard table
            self.cursor.execute('''
                SELECT front_content, back_content
                FROM flashcard
                WHERE topic_id = ?
            ''', (topic_id,))
        
            # Format results
            flashcards = [
                {
                    "word": row[0],  # front_content
                    "info": row[1]   # back_content
                }
                for row in self.cursor.fetchall()
            ]
        
            print(f"Loaded {len(flashcards)} flashcards for topic {topic_name}")
            return flashcards

        except sqlite3.Error as e:
            print(f"Error loading flashcards: {e}")
            return []
    def add_user_review(self, front_content, back_content):
        """Add a new user review record"""
        try:
            # Find active user
            self.cursor.execute('''
                SELECT user_id 
                FROM user
                WHERE status = 'on'
            ''')
            active_user = self.cursor.fetchone()
            if not active_user:
                print("No active user found")
                return []
            user_id = active_user[0]
            # Thực hiện câu lệnh INSERT
            self.cursor.execute('''
                INSERT INTO user_review (user_id, front_content, back_content )
                VALUES (?, ?, ?)
            ''', (user_id, front_content, back_content))
        
        # Ghi thay đổi vào cơ sở dữ liệu
            self.conn.commit()
            review_id = self.cursor.lastrowid  # Get the auto-generated review_id
        # Xác nhận nếu thêm thành công
            print(f"User review added: user_id={user_id}")
            return True
        except sqlite3.Error as e:
        # Thông báo lỗi nếu xảy ra
            print(f"Error adding user review: {e}")
            return False
    def delete_review_card(self, user_id, review_id):
        """Delete a review card from the user_review table"""
        try:
            # Thực hiện câu lệnh DELETE với điều kiện user_id và review_id
            self.cursor.execute('''
                SELECT user_id 
                FROM user
                WHERE status = 'on'
            ''')
            active_user = self.cursor.fetchone()
            if not active_user:
                print("No active user found")
                return []
            user_id = active_user[0]
            self.cursor.execute('''
                DELETE FROM user_review
                WHERE user_id = ? AND review_id = ?
            ''', (user_id, review_id))
            self.conn.commit()
           
            print(f"Review card deleted: user_id={user_id}, review_id={review_id}")
            return True
        except sqlite3.Error as e:
            print(f"Error deleting review card: {e}")
            return False
    def count_all_reviews(self):
        """Count the total number of words (flashcards) in the user_review table"""
        try:
            # Truy vấn để lấy tất cả front_content và back_content của user_id
            self.cursor.execute('''
                SELECT user_id 
                FROM user
                WHERE status = 'on'
            ''')
            active_user = self.cursor.fetchone()
            if active_user:
                pass
            else:
                return None
            print("Active Users:", active_user)
            user_id = active_user[0]
            # Truy vấn đếm tổng số từ trong bảng user_review
            self.cursor.execute('''
                SELECT COUNT(*) 
                FROM user_review
                WHERE user_id = ?
            ''', (user_id,))
            count = self.cursor.fetchone()[0]  # Lấy kết quả đầu tiên từ truy vấn
            print(f"Total words in review: {count}")  # In ra tổng số từ
            return count
        except sqlite3.Error as e:
            print(f"Error counting all reviews: {e}")
            return None
        
    def load_user_review_album(self):
        """Load all front_content and back_content for a specific user into review_album"""
        try:
            # Truy vấn để lấy tất cả front_content và back_content của user_id
            self.cursor.execute('''
                SELECT user_id 
                FROM user
                WHERE status = 'on'
            ''')
            active_user = self.cursor.fetchone()
            if active_user:
                pass
            else:
                return []
            print("Active Users:", active_user)
            user_id = active_user[0]
            self.cursor.execute('''
                SELECT front_content, back_content
                FROM user_review
                WHERE user_id = ?
            ''', (user_id,))
            # Lấy tất cả kết quả từ truy vấn
            rows = self.cursor.fetchall()
        
            # Lưu vào album review_album
            review_album = [(row[0], row[1]) for row in rows]
            # Xóa toàn bộ các review card của user_id đó
            self.cursor.execute('''
                DELETE FROM user_review
                WHERE user_id = ?
             ''', (user_id,))
        
             # Ghi nhận thay đổi
            self.conn.commit()
            
            print(f"Loaded {len(review_album)} review cards for user_id={user_id}")
            return review_album
        except sqlite3.Error as e:
            print(f"Error loading review album: {e}")
            return []


db = LearningDatabase()