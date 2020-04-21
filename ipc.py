from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.image import Image as Im
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.slider import Slider
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListLayout
from kivy.uix.popup import Popup
from kivy.graphics import Color, Ellipse, Line
from kivy.properties import ObjectProperty
from PIL import Image
import os

image_path=""
im = None

class CustomPopup(Popup):

    fc = ObjectProperty(None)
    txt_input = ObjectProperty(None)

    def update_text_input(self):
        for i in self.fc.selection:
            self.txt_input.text=i

    def close_save_file_popup(self):
        popup.dismiss()

    def open_image(self):

        global image_path
        global im

        for i in self.fc.selection:
            image_path=i

        if os.system("cd tmp")!=0:
            os.system("mkdir -p ./tmp")
            os.system("mount -t ramfs -o size=50m ramfs ./tmp")
        os.system("cp " + image_path + " ./tmp/")
                
        c = len(image_path)-1
        while image_path[c]!='/' and c>0:
            c=c-1
        c=c+1
        file_name = image_path[c:]
        
        image_path=image_path [:c]
        image_path=image_path + "tmp/" + file_name

        im = Image.open(image_path)
        print(image_path)
        #IPC().reload_image() ne radi iz nekog razloga mora da se pozove iz IPC klase
        self.dismiss()


    def save_file(self):

        self.dismiss()

        if self.txt_input!="":
            url=self.txt_input.text
            ext=self.txt_input.text[self.txt_input.text.index('.')+1:]
        try:
            ext=ext.upper()
            if ext=='BMP' or ext=='JPEG' or ext=='PNG':
                image=im.convert('RGB')
                image.save(url,ext)
                pass
        except ValueError:
            print('ValueError')
        except IOError:
            print('IOError')

class IPC(FloatLayout):
    selection_tool = ObjectProperty(None)
    resize_tool = ObjectProperty(None)
    crop_tool = ObjectProperty(None)
    laso_tool = ObjectProperty(None)
    save_file_popup = ObjectProperty(None)
    img_id = ObjectProperty(None)
    current_path="./"
    area_start = None
    area_end = None
    active_tool = None
    

    def init(self):
        pass

    
    def on_touch_down(self,touch):
        global im
        print(self.area_start)
        if (self.active_tool == self.selection_tool) and (touch.osx>0.3 or touch.osy>0.3):
            self.area_start = [(touch.osx-0.3)*(1/0.7)*im.width,((touch.osy-0.15)*(1/0.85))*im.height]
        if self.disabled and self.collide_point(*touch.pos):
            return True
        for child in self.children[:]:
            if child.dispatch('on_touch_down', touch):
                return True

    def on_touch_up(self,touch):
        global im
        if (self.active_tool == self.selection_tool) and (touch.osx>0.3 or touch.osy>0.3):
            self.area_end = [(touch.osx-0.3)*(1/0.7)*im.width,((touch.osy-0.15)*(1/0.85))*im.height]
        if self.disabled:
            return
        for child in self.children[:]:
            if child.dispatch('on_touch_up', touch):
                return True
    
    def reload_image(self):
        global image_path
        self.img_id.source=image_path
        self.img_id.reload()

    def open_file(self):
        popup = CustomPopup()
        popup.open()

    def save_temp_image(self):
        global image_path
        url=image_path
        ext=image_path[image_path.index('.')+1:]
        try:
            ext=ext.upper()
            if ext=='BMP' or ext=='JPEG' or ext=='PNG':
                image=im.convert('RGB')
                image.save(url,ext)
                pass
        except ValueError:
            print('ValueError')
        except IOError:
            print('IOError')

    def activate_selection_tool(self):
        self.active_tool=self.selection_tool


class IPCApp(App):
    
    def build(self):
        return IPC()

if __name__ == '__main__':
    IPCApp().run()