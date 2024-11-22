from generate_db import db
from nicegui import ui
from game_backend import GameLogic, ReviewLogic


class GameUI:
    def __init__(self,game_logic, game_front):
        self.game_logic = game_logic
        self.game_front = game_front  # Add reference to Gamefront
        self.container = None
        self.mode_container = None
        self.game_controls = None
        self.game_interface = None
        self.review_section = None
        self.score_label = None
        self.word_display = None
        self.input_box = None
        self.hint_label = None
        self.review_count_label = None
        self.card_content = None
        self.flashcard = None

    def setup_ui(self):
        with ui.column().classes('w-full'):
         with ui.row().classes('w-full justify-between mb-4'):
            ui.button('Back', on_click=self.game_front.setup_home_page, color = 'pink').classes('bg-pink-600').props('rounded')
        
         self._create_header()
         self._create_mode_selection()
         self._create_game_controls()
         self._create_game_interface()
        # Add review section initialization
         self.review_section = ui.column().classes('w-full mt-4')
         self.review_section.set_visibility(False)
    def add_to_review(self, word):
        if word not in self.review_album:
            self.review_album.append(word)
    def _create_header(self):
        ui.label("Word Scamble Game").classes('text-2xl text-pink-600 font-bold mb-4')
        with ui.row().classes('gap-4 mb-4'):
            ui.button("Self Album", on_click=lambda: self.show_mode_options('album'), color = 'pink').classes('bg-pink-600 hover:bg-pink-800').props('rounded').props('rounded')
            ui.button("Flashcard Topic", on_click=lambda: self.show_mode_options('topic'), color = 'pink').classes('bg-pink-600 hover:bg-pink-800 ').props('rounded').props('rounded')

    def _create_mode_selection(self):
        self.mode_container = ui.column().classes('w-full mb-4')

    def _create_game_controls(self):
        self.game_controls = ui.column().classes('w-full mb-4')
        with self.game_controls:
            ui.button("Start", on_click=self.start_new_game, color = 'pink').classes('bg-pink-500').props('rounded')
            ui.button("Replay", on_click=self.reset_game, color = 'pink').classes('bg-pink-500').props('rounded')
        self.game_controls.set_visibility(False)
    def finish (self):
        self.game_logic.save_review_album()
        ui.notify('Saved review album', color = 'success')
    def _create_game_interface(self):
        self.game_interface = ui.column().classes('w-full')
        with self.game_interface:
            self.score_label = ui.label(f"Score: 0").classes('text-lg mb-2')
            self.word_display = ui.label().classes('text-xl mb-2')
            self.hint_label = ui.label().classes('text-sm text-gray-500 mb-2')
            
            with ui.row().classes('gap-2'):
                self.input_box = ui.input(placeholder='Enter word...').classes('w-64')
                ui.button("Check", on_click=self.check_word, color = 'pink').classes('bg-pink-500').props('rounded')
                # ui.button("Skip", on_click=self.skip_word).classes('bg-pink-500')
                ui.button("Finish", on_click=self.finish, color = 'pink').classes('bg-pink-500').props('rounded')
        self.game_interface.set_visibility(False)


    def show_mode_options(self, mode):
        self.mode_container.clear()
        with self.mode_container:
            options = (list(self.game_logic.get_albums().keys()) if mode == 'album' 
                      else list(self.game_logic.get_topics()))
            
            if mode == 'album' and not options:
                ui.label("").classes('text-red-500')
                return

            ui.select(
                label="Choose " + ("album" if mode == 'album' else "topic"),
                options=options,
                on_change=lambda e: self.on_source_change(e.value, mode == 'album')
            ).classes('w-full max-w-xs mb-4 ')

    def on_source_change(self, source, is_album):
        if self.game_logic.set_word_source(source, is_album):
            self.game_controls.set_visibility(True)
            self.game_interface.set_visibility(False)
            self.review_section.set_visibility(True)
            self.update_review_section(True)

    def start_new_game(self):
        scrambled_word, word_length = self.game_logic.get_next_word()
        if not scrambled_word:
            ui.notify("Please choose a word source", color="warning")
            return
        
        self.game_interface.set_visibility(True)
        self.word_display.set_text(f"Rearrange: {scrambled_word}")
        self.hint_label.set_text(f"Length of word: {word_length} charaters")
        self.input_box.value = ""

    def check_word(self):
        is_correct, result = self.game_logic.check_answer(self.input_box.value.strip())
        if result == "empty":
            ui.notify("Please enter word", color="warning")
        elif is_correct:
            ui.notify("Correct! +1 point", color="success")
            self.score_label.set_text(f"Score: {self.game_logic.score}")
        else:
            ui.notify(f"Wrong! Correct answer: {result}", color="error")
            self.game_logic.add_to_review(result)
            # Update review logic immediately
            self.game_front.review_logic.set_review_words(self.game_logic.review_album)
            self.update_review_section()
    
        self.start_new_game()
    

    def reset_game(self):
        self.game_logic.reset_game()
        self.score_label.set_text("Score: 0")
        self.start_new_game()
    



class ReviewUI:
    def __init__(self, review_logic, game_front):
        self.review_logic = review_logic
        self.game_front = game_front
        self.review_section = None
        self.review_count_label = None
        self.card_content = None
        self.flashcard = None
    def setup_ui(self):
        with ui.column().classes('w-full'):
            # Add home button
            with ui.row().classes('w-full justify-between mb-4'):
                ui.button('Back', on_click=self.game_front.setup_home_page, color = 'pink').classes('bg-pink-600').props('rounded')
            
            self._create_review_section()
    def finish(self):
        self.review_logic.save_review_album
        ui.notify('Saved review words')
    def _create_review_section(self):
        self.review_section = ui.column().classes('w-full mt-4')
        with self.review_section:
            ui.label("Revision").classes('text-2xl text-pink-600 font-bold mb-2')
            self.review_count_label = ui.label().classes('text-sm text-gray-600 mb-2')
            
            self.flashcard = ui.card().classes('w-full h-48 cursor-pointer mb-4')
            with self.flashcard:
                self.card_content = ui.label().classes('text-xl text-center w-full h-full flex items-center justify-center')
            
            with ui.row().classes('w-full justify-center gap-4'):
                ui.button('←', on_click=self.prev_card, color = 'pink' ).classes('bg-pink-500').props('rounded')
                ui.button('Flip', on_click=self.flip_card, color = 'pink').classes('bg-pink-500').props('rounded')
                ui.button('→', on_click=self.next_card, color = 'pink').classes('bg-pink-500').props('rounded')
            
            with ui.row().classes('w-full justify-center gap-4 mt-4'):
                ui.button('Remembered', on_click=self.mark_as_remembered, color = 'pink').classes('bg-pink-500').props('rounded')
                ui.button('Not remember yet', on_click=self.next_card, color = 'pink').classes('bg-pink-500').props('rounded')
                ui.button('Finish Revision', on_click = self.finish , color = 'pink').classes('bg-pink-500').props('rounded')
        #self.review_section.set_visibility(False)
        self.update_review_section()
    
    def update_review_section(self):
        if self.review_count_label:
            count = self.review_logic.get_review_count()
            self.review_count_label.set_text(f'{count} revision word left')

        if self.card_content and self.flashcard:
            card_content = self.review_logic.get_current_card()
            if card_content:
                self.card_content.set_text(card_content)
                self.flashcard.style('background-color: white; color: gray')
            else:
                self.card_content.set_text("No revision word left")

    def flip_card(self):
        self.review_logic.flip_card()
        self.update_review_section()

    def next_card(self):
        self.review_logic.next_card()
        self.update_review_section()

    def prev_card(self):
        self.review_logic.prev_card()
        self.update_review_section()

    def mark_as_remembered(self):
        removed_word = self.review_logic.mark_as_remembered()
        if removed_word:
            ui.notify(f'Removed "{removed_word}" from revision word list', color="success")
            self.update_review_section()



class Gamefront:
    def __init__(self):
        self.game_logic = GameLogic()
        self.review_logic = ReviewLogic()
        self.page = ui.column().style('width: 144%; height: 80px; padding: 20px;').classes('p-8 flex-1 items-center').style('background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(20px);')
        self.setup_home_page()


    def setup_home_page(self):
        self.page.clear()
        with self.page:
            with ui.row().classes('w-full items-center gap-4 mb-6'):
                ui.icon('school', size='32px').classes('text-pink-600')
                ui.label('GAME').classes('text-2xl font-bold text-pink-600') 

            with ui.row().style('justify-content: center; margin: 10px 0;gap: 10px; flex-wrap: wrap;'):
                ui.button('Game', on_click=lambda: self.setup_game_page(), color = 'pink').classes('bg-pink-600').props('rounded')
                ui.button('Review', on_click=lambda: self.setup_review_page(), color = 'pink').classes('bg-pink-600').props('rounded')

    def setup_game_page(self):
        self.page.clear()
        with self.page:
            game_ui = GameUI(self.game_logic, self)  # Pass self reference
            game_ui.setup_ui()

    def setup_review_page(self):
        self.page.clear()
        with self.page:
            if self.game_logic.review_album:
                self.review_logic.set_review_words(self.game_logic.review_album)
            
            review_ui = ReviewUI(self.review_logic, self)  # Pass self reference
            review_ui.setup_ui()

    def register_routes(self):
        @ui.page('/game/home')
        def game():
            self.setup_game_page()

        @ui.page('/game/review')
        def review():
            self.setup_review_page()



# Khởi chạy ứng dụng
def start_app():
    app = Gamefront()
    #app = GameUI(GameLogic())
    app.register_routes()
    ui.run()

# Sử dụng
if __name__ in {"main", "mp_main"}:
    start_app()