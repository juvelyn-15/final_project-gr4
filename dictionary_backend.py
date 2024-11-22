import requests
from nicegui import ui
from generate_db import db
# Backend 
class DictionaryBackend:
    def __init__(self):
        self.api_url = "https://api.dictionaryapi.dev/api/v2/entries/en/{word}"

    # Lấy thông tin của từ từ API
    def get_word_info(self, word):
        """Fetch word information from the API"""
        result = requests.get(self.api_url.format(word=word))
        return result.json()

    # Tạo một album flashcard mới
    def create_album(self, name):
        """Create an album and return result tuple"""
        return db.add_flashcard_topic(name)
        

    # Thêm một từ vào album đã chỉ định với định nghĩa tùy chỉnh tùy chọn
    def add_to_album(self, album_name, word_data, custom_definition=None):
        word = word_data['word']
        return db.add_flashcard(album_name, word, custom_definition)

    # Lấy danh sách tất cả các tên album
    def get_albums_list(self):
        """Get list of all album names"""
        return db.load_user_personal_flashcard_topic()