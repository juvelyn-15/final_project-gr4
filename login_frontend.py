from nicegui import ui
from login_backend import User, UserDatabase, user_db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from typing import List, Dict

class NiceGUIPages:
    def __init__(self):
        self.nav_items = [
            {"name": "Home", "url": "/", "icon": "home"},
            {"name": "Explore", "url": "/explore", "icon": "explore"},
            {"name": "Help", "url": "/help", "icon": "help"}
        ]
        self.setup_login_page()
        self.setup_register_page()
        self.setup_forgot_password_page()
        self.setup_verify_account_page()
        self.setup_reset_password_page()
        #self.setup_home_page()

    def create_intro_page(self):
        # Set page background and styles
        ui.query('body').style(
            '''
            background: rbga(255, 200, 210, 0.9);
            backdrop-filter: blur(10px);
            margin: 0;
            padding: 0;
            min-height: 100vh;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            '''
        )

        # Header
        with ui.header().classes('w-full').style('background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(10px);'):
            with ui.row().classes('w-full max-w-7xl mx-auto justify-between items-center p-4'):
                # Logo section
                with ui.row().classes('items-center gap-2'):
                    ui.icon('auto_stories').classes('text-3xl text-pink-600')
                    ui.label('MYMY').classes('text-2xl font-bold text-pink-600')
                
                # Navigation
                with ui.row().classes('space-x-6'):
                    for item in self.nav_items:
                        with ui.row().classes('items-center gap-2 cursor-pointer hover:text-pink-600 transition-colors duration-200 '):
                            ui.icon(item['icon']).classes('text-pink-600')
                            ui.link(item['name'], item['url']).classes(
                                'text-gray-700 hover:text-pink-600 transition-colors duration-200'
                            )

    def create_centered_container(self):
        return ui.element('div').style('position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 100%; max-width: 400px;')

    def get_date_limits(self):
        today = datetime.now()
        max_date = today.strftime('%Y-%m-%d')
        min_date = (today - timedelta(days=365 * 100)).strftime('%Y-%m-%d')
        return min_date, max_date

    def redirect(self, url: str):
        ui.run_javascript(f'window.location.href = "{url}"')

    def setup_login_page(self):
        @ui.page('/login')
        def login_page():
            self.create_intro_page()
            with self.create_centered_container():
                with ui.card().classes('w-full p-8 rounded-lg shadow-lg'):
                    ui.label('Log in').classes('text-3xl font-bold text-center mb-6')
                    
                    with ui.column().classes('w-full gap-4'):
                        username_input = ui.input('Your username...').props('rounded').props('outlined required').classes('w-full')    
                        password_input = ui.input('Enter password...').props('rounded').props('outlined required type=password').classes('w-full')
                        
                        ui.link('Forgot password?', '/forgot-password').classes('text-pink-500 text-center hover:text-pink-700 cursor-pointer no-underline')
                        
                        async def handle_login():
                            success, message = user_db.authenticate_user(username_input.value, password_input.value)
                            ui.notify(message, color='positive' if success else 'negative')
                            if success:
                                user_db.set_user_status_on_by_username(username_input.value)
                                self.redirect('http://localhost:8080/')

                        ui.button('LOG IN', on_click=handle_login).props('rounded').classes('w-full bg-pink hover:bg-pink-600 text-white font-semibold py-2 rounded-lg shadow-md')
                        
                        with ui.row().classes('w-full justify-center items-center gap-2 mt-4'):
                            ui.label('Do not have account yet?').classes('text-center')
                            ui.link('Create account', '/register').classes('text-pink-500 hover:text-pink-700 cursor-pointer no-underline')

    def setup_register_page(self):
        @ui.page('/register')
        def register_page():
            self.create_intro_page()
            min_date, max_date = self.get_date_limits()
            
            with self.create_centered_container():
                with ui.card().classes('w-full p-8 rounded-lg shadow-lg'):
                    ui.label('Sign up').classes('text-3xl front-bold text-center mb-6')
                    
                    with ui.column().classes('w-full gap-4') as form_container:
                        username_input = ui.input('User name*').props('rounded').props('outlined required').classes('w-full')
                        fullname_input = ui.input('Full name*').props('rounded').props('outlined required').classes('w-full')
                        email_input = ui.input('Email*').props('rounded').props('outlined required type=email').classes('w-full')
                        birthdate_input = ui.input('Date of birth*').props('rounded').props(f'outlined required type=date min="{min_date}" max="{max_date}"').classes('w-full')
                        password_input = ui.input('Password*').props('rounded').props('outlined required type=password').classes('w-full')
                        confirm_password_input = ui.input('Confirm password*').props('rounded').props('outlined required type=password').classes('w-full')
                        
                        ui.label('* Please enter correctly and remember the information to retrieve your password when necessary').classes('text-red-500 text-sm mb-2')

                        register_button = ui.button('SIGN UP').props('rounded').classes('w-full bg-pink hover:bg-pink text-white font-semibold py-2 rounded-lg shadow-md')
                        
                        async def validate_and_register():

                            #Check email,username
                            if user_db.find_user_by_email(email_input.value):
                                 ui.notify('Existed email', color = 'negative')
                            if not '@' in email_input.value:
                                 ui.notify('Invalid email!', color='negative')
                                 return
                            if user_db.find_user_by_username(username_input.value):
                                 ui.notify('Existed username', color = 'negative')

                            # Kiểm tra ngày sinh
                            if not birthdate_input.value:
                                 ui.notify('Please enter your date of birth!', color='negative')
                                 return
                    
                            # Kiểm tra định dạng ngày
                            input_date = datetime.strptime(birthdate_input.value, '%Y-%m-%d')
                            min_date_obj = datetime.strptime(min_date, '%Y-%m-%d')
                            max_date_obj = datetime.strptime(max_date, '%Y-%m-%d')

                            # Validate ngày sinh
                            if input_date < min_date_obj or input_date > max_date_obj:
                                 birthdate_input.value = min_date
                                 ui.notify('Invalid date of birth', color='negative')
                                 return
                    
                            # Kiểm tra mật khẩu
                            # Yêu cầu độ mạnh của mật khẩu
                            if len(password_input.value) < 8 or not any(char.isupper() for char in password_input.value) or not any(char.isdigit() for char in password_input.value):
                                 ui.notify('Password must be at least 8 characters long, contain at least 1 uppercase letter, 1 lowercase letter, 1 number.', color='negative')
                                 return
                            if password_input.value != confirm_password_input.value:
                                 ui.notify('Password does not match!', color='negative')
                                 return
                    
                            # Tạo user mới
                            new_user = User(
                                 username=username_input.value,
                                 fullname=fullname_input.value,
                                 email=email_input.value,
                                 birthdate=birthdate_input.value,
                                 password=password_input.value
                            )
                    
                            # Thêm user vào database
                            success, message = user_db.add_user(new_user)
                            if success:
                                 print(f"User registered: {new_user.__dict__}")

                            ui.notify(message, color='positive' if success else 'negative')
                            if success:
                                 register_button.visible = False
                                 ui.link('Back to log in', '/login').classes('w-full text-center text-pink-500 hover:text-pink-700 cursor-pointer no-underline')
                            
                        register_button.on_click(validate_and_register)

    def setup_forgot_password_page(self):
        @ui.page('/forgot-password')
        def forgot_password_page():
            self.create_intro_page()
            with self.create_centered_container():
                with ui.card().classes('w-full p-8 rounded-lg shadow-lg'):
                    ui.label('Find your account').classes('text-3xl font-bold text-center mb-6')
                    
                    with ui.column().classes('w-full gap-4'):
                        ui.label('* Please enter your registered email').classes('text-red-500 text-sm mb-2')
                        email_input = ui.input('Email').props('rounded').props('outlined required').classes('w-full')
                        
                        async def verify_email():
                            if not '@' in email_input.value:
                                 ui.notify('Invalid email!', color='negative')
                                 return
                    
                            user = user_db.find_user_by_email(email_input.value)
                            if user:
                                 ui.notify('Account found! Verify informaion', color='positive')
                                 ui.timer(2.0, lambda: self.redirect(f'/verify-account/{user.username}'))
                            else:
                                 ui.notify('No account found', color='negative')

                        ui.button('Continue', on_click=verify_email).props('rounded').classes('w-full bg-pink text-white')
                        
                        with ui.row().classes('w-full justify-center items-center gap-2 mt-4'):
                            ui.link('Back to log in', '/login').classes('text-pink-500 hover:text-pink-700 cursor-pointer no-underline')

    def setup_verify_account_page(self):
        @ui.page('/verify-account/{username}')
        def verify_account_page(username: str):
            self.create_intro_page()
            min_date, max_date = self.get_date_limits()
        
            with self.create_centered_container():
                with ui.card().classes('w-full p-8 rounded-lg shadow-lg'):
                    ui.label('Verify information').classes('text-3xl font-bold text-center mb-6')
                
                    with ui.column().classes('w-full gap-4'):
                        ui.label('* Please enter correct registration information').classes('text-red-500 text-sm mb-2')
                        fullname_input = ui.input('Full Name*').props('rounded').props('outlined required').classes('w-full')
                        birthdate_input = ui.input('Date of birth*').props('rounded').props(f'outlined required type=date min="{min_date}" max="{max_date}"').classes('w-full')
                    
                        async def verify_info():
                            user = user_db.find_user_by_username(username)
                            if user and user.fullname.strip().lower() == fullname_input.value.strip().lower() and user.birthdate == birthdate_input.value:
                                ui.notify('Verified successfully! Reset password...', color='positive')
                                ui.timer(2.0, lambda: self.redirect(f'/reset-password/{username}'))
                            else:
                                ui.notify('Incorrect information!', color='negative')

                        ui.button('Verify', on_click=verify_info).props('rounded').classes('w-full bg-pink text-white')
                    
                        with ui.row().classes('w-full justify-center items-center gap-2 mt-4'):
                            ui.link('Back', '/forgot-password').classes('text-pink-500 hover:text-pink-700 cursor-pointer no-underline')
    def setup_reset_password_page(self):
        @ui.page('/reset-password/{username}')
        def reset_password_page(username: str):
            self.create_intro_page()
            with self.create_centered_container():
                with ui.card().classes('w-full p-6'):
                    ui.label('Reset password').classes('text-3xl font-bold text-center mb-6')
                    
                    with ui.column().classes('w-full gap-4'):
                        new_password = ui.input('New password*')\
                            .props('outlined required type=password').props('rounded')\
                            .classes('w-full')
                        
                        confirm_password = ui.input('Verify new password*')\
                            .props('rounded').props('outlined required type=password')\
                            .classes('w-full')
                        
                        reset_button = ui.button('Change password')\
                            .props('rounded').classes('w-full bg-pink text-white')
                        
                        async def reset_password():
                            if len(new_password.value) < 8 or not any(char.isupper() for char in new_password.value) or not any(char.isdigit() for char in new_password.value):
                                 ui.notify('Password must be at least 8 characters long, contain at least 1 uppercase letter, 1 lowercase letter, 1 number.', color='negative')
                                 return
                            # Kiểm tra xem hai mật khẩu có khớp nhau không
                            if new_password.value != confirm_password.value:
                                 ui.notify('Password does not match!', color='negative')
                                 return
                    
                            # Tìm user trong database
                            user = user_db.find_user_by_username(username)
                            if user:
                                # Cập nhật mật khẩu mới đã được mã hóa
                                user.password_hash = generate_password_hash(new_password.value)
                                user_db.update_user_password(user.username, user.password_hash)
                                # Hiển thị thông báo thành công
                                ui.notify('Change password successfully!', color='positive')
                                # Ẩn nút đặt lại mật khẩu
                                reset_button.visible = False
                                # Hiển thị link quay về trang đăng nhập
                                ui.link('Back to log in', '/login')\
                                    .classes('w-full text-center text-pink-500 hover:text-pink-700 cursor-pointer no-underline')
                            else:
                                # Hiển thị thông báo lỗi nếu không tìm thấy user
                                ui.notify('Error occurred!', color='negative')
                        reset_button.on_click(reset_password)

    #def setup_home_page(self):
    #    @ui.page('/home')
    #    def home_page():
    #        DashboardApp()

    def run(self):
        # Set up all pages
        '''self.setup_login_page()
        self.setup_register_page()
        self.setup_forgot_password_page()
        self.setup_verify_account_page()
        self.setup_reset_password_page()
        self.setup_home_page()'''

        # Run the application
        ui.run()

# Usage
if __name__ in {"__main__", "__mp_main__"}:
    app = NiceGUIPages()
    app.run()