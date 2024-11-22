import requests
from nicegui import ui
from dictionary_backend import DictionaryBackend
# Frontend 
class DictionaryUI:
    def __init__(self):
        self.backend = DictionaryBackend()
        self.setup_ui()

    def search_word(self):
        word = self.input_word.value.strip()
        
        # Clear previous results
        if hasattr(self, 'result_container'):
            self.result_container.clear()
        
        with self.result_container:
            if not word:
                ui.label('Please enter a word to search').classes('text-red-500')
                return

            try:
                with ui.spinner('circle').classes('text-pink-500'):
                    data = self.backend.get_word_info(word)
                
                if isinstance(data, list) and len(data) > 0:
                    word_data = data[0]
                    self.display_word_info(word_data)
                else:
                    ui.label(f"No information found for word: '{word}'").classes('text-red-500')

            except Exception as e:
                ui.label(f"Error: {str(e)}").classes('text-red-500')

    def display_word_info(self, word_data):
        word = word_data['word']
        phonetic = word_data.get('phonetic', 'No phonetic available')
        meanings = word_data.get('meanings', [])

        # Word and Phonetic
        with ui.card().classes('w-full'):
            with ui.row().classes('items-center gap-4'):
                ui.label(word).classes('text-2xl font-bold')
                ui.label(phonetic).classes('text-gray-500')

        # Meanings
        with ui.card().classes('w-full mt-4'):
            for i, meaning in enumerate(meanings):
                if i > 0:
                    ui.separator().classes('my-4')
                
                ui.label(meaning.get('partOfSpeech', '').capitalize()).classes('text-lg font-semibold mb-2')
                
                for j, definition in enumerate(meaning.get('definitions', []), 1):
                    with ui.row().classes('ml-4 mb-2'):
                        ui.label(f"{j}.").classes('mr-2')
                        with ui.column().classes('gap-1'):
                            ui.label(definition.get('definition', '')).classes('text-gray-700')
                            if example := definition.get('example'):
                                ui.label(f"Example: {example}").classes('text-gray-500 text-sm ml-4')

        # Flashcard Creation Section
        self.display_flashcard_section(word_data)

    def display_flashcard_section(self, word_data):
        with ui.card().classes('w-full mt-4 p-4'):
            ui.label('Create Flashcard Album').classes('text-lg font-semibold mb-2')
            
            # Album creation section
            with ui.row().classes('w-full gap-2 mb-4'):
                self.new_album_input = ui.input(label='New Flashcard Album Name').classes('flex-grow')
                ui.button('Create', on_click=lambda: self.create_album()).props('rounded').classes('bg-pink text-white')
            
            # Add to existing album section
            with ui.row().classes('w-full gap-2 items-center'):
                albums = self.backend.get_albums_list()
                if albums != []:
                    self.album_select = ui.select(
                        options=albums,
                        label='Select Existing Flashcard Album'
                    ).classes('flex-grow')
                    
                    # Custom definition input
                    self.custom_def_input = ui.textarea(
                        label='Your custom definition (optional)',
                        placeholder='Enter your own definition or notes for this word...'
                    ).classes('w-full mt-2')
                    
                    ui.button('Add to Flashcard Album', 
                            on_click=lambda: self.add_to_flashcard(word_data)) \
                        .props('rounded').classes('bg-pink text-white')
                else:
                    ui.label('Create a flashcard album above to add flashcards').classes('text-gray-500')

    def create_album(self):
        success, message = self.backend.create_album(self.new_album_input.value)
        if success:
            self.new_album_input.value = ''
            if hasattr(self, 'album_select'):
                self.album_select.options = self.backend.get_albums_list()
                self.album_select.update()
            ui.notify(message, type='success')
        else:
            ui.notify(message, type='warning')

    def add_to_flashcard(self, word_data):
        if not hasattr(self, 'album_select') or not self.album_select.value:
            ui.notify("Please select a flashcard album", type='warning')
            return

        custom_def = self.custom_def_input.value.strip() if hasattr(self, 'custom_def_input') else None
        success, message = self.backend.add_to_album(
            self.album_select.value, 
            word_data, 
            custom_def
        )

        if success:
            if hasattr(self, 'custom_def_input'):
                self.custom_def_input.value = ''
            ui.notify(message, type='success')
        else:
            ui.notify(message, type='warning')

    def setup_ui(self):
        self.container_ui =  ui.column().style('width: 144%; height: 80px; padding: 20px;').classes('p-8 flex-1').style('background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(20px);')
        with self.container_ui:
            with ui.row().classes('w-full items-center gap-4 mb-6'):
                ui.icon('school', size='32px').classes('text-pink-600')
                ui.label('DICTIONARY').classes('text-2xl font-bold text-pink-600')
                
            # Search section
            with ui.row().classes('w-full gap-2 items-center'):
                self.input_word = ui.input(label='Search word').classes('flex-grow')
                self.input_word.on('keypress.enter', self.search_word)
                ui.button('Search', on_click=self.search_word).props('rounded').classes('bg-pink text-white')
                
            # Results container
            self.result_container = ui.column().classes('w-full mt-4 gap-4')

def main():
    app = DictionaryUI()
    ui.run(title='Dictionary', favicon='🎓')

if __name__ in {"__main__", "__mp_main__"}:
    main()