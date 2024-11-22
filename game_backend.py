# backend/data.py
import random
from generate_db import db
topic_flashcards = {
"Nghề nghiệp": [
        {"word": "chef", "info": "đầu bếp"},
        {"word": "comedian", "info": "diễn viên hài"},
        {"word": "delivery man", "info": "nhân viên giao hàng"},
        {"word": "doctor", "info": "bác sĩ"},
        {"word": "entrepreneur", "info": "nhà kinh doanh"},
        {"word": "engineer", "info": "kỹ sư"},
        {"word": "factory worker", "info": "công nhân nhà máy"},
        {"word": "office worker", "info": "nhân viên văn phòng"},
        {"word": "florist", "info": "người bán hoa"},
        {"word": "hairdresser", "info": "thợ cắt tóc"},
    ],
    "Trái cây": [
        {"word": "pear", "info": "quả lê"},
        {"word": "grape", "info": "quả nho"},
        {"word": "peach", "info": "quả đào"},
        {"word": "orange", "info": "quả cam"},
        {"word": "mango", "info": "quả xoài"},
        {"word": "coconut", "info": "quả dừa"},
        {"word": "pineapple", "info": "quả dứa"},
        {"word": "watermelon", "info": "dưa hấu"},
        {"word": "durian", "info": "sầu riêng"},
        {"word": "lychee", "info": "quả vải"},
        {"word": "guava", "info": "quả ổi"},
        {"word": "starfruit", "info": "quả khế"},
    ],
    "Gia đình": [
        {"word": "parent", "info": "bố hoặc mẹ"},
        {"word": "daughter", "info": "con gái"},
        {"word": "son", "info": "con trai"},
        {"word": "sibling", "info": "anh chị em ruột"},
        {"word": "sister", "info": "chị, em gái"},
        {"word": "brother", "info": "anh, em trai"},
        {"word": "grandmother", "info": "bà nội (ngoại)"},
        {"word": "grandfather", "info": "ông nội (ngoại)"},
        {"word": "grandparent", "info": "ông hoặc bà"},
        {"word": "relative", "info": "họ hàng"},
        {"word": "aunt", "info": "cô, dì"},
        {"word": "uncle", "info": "chú, bác, cậu, dượng"},
    ],
    "Động Vật": [
        {"word": "mouse", "info": "con chuột"},
        {"word": "cat", "info": "con mèo"},
        {"word": "dog", "info": "con chó"},
        {"word": "kitten", "info": "mèo con"},
        {"word": "puppy", "info": "chó con"},
        {"word": "pig", "info": "con lợn, heo"},
        {"word": "chicken", "info": "con gà"},
        {"word": "duck", "info": "con vịt"},
        {"word": "goose", "info": "con ngỗng"},
        {"word": "turkey", "info": "con gà tây"},
        {"word": "stork", "info": "con cò"},
        {"word": "swan", "info": "thiên nga"},
    ],
    "Rau Quả": [
        {"word": "bean", "info": "hạt đậu"},
        {"word": "pea", "info": "đậu Hà Lan"},
        {"word": "cabbage", "info": "bắp cải"},
        {"word": "carrot", "info": "củ cà rốt"},
        {"word": "corn", "info": "ngô, bắp"},
        {"word": "cucumber", "info": "dưa chuột"},
        {"word": "tomato", "info": "quả cà chua"},
        {"word": "garlic", "info": "tỏi"},
        {"word": "onion", "info": "củ hành"},
        {"word": "spring onion", "info": "hành lá"},
        {"word": "ginger", "info": "củ gừng"},
        {"word": "turmeric", "info": "củ nghệ"},
        {"word": "potato", "info": "khoai tây"},
        {"word": "sweet potato", "info": "khoai lang"},
    ],
    "Đồ Ăn": [
        {"word": "soup", "info": "món súp, món canh"},
        {"word": "salad", "info": "rau trộn, nộm rau"},
        {"word": "bread", "info": "bánh mì"},
        {"word": "sausage", "info": "xúc xích"},
        {"word": "hot dog", "info": "bánh mỳ kẹp xúc xích"},
        {"word": "bacon", "info": "thịt xông khói"},
        {"word": "ham", "info": "thịt giăm bông"},
        {"word": "egg", "info": "trứng"},
        {"word": "pork", "info": "thịt lợn"},
        {"word": "beef", "info": "thịt bò"},
        {"word": "chicken", "info": "thịt gà"},
        {"word": "duck", "info": "thịt vịt"},
        {"word": "lamb", "info": "thịt cừu"},
        {"word": "ribs", "info": "sườn"},
    ],
    "Động tác cơ thể": [
        {"word": "tiptoe", "info": "đi nhón chân"},
        {"word": "jump", "info": "nhảy"},
        {"word": "leap", "info": "nhảy vọt, nhảy xa"},
        {"word": "stand", "info": "đứng"},
        {"word": "sit", "info": "ngồi"},
        {"word": "lean", "info": "dựa, tựa"},
        {"word": "wave", "info": "vẫy tay"},
        {"word": "clap", "info": "vỗ tay"},
        {"word": "point", "info": "chỉ, trỏ"},
        {"word": "catch", "info": "bắt, đỡ"},
        {"word": "stretch", "info": "vươn (vai..), ưỡn lưng"},
        {"word": "push", "info": "đẩy"},
        {"word": "pull", "info": "kéo"},
        {"word": "crawl", "info": "bò, trườn"},
    ],
    'Bộ phận cơ thế': [
    {"word": "head", "info": "đầu"},
    {"word": "hair", "info": "tóc"},
    {"word": "face", "info": "gương mặt"},
    {"word": "forehead", "info": "trán"},
    {"word": "eyebrow", "info": "lông mày"},
    {"word": "eye", "info": "mắt"},
    {"word": "eyelash", "info": "lông mi"},
    {"word": "nose", "info": "mũi"},
    {"word": "ear", "info": "tai"},
    {"word": "cheek", "info": "má"} 
    ],
    'Trường học': [
    {"word": "school", "info": "trường học"},
    {"word": "class", "info": "lớp học"},
    {"word": "student", "info": "học sinh, sinh viên"},
    {"word": "pupil", "info": "học sinh"},
    {"word": "teacher", "info": "giáo viên"},
    {"word": "principal", "info": "hiệu trưởng"},
    {"word": "course", "info": "khóa học"},
    {"word": "semester", "info": "học kì"},
    {"word": "exercise", "info": "bài tập"},
    {"word": "homework", "info": "bài tập về nhà"}
    ],
    'Tính cách': [
    {"word": "active", "info": "năng nổ, lanh lợi"},
    {"word": "alert", "info": "tỉnh táo, cảnh giác"},
    {"word": "ambitious", "info": "tham vọng"},
    {"word": "attentive", "info": "chăm chú, chú tâm"},
    {"word": "bold", "info": "táo bạo, mạo hiểm"},
    {"word": "brave", "info": "dũng cảm, gan dạ"},
    {"word": "careful", "info": "cẩn thận, thận trọng"},
    {"word": "careless", "info": "bất cẩn, cẩu thả"},
    {"word": "cautious", "info": "thận trọng, cẩn thận"},
    {"word": "conscientious", "info": "chu đáo, tỉ mỉ"},
    {"word": "courageous", "info": "can đảm"}
    ],
    'Đồ dùng học tập': 
    [
    {"word": "pen", "info": "bút mực"},
    {"word": "pencil", "info": "bút chì"},
    {"word": "highlighter", "info": "bút nhớ"},
    {"word": "ruler", "info": "thước kẻ"},
    {"word": "eraser", "info": "tẩy, gôm"},
    {"word": "pencil case", "info": "hộp bút"},
    {"word": "book", "info": "quyển sách"},
    {"word": "notebook", "info": "vở"},
    {"word": "paper", "info": "giấy"},
    {"word": "scissors", "info": "kéo"}
     ],
    'Thiên nhiên ': [
    {"word": "forest", "info": "rừng"},
    {"word": "rainforest", "info": "rừng mưa nhiệt đới"},
    {"word": "mountain", "info": "núi, dãy núi"},
    {"word": "highland", "info": "cao nguyên"},
    {"word": "hill", "info": "đồi"},
    {"word": "valley", "info": "thung lũng, châu thổ, lưu vực"},
    {"word": "cave", "info": "hang động"},
    {"word": "rock", "info": "đá"},
    {"word": "slope", "info": "dốc"},
    {"word": "volcano", "info": "núi lửa"}
    ],
    'Du lịch': [
    {"word": "travel", "info": "đi du lịch"},
    {"word": "depart", "info": "khởi hành"},
    {"word": "leave", "info": "rời đi"},
    {"word": "arrive", "info": "đến nơi"},
    {"word": "airport", "info": "sân bay"},
    {"word": "take off", "info": "cất cánh"},
    {"word": "land", "info": "hạ cánh"},
    {"word": "check in", "info": "đăng ký phòng ở khách sạn"},
    {"word": "check out", "info": "trả phòng khách sạn"},
    {"word": "visit", "info": "thăm viếng"}
]
}
# backend/game_logic.py

class GameLogic:
    def __init__(self):
        self.albums = db.get_albums()  # Dictionary lưu trữ album
        self.review_album = db.load_user_review_album()  # Album cho từ cần ôn tập
        self.current_word = ""
        self.current_info = ""
        self.filtered_words = []
        self.score = 0

    def get_albums(self):
        return self.albums
    
    def get_topics(self):
        return topic_flashcards.keys()
        
    def set_word_source(self, source, is_album = False):
        if is_album:
            self.filtered_words = [(entry["word"], entry["info"]) for entry in self.albums[source]]
        else:
            self.filtered_words = [(entry["word"], entry["info"]) for entry in topic_flashcards[source]]
        return len(self.filtered_words) > 0

    def get_next_word(self):
        if not self.filtered_words:
            return None, None
        
        self.current_word, self.current_info = random.choice(self.filtered_words)
        word_letters = list(self.current_word.lower())
        random.shuffle(word_letters)
        scrambled_word = ''.join(word_letters)
        return scrambled_word, len(self.current_word)

    def check_answer(self, user_input):
        if not user_input:
            return False, "empty"
        
        is_correct = user_input.lower() == self.current_word.lower()
        if is_correct:
            self.score += 1
            self.filtered_words.remove((self.current_word, self.current_info))
        else:
            if (self.current_word, self.current_info) not in self.review_album:
                self.review_album.append((self.current_word, self.current_info))
        
        return is_correct, self.current_word

    def skip_current_word(self):
        """
        Skip the current word and add it to review album
        """
        if self.current_word and self.current_info:
            # Add to review album
            if (self.current_word, self.current_info) not in self.review_album:
                self.review_album.append((self.current_word, self.current_info))
            
            # Remove from filtered words
            self.filtered_words = [pair for pair in self.filtered_words if pair[0] != self.current_word]
            
            # Store skipped word to return
            skipped_word = self.current_word
            
            return skipped_word
        return None


    def reset_game(self):
        self.score = 0
        return self.score
    def save_review_album(self):
        try:
            print(self.review_album)
            success_count = 0
            for index, (front_content, back_content) in enumerate(self.review_album, start=1):
                print(front_content, back_content)
                # Sử dụng index như review_id
                success = db.add_user_review(front_content = front_content, back_content = back_content)
                if success:
                    success_count += 1
            print(f"Saved {success_count} reviews back to user_review")
            return True
        except Exception as e:
            print(f"Error saving reviews with existing function: {e}")
            return False

# backend/review_logic.py
class ReviewLogic:
    def __init__(self):
        self.review_album = db.load_user_review_album()
        self.current_index = 0
        self.card_flipped = False

    def set_review_words(self, review_words):
        """
        Set the review album with new words from game logic
        
        Parameters:
        review_words (list): List of tuples containing (word, info) pairs to review
        """
        self.review_album = review_words
        self.current_index = 0
        self.card_flipped = False

    def get_current_card(self):
        if not self.review_album:
            return None, None
        word, info = self.review_album[self.current_index]
        return info if self.card_flipped else word

    def flip_card(self):
        self.card_flipped = not self.card_flipped
        return self.get_current_card()

    def next_card(self):
        if self.review_album:
            self.current_index = (self.current_index + 1) % len(self.review_album)
            self.card_flipped = False
        return self.get_current_card()

    def prev_card(self):
        if self.review_album:
            self.current_index = (self.current_index - 1) % len(self.review_album)
            self.card_flipped = False
        return self.get_current_card()

    def mark_as_remembered(self):
        if self.review_album:
            removed_word = self.review_album.pop(self.current_index)
            if self.current_index >= len(self.review_album):
                self.current_index = max(0, len(self.review_album) - 1)
            return removed_word[0]
        return None

    def get_review_count(self):
        return len(self.review_album)
    def save_review_album(self):
        try:
            print(self.review_album)
            success_count = 0
            for index, (front_content, back_content) in enumerate(self.review_album, start=1):
                print(front_content, back_content)
                # Sử dụng index như review_id
                # Có thể tuỳ chỉnh ngày review nếu cần
                success = db.add_user_review(front_content = front_content, back_content = back_content)
                if success:
                    success_count += 1
            print(f"Saved {success_count} reviews back to user_review. ")
            return True
        except Exception as e:
            print(f"Error saving reviews with existing function: {e}")
            return False
    def review_section(self, num_cards):
        """
        Lấy một số lượng từ vựng cần ôn tập.
        
        Parameters:
        num_cards (int): Số lượng từ cần lấy từ album ôn tập.
        
        Returns:
        list: Danh sách các từ cần ôn tập.
        """
        return self.review_album[:num_cards]