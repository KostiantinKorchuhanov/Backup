import customtkinter
import os
from PIL import Image
from core.cleaner import ClearByTime
from core.restore import RestoreFile
import json
from datetime import datetime


class ItemsWindow:
    def __init__(self, scrollable_frame, data_file, font_1, font_2, current_dir):
        self.scrollable_frame = scrollable_frame
        self.data_file = data_file
        self.font_1 = font_1
        self.font_2 = font_2
        self.current_dir = current_dir

    def restore_pressed(self, id):
        RestoreFile().restore_file(id)
        self.refresh_items()

    def refresh_items(self):
        ClearByTime().check_clean()
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.create_items()

    def create_items(self):
        with open(self.data_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        for item in data:
            frame_item = customtkinter.CTkFrame(self.scrollable_frame, border_width=1)
            frame_item.pack(side="top", fill="x", padx=2, pady=(2, 0))

            textbox = customtkinter.CTkTextbox(frame_item, height=100, width=500)
            if item["File name"]:
                file_name = f"File name: {str(item["File name"])}"
            if item["Original path"]:
                original_path = f"Original path: {str(item["Original path"])}"
            if item["Expire time"]:
                expire_time_isoformat = item["Expire time"]
                expire_time_converted = datetime.fromisoformat(expire_time_isoformat)
                expire_time = expire_time_converted.strftime("%d.%m.%Y at %H:%M:%S")
                expire_result = f"Expire time: {expire_time}"
            textbox.insert("end", file_name + "\n", "font_1")
            textbox.insert("end", expire_result + "\n", "font_1")
            textbox.insert("end", original_path, "font_2")
            textbox.tag_config("font_1", cnf={"font": self.font_1})
            textbox.tag_config("font_2", cnf={"font": self.font_2})
            textbox.pack(side="left", padx=3, pady=(3, 3))
            textbox.configure(state="disabled")

            icon_restore_path_dark = os.path.join(self.current_dir, "image", "undo_dark.png")
            icon_restore_path_light = os.path.join(self.current_dir, "image", "undo_light.png")
            icon_restore = customtkinter.CTkImage(
                light_image=Image.open(icon_restore_path_light),
                dark_image=Image.open(icon_restore_path_dark),
                size=(35, 35)
            )
            id = item["ID"]
            restore_button = customtkinter.CTkButton(frame_item, image=icon_restore, text="",
                                                         command=lambda file_id=id: self.restore_pressed(file_id),
                                                         fg_color="gray", height=45, width=45)
            restore_button.pack(side="top", anchor="nw", padx=5, pady=5)