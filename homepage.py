from nicegui import ui
from typing import Dict, List
from dictionary_frontend import DictionaryUI
from flashcard_frontend import FlashcardStudyPanel
from dictation import Dictation
from game_frontend import Gamefront, GameUI, ReviewUI, GameLogic, start_app
from read_frontend import ReadingUI
from login_frontend import NiceGUIPages 
from generate_db import db
import os

class DashboardApp:
    def __init__(self):
        # Configuration
        self.menu_items: List[Dict] = [
            {"name": "Dictionary", "icon": "school", "url": "/dictionary", "description": "Look up words and definitions"},
            {"name": "Flashcard", "icon": "style", "url": "/flashcard", "description": "Practice with flashcards"},
            {"name": "Reading", "icon": "menu_book", "url": "/reading", "description": "Read and comprehend texts"},
            {"name": "Dictation", "icon": "record_voice_over", "url": "/dictation", "description": "Practice listening and writing"},
            {"name": "Game", "icon": "insights", "url": "/game", "description": "Track your learning progress"}
        ]

        self.nav_items: List[Dict] = [
            {"name": "Home", "url": "/", "icon": "home"},
            {"name": "Explore", "url": "/explore", "icon": "explore"},
            {"name": "Help", "url": "/help", "icon": "help"}
        ]

        # State management
        self.notifications = []


    def sign_out(self):
        ui.run_javascript("window.location.href = 'http://127.0.0.1:8080/login';")
        db.set_user_status_off_by_username()


    def login(self):
        ui.run_javascript("window.location.href = 'http://127.0.0.1:8080/login';")

    def create_sidebar(self):
        sidebar_style =  '''
        background: linear-gradient(180deg, 
                rgba(255,255,255,0.8) 0%, 
                rgba(249,250,251,0.9) 100%);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-right: 1px solid rgba(0,0,0,0.1);
            height: 100vh
        '''

        with ui.column().classes('w-64 h-screen').style(sidebar_style):
            # Logo section
            with ui.row().classes('p-6 items-center justify-between w-full'):
                with ui.row().classes('items-center gap-2'):
                    ui.icon('auto_stories').classes('text-3xl text-pink-600')
                    ui.label('MYMY').classes('text-2xl font-bold text-pink-600')

            ui.separator().classes('mb-4')

            # Menu items
            for item in self.menu_items:
                with ui.row().classes(
                    'mx-4 p-3 rounded-xl transition-all duration-200 cursor-pointer ' +
                    ('hover:bg-pink-100')
                ):
                    ui.icon(item['icon']).classes('text-xl text-pink-600')
                    with ui.column().classes('ml-3 flex-1'):
                        ui.link(item['name'], item['url']).classes('font-semibold text-gray-700 no-underline')
                        #ui.label(item['name']).classes('font-semibold text-gray-700')
                        ui.label(item['description']).classes('text-xs text-gray-500')

            # Bottom section
            with ui.row().classes('mt-auto p-4 w-full items-center justify-between'):
                NiceGUIPages()
                ui.button('Log in', on_click=lambda: self.login(), color='pink').classes('btn btn-primary w-auto bg-pink-500 hover:bg-pink-700 text-white px-4 py-2 rounded-md') 
                ui.button('Sign out', on_click=lambda: self.sign_out(), color='pink').classes('btn btn-primary w-auto bg-pink-500 hover:bg-pink-700 text-white px-4 py-2 rounded-md') 
                #ui.link('Log Out',on_click=lambda: NiceGUIPages()).props('rounded').classes(
                #    'btn btn-primary w-auto bg-blue-500 hover:bg-blue-700 text-, white nouto-underline px-4 py-2 rounded-md'
                #        )
                #ui.link('Log Out', target=NiceGUIPages()).props('rounded').classes(
                #        'w-auto bg-pink-600 hover:bg-pink-800 text-white no-underline')
    def create_header(self):
        header_style = '''
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
        '''

        with ui.row().style('width: 144%; height: 80px; padding: 20px;').classes('items-center justify-between').style(header_style):
            # Navigation items
            with ui.row().classes('space-x-6'):
                for item in self.nav_items:
                    with ui.row().classes('items-center gap-2'):
                        ui.icon(item['icon']).classes('text-pink-600')
                        ui.link(item['name'], item['url']).classes(
                            'text-gray-700 hover:text-pink-600 transition-colors duration-200'
                        )

            # Right side elements
            with ui.row().classes('items-center gap-4'):
                with ui.row().classes('relative'):
                    ui.input(placeholder='Search...').props('rounded outlined dense').classes(
                    'w-64 bg-gray-100 border border-pink-500'
                    ).style('border-radius: 20px;')
                    ui.icon('search').classes('absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400')

                ui.button(icon='notifications', color='pink').props('flat round')
                ui.avatar('User').style('background: linear-gradient(135deg, #6366f1, #a855f7);')

    def create_main_content(self):
        with ui.column().style('width: 144%; height: 80px; padding: 20px;').classes('p-8 flex-1').style('background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(20px);'):
            # Welcome section
            with ui.row().classes('items-center justify-between mb-8'):
                with ui.column():
                    usname = db.active_user()
                    if usname != None:
                        ui.label(f'Welcome back, {usname} 🌷').classes('text-3xl font-bold text-gray-800')
                    else:
                        ui.label('Please log in 👽').classes('text-3xl font-bold text-gray-800')
                    ui.label('Here are some things you can do today').classes('text-gray-500 mt-1')                        
                    ui.label("Here's what's happening with your learning progress").classes('text-gray-500 mt-1')

            # Stats cards
            with ui.row().classes('gap-6 mb-8'):
                if db.count_all_reviews():
                    num = db.count_all_reviews()
                    stats = [
                        {'label': 'Review Words', 'value': num , 'icon': 'school'},
                    ]
                
                    for stat in stats:
                         with ui.card().classes('p-6 flex-1').style(
                            'background: rgba(255, 200, 210, 0.9); backdrop-filter: blur(20px);'
                        ):
                            with ui.row().classes('items-center justify-between mb-4'):
                                ui.label(stat['label']).classes('text-gray-500')
                                ui.icon(stat['icon']).classes('text-pink-600')
                            ui.label(stat['value']).classes('text-3xl font-bold mb-2 text-gray-800')
                            with ui.row().classes('items-center gap-1'):
                                ui.icon('arrow_upward').classes('text-green-500 text-sm')
                                
                else:
                    pass

           
        
     
     
    def create_page(self, url: str, title: str, content_callback=None):
        page_routes = {
            '/dictionary': self.create_dictionary_page,
            '/flashcard': self.create_flashcard_page,
            '/reading': self.create_reading_page,
            '/dictation': self.create_dictation_page,
            '/game': self.create_game_page,
        }

        @ui.page(url)
        def page():
            # Apply a style to the body
            bg_path = os.path.join(os.path.dirname(__file__), "background.jpg")
            with ui.image(bg_path).style(
            'position: fixed; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: -1;'
            ):
                pass

            with ui.row().classes('min-h-screen'):
                # Sidebar and header are only created once
                self.create_sidebar()
                with ui.column().classes('flex-1'):
                    self.create_header()

                # Check if content callback is provided
                    if content_callback:
                        content_callback()
                    elif url == '/':
                        self.create_main_content()
                    elif url in page_routes:
                        page_routes[url]()
                    else:
                        with ui.column().style('width: 144%; height: 80px; padding: 20px;').classes('p-8 flex-1').style('background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(20px);'):
                            ui.label(f'{title}').classes('text-3xl font-bold mb-4')
                            ui.label(f'Content for {title} will be displayed here.')

    
    def create_dictionary_page(self):
       # Placeholder function for the dictionary page
        DictionaryUI()
        return self.create_dictionary_page
    def create_flashcard_page(self):
        # Placeholder function for the dictionary page
        FlashcardStudyPanel()
        return self.create_flashcard_page
    def create_reading_page(self):
        ReadingUI()
        # Placeholder function for the dictionary page
        return self.create_reading_page
    def create_dictation_page(self):
        # Placeholder function for the dictionary page
        Dictation()
        return self.create_dictation_page
    def create_game_page(self):
        # Placeholder function for the dictionary page
        start_app()
        return self.create_game_page 

app = DashboardApp()

for item in app.menu_items + app.nav_items:
    app.create_page(item['url'], item['name'])

ui.run(port=808, title='MYMY Learning Platform', favicon='🎓')