from nicegui import ui
import pandas as pd
import string

class Dictation:
    def __init__(self):
        self.index = 0
        self.user_answer = ""
        self.audio_player = None
        self.data = pd.DataFrame()  # Khởi tạo DataFrame rỗng
        self.selected_difficulty = None
        self.selected_topic = None
        self.notification_label = ui.label('').style('margin-top: 20px; font-size: 18px; color: black;')  # Khởi tạo label thông báo
        # Tạo các column cho từng trang
        self.difficulty_column =  ui.column().style('width: 144%; height: 80px; padding: 20px;').classes('p-8 flex-1 items-center').style('background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(20px);')
        self.topic_column =  ui.column().style('width: 144%; height: 80px; padding: 20px;').classes('p-8 flex-1 items-center').style('background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(20px);')
        self.dictation_column =  ui.column().style('width: 144%; height: 80px; padding: 20px;').classes('p-8 flex-1 items-center').style('background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(20px);')
        self.render_difficulty_page()  # Khởi động ứng dụng tại trang chọn độ khó

    def update_audio_file(self):
        audio_file = self.data.iloc[self.index]['audio_file']
        
        if self.audio_player:
            self.audio_player.delete()
        self.audio_player = ui.audio(audio_file).props('controls').style('width: 300px;')  
        self.audio_player.play()

    def normalize(self, text):
        return str(text).lower().translate(str.maketrans('', '', string.punctuation.replace("'", "")))
    
    def check_answer(self):
        user_words = self.normalize(self.user_answer).strip().split()
        correct_answer = self.data.iloc[self.index]['sentence']
        correct_words = self.normalize(correct_answer).strip().split()
        return user_words == correct_words
    
    def play_sound(self, audio_file):
        self.play = ui.audio(audio_file).style('display: none;')  
        self.play.play()

    def check_answer_click(self):
        if self.user_answer:
            result = self.check_answer()
            if result:
                self.play_sound("https://raw.githubusercontent.com/Phamlong2675/Python-Project/refs/heads/main/Audio/effect%20sound/sound_correct.wav")
                self.notification_label.text = 'Correct answer!'
                self.notification_label.style('color: green;')
            else:
                self.play_sound("https://raw.githubusercontent.com/Phamlong2675/Python-Project/refs/heads/main/Audio/effect%20sound/sound_wrong.mp3")
                self.notification_label.text = 'Wrong answer!'
                self.notification_label.style('color: red;')
        else:
            self.notification_label.text = 'Please enter your answer before checking.'
            self.notification_label.style('color: orange;')

    def show_answer(self):
        correct_answer = self.data.iloc[self.index]['sentence']
        self.notification_label.text = f"Answer: '{correct_answer}'"
        self.notification_label.style('color: green;')

    def skip(self):
        if len(self.data) > 0:
            self.index = (self.index + 1) % len(self.data)
            self.user_answer = ""
            self.input.value = "" 
            self.notification_label.text = ""
            self.update_audio_file()
            self.no_sens.delete()
            self.no_sens = ui.label(f'({self.index+1}/10)').style('font-size: 18px;')

    def turnback(self):
        if len(self.data) > 0:
            if self.index > 0:
                self.index -= 1
            else:
                self.index = 9
            self.user_answer = ""
            self.input.value = "" 
            self.notification_label.text = "" 
            self.update_audio_file()
            self.no_sens.delete()
            self.no_sens = ui.label(f'({self.index+1}/10)').style('font-size: 18px;')

    def load_data(self, url):
        self.data = pd.read_csv(url)
        self.index = 0  # Đặt lại chỉ số khi tải dữ liệu mới
        self.update_audio_file()  # Cập nhật tệp âm thanh cho mục đầu tiên

    def go_to_topic_selection(self, difficulty):
        self.selected_difficulty = difficulty
        self.render_topic_page()  # Hiển thị trang chọn chủ đề

    def set_topic(self, topic):
        self.selected_topic = topic
        self.start_dictation()

    def start_dictation(self):
        topic_urls = {
            'Movies - Easy': 'https://raw.githubusercontent.com/Phamlong2675/Python-Project/main/Audio/topic1easy.csv',
            'Snowfall - Easy': 'https://raw.githubusercontent.com/Phamlong2675/Python-Project/main/Audio/topic2easy.csv',
            'Grant - Easy': 'https://raw.githubusercontent.com/Phamlong2675/Python-Project/main/Audio/topic3easy.csv',
            'Weather - Easy': 'https://raw.githubusercontent.com/Phamlong2675/Python-Project/main/Audio/topic4easy.csv',
            'Daily - Easy': 'https://raw.githubusercontent.com/Phamlong2675/Python-Project/main/Audio/topic5easy.csv',
            'Excursion - Hard': 'https://raw.githubusercontent.com/Phamlong2675/Python-Project/main/Audio/topic1hard.csv',
            'Healthy - Hard': 'https://raw.githubusercontent.com/Phamlong2675/Python-Project/main/Audio/topic2hard.csv',
            'Restaurant - Hard': 'https://raw.githubusercontent.com/Phamlong2675/Python-Project/main/Audio/topic3hard.csv',
            'Painting - Hard': 'https://raw.githubusercontent.com/Phamlong2675/Python-Project/main/Audio/topic4hard.csv',
            'Project - Hard': 'https://raw.githubusercontent.com/Phamlong2675/Python-Project/main/Audio/topic5hard.csv',
        }
        url = topic_urls.get(self.selected_topic)
        if url:
            self.load_data(url)
        self.render_dictation_page()

    def render_difficulty_page(self):
            self.difficulty_column.clear()  # Xóa nội dung cũ
            with self.difficulty_column:
                with ui.row().classes('w-full items-center gap-4 mb-6'):
                    ui.icon('school', size='32px').classes('text-pink-600')
                    ui.label('DICTATION').classes('text-2xl font-bold text-pink-600')
                ui.label('CHOOSE APPROPRIATE LEVEL').style('margin-bottom: 20px;').classes('text-2xl font-semibold text-gray-800')
                with ui.row().style('justify-content: center; margin: 10px 0;'):
                    ui.button('Easy', on_click=lambda: self.go_to_topic_selection('Easy')).props('rounded').style('margin: 10px; padding: 15px; font-size: 14px;').classes('bg-pink text-white')  # Căn giữa
                    ui.button('Hard', on_click=lambda: self.go_to_topic_selection('Hard')).props('rounded').style('margin: 10px; padding: 15px; font-size: 14px;').classes('bg-pink text-white')  # Căn giữa
            self.topic_column.clear()  # Xóa nội dung cũ
            self.dictation_column.clear()  # Xóa nội dung cũ
            self.difficulty_column.visible = True
            self.topic_column.visible = False
            self.dictation_column.visible = False

    def render_topic_page(self):
        self.topic_column.clear()  # Xóa nội dung cũ
        with self.topic_column:
            with ui.row().classes('w-full items-center gap-4 mb-6'):
                    ui.icon('school', size='32px').classes('text-pink-600')
                    ui.label('DICTATION').classes('text-2xl font-bold text-pink-600')
            ui.label(f'DICTATION TOPIC').style('margin-bottom: 10px;').classes('text-2xl font-semibold text-gray-800')
        
            # Tạo hàng cho các nút chủ đề
            with ui.row().style('justify-content: center; margin: 10px 0;gap: 10px; flex-wrap: wrap;'):
                    if self.selected_difficulty == 'Easy':
                        ui.button('Movies', on_click=lambda: self.set_topic('Movies - Easy')).props('rounded').classes('w-full bg-pink hover:bg-pink text-white font-semibold py-2 rounded-lg shadow-md') 
                        ui.button('Snowfall', on_click=lambda: self.set_topic('Snowfall - Easy')).props('rounded').classes('w-full bg-pink hover:bg-pink text-white font-semibold py-2 rounded-lg shadow-md')
                        ui.button('Grant', on_click=lambda: self.set_topic('Grant - Easy')).props('rounded').classes('w-full bg-pink hover:bg-pink text-white font-semibold py-2 rounded-lg shadow-md')
                        ui.button('Weather', on_click=lambda: self.set_topic('Weather - Easy')).props('rounded').classes('w-full bg-pink hover:bg-pink text-white font-semibold py-2 rounded-lg shadow-md')  
                        ui.button('Daily', on_click=lambda: self.set_topic('Daily - Easy')).props('rounded').classes('w-full bg-pink hover:bg-pink text-white font-semibold py-2 rounded-lg shadow-md')
                    elif self.selected_difficulty == 'Hard':
                        ui.button('Excursion', on_click=lambda: self.set_topic('Excursion - Hard')).props('rounded').classes('w-full bg-pink hover:bg-pink text-white font-semibold py-2 rounded-lg shadow-md')
                        ui.button('Healthy', on_click=lambda: self.set_topic('Healthy - Hard')).props('rounded').classes('w-full bg-pink hover:bg-pink text-white font-semibold py-2 rounded-lg shadow-md')
                        ui.button('Restaurant', on_click=lambda: self.set_topic('Restaurant - Hard')).props('rounded').classes('w-full bg-pink hover:bg-pink text-white font-semibold py-2 rounded-lg shadow-md')
                        ui.button('Painting', on_click=lambda: self.set_topic('Painting - Hard')).props('rounded').classes('w-full bg-pink hover:bg-pink text-white font-semibold py-2 rounded-lg shadow-md')
                        ui.button('Project', on_click=lambda: self.set_topic('Project - Hard')).props('rounded').classes('w-full bg-pink hover:bg-pink text-white font-semibold py-2 rounded-lg shadow-md')        
            
            # Nút Quay lại căn trái
            ui.button('Back', on_click=self.render_difficulty_page).props('rounded').style('margin: 10px 0; padding: 15px; font-size: 14px; align-self: flex-start;').classes('bg-pink text-white')
        self.difficulty_column.visible = False
        self.dictation_column.visible = False
        self.topic_column.visible = True

    def render_dictation_page(self):
        self.dictation_column.clear()  # Xóa nội dung cũ
        with self.dictation_column:
            with ui.row().classes('w-full items-center gap-4 mb-6'):
                    ui.icon('school', size='32px').classes('text-pink-600')
                    ui.label('DICTATION').classes('text-2xl font-bold text-pink-600')
            ui.label(f'Dictation: {self.selected_topic}').style('margin-bottom: 20px; font-size: 24px;').classes('font-semibold text-gray-800')
            with ui.row().style('justify-content: center; margin: 10px 0; align-items: center;'):
                ui.button(on_click=lambda: [self.turnback(), setattr(self.input, 'value', '')], icon='fast_rewind').props('rounded').style('width: 50px; height: 50px; padding: 0;').classes('bg-pink text-white')
                ui.button(on_click=lambda: [self.skip(), setattr(self.input, 'value', '')], icon='fast_forward').props('rounded').style('width: 50px; height: 50px; padding: 0;').classes('bg-pink text-white')
                self.update_audio_file()  # Cập nhật âm thanh
                self.no_sens = ui.label(f'({self.index+1}/10)').style('font-size: 18px;')
            self.input = ui.input('Enter your answer:', on_change=lambda: setattr(self, 'user_answer', self.input.value)).style('margin-bottom: 10px; font-size: 14px; width: 400px; padding: 10px;')
            # Hiển thị label thông báo ở đây
            self.notification_label = ui.label('').style('margin-top: 20px; font-size: 20px; color: black;')  # Khởi tạo label thông báo
            # Tạo hàng cho các nút
            with ui.row().style('justify-content: center; margin: 10px 0;'):
                ui.button('Check answer', on_click=self.check_answer_click).props('rounded').classes('bg-pink text-white')
                ui.button('Show answer', on_click=self.show_answer).props('rounded').classes('bg-pink text-white')
            with ui.row().style('justify-content: center; margin: 10px 0;'):
                ui.button('Choose dictation level', on_click=self.render_difficulty_page).props('rounded').classes('bg-pink text-white')
                ui.button('Choose dictation topic', on_click=self.render_topic_page).props('rounded').classes('bg-pink text-white')
        self.difficulty_column.visible = False
        self.topic_column.visible = False
        self.dictation_column.visible = True
        
Dictation()
ui.run()
