from kivy.app import App 
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder 
from filestack import Client
from kivy.uix.camera import Camera
import time
import webbrowser

#Creating a kivi file to build the frontend
Builder.load_file('frontend.kv')

#Basic layout

class CameraScreen(Screen):

    def start(self):
        self.ids.camera.play= True
        self.ids.camera_button.text="Stop Camera"
        self.ids.camera.texture = self.ids.camera._camera.texture

    def stop(self):
        self.ids.camera.play= False
        self.ids.camera_button.text="Start Camera"
        self.ids.camera.texture = None


    def capture(self):
        if self.ids.camera.play:
            current_time = time.strftime('%Y%m%d-%H%M%S')
            self.filename = f"images/{current_time}.png"
            self.ids.camera.export_to_png(self.filename)
            print(f"Captured image saved as {self.filename}")
            self.manager.current = 'image_screen' #navigates to the ImageScreen
            self.manager.current_screen.ids.img.source = self.filename #Display the Captured Screen in the ImageScreen

        else:
            print("Camera is not playing. Please start the camera first.")

class ImageScreen(Screen):

    link_message="Create a Link first!"
    def create_link(self):
        #Access the photo filepath and uploads to the web and creates a url
        file_path = App.get_running_app().root.ids.camera_screen.filename
        file_share = FileSharer(filepath=file_path)
        self.url = file_share.share()
        self.ids.link.text= self.url

    def copy_link(self):
        #Copies the link to the clipboard
        try:
            Clipboard.copy(self.url)
        except:
            self.ids.link.text=self.link_message

    def open_link(self):
        #Opens the link in the browser
        try:
            webbrowser.open(self.url)
        except:
            self.ids.link.text=self.link_message



class FileSharer:

    def __init__(self,filepath,api_key='APiD6hfRRI2GRSZSNHFDgz'):
        self.filepath=filepath
        self.api_key=api_key
    
    def share(self):
        client = Client(self.api_key)
        new_filelink = client.upload(filepath=self.filepath)
        return new_filelink.url


class RootWidget(ScreenManager):
    pass

class MyApp(App):

    def build(self):
        return RootWidget()

MyApp().run()


