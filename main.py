from kivy.core.window import Window
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivymd.toast import toast
import webbrowser
from kivy.utils import platform
import os

# Only set window size for desktop debugging
if platform not in ['android', 'ios']:
    Window.size = (360, 640)

# Constants (Unchanged)
URL_TRAIN = "https://gleeful-lokum-c4db9b.netlify.app/"
URL_RECORDS = "https://gleeful-lokum-c4db9b.netlify.app/train_information"
URL_POWERBLOCK = "https://gleeful-lokum-c4db9b.netlify.app/power%20block%20certificate%20&%20record"
URL_JOBCARD = "https://gleeful-lokum-c4db9b.netlify.app/Raise_Jobcard"
URL_POWERBLOCK_RECORDS = "https://gleeful-lokum-c4db9b.netlify.app/powerblock_record"
URL_JOBCARD_RECORDS = "https://gleeful-lokum-c4db9b.netlify.app/jobcard_record"

DEMO_EMAIL = "PPIO@example.com"
DEMO_PASSWORD = "admin123"
DEMO_PASSWORD_USER = "pass123"

KV = '''
ScreenManager:
    LoginScreen:
    HomeScreen:

<LoginScreen>:
    name: "login"
    MDFloatLayout:
        md_bg_color: app.theme_cls.bg_normal
        FitImage:
            source: "upmrclogo.jpeg"
            pos_hint: {"center_x": .5, "center_y": .9}
            size_hint: .4, .25

        MDLabel:
            text: "Kanpur Metro Depot"
            halign: "center"
            pos_hint: {"center_x": .5, "center_y": .75}
            font_style: "H5"

        MDTextField:
            id: email
            hint_text: "Email"
            pos_hint: {"center_x": .5, "center_y": .65}
            size_hint_x: .85
            icon_right: "email"
            mode: "rectangle"

        MDTextField:
            id: password
            hint_text: "Password"
            password: True
            pos_hint: {"center_x": .5, "center_y": .55}
            size_hint_x: .85
            icon_right: "lock"
            mode: "rectangle"

        MDRaisedButton:
            text: "Login"
            pos_hint: {"center_x": .5, "center_y": .42}
            size_hint_x: .5
            on_release: app.on_login(email.text, password.text)

        MDLabel:
            id: error_lbl
            text: ""
            halign: "center"
            theme_text_color: "Error"
            pos_hint: {"center_x": .5, "center_y": .30}

<HomeScreen>:
    name: "home"
    MDBoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(15)

        MDLabel:
            text: "Dashboard"
            halign: "center"
            font_style: "H4"
            size_hint_y: None
            height: dp(80)

        MDRaisedButton:
            text: "Train Information"
            size_hint: 1, .2
            md_bg_color: 1, 0.647, 0, 1
            on_release: app.on_button_press_index()

        MDRaisedButton:
            text: "Request Job Card"
            size_hint: 1, .2
            md_bg_color: 0, 0, 1, 1
            on_release: app.on_button_press_jobcard()

        MDRaisedButton:
            text: "Request Power Block"
            size_hint: 1, .2
            md_bg_color: 1, 0, 0, 1
            on_release: app.on_button_press_powerblock()

        Widget: # Spacer

        MDRectangleFlatButton:
            text: "Logout"
            pos_hint: {"center_x": .5}
            on_release: app.logout()
'''


class LoginScreen(Screen):
    pass


class HomeScreen(Screen):
    pass


class LoginApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"

        # Safe initialization of JsonStore
        store_path = os.path.join(self.user_data_dir, 'user_store.json')
        self.store = JsonStore(store_path)

        self.root_widget = Builder.load_string(KV)

        # Auto-login if session exists
        if self.store.exists("session"):
            self.root_widget.current = "home"

        return self.root_widget

    def on_login(self, email, password):
        # Using self.root_widget instead of self.root to ensure reliability
        screen = self.root_widget.get_screen("login")
        if not email or not password:
            screen.ids.error_lbl.text = "Enter email and password."
            return

        if (email == DEMO_EMAIL and password == DEMO_PASSWORD) or \
                (email == DEMO_EMAIL and password == DEMO_PASSWORD_USER):
            self.store.put("session", logged_in=True, email=email, password=password)
            self.root_widget.current = "home"
            toast("Login successful")
        else:
            screen.ids.error_lbl.text = "Invalid credentials."

    def get_user_pass(self):
        if self.store.exists("session"):
            return self.store.get("session").get("password")
        return None

    def open_url(self, url):
        """Universal URL opener"""
        try:
            webbrowser.open(url)
        except Exception as e:
            toast("Could not open browser")

    def on_button_press_jobcard(self):
        pw = self.get_user_pass()
        url = URL_JOBCARD if pw == DEMO_PASSWORD_USER else URL_JOBCARD_RECORDS
        self.open_url(url)

    def on_button_press_index(self):
        pw = self.get_user_pass()
        url = URL_RECORDS if pw == DEMO_PASSWORD_USER else URL_TRAIN
        self.open_url(url)

    def on_button_press_powerblock(self):
        pw = self.get_user_pass()
        url = URL_POWERBLOCK if pw == DEMO_PASSWORD_USER else URL_POWERBLOCK_RECORDS
        self.open_url(url)

    def logout(self):
        if self.store.exists("session"):
            self.store.delete("session")
        self.root_widget.current = "login"
        self.root_widget.get_screen("login").ids.password.text = ""
        self.root_widget.get_screen("login").ids.email.text = ""
        toast("Logged out")


if __name__ == "__main__":
    LoginApp().run()