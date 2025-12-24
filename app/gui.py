import customtkinter
from PIL import Image
import json
import os
from datetime import datetime
from core.restore import RestoreFile
from customtkinter import CTkFont

current_dir = os.path.dirname(os.path.abspath(__file__))
data_file = os.path.join("database", "data.json")

def settings_pressed():
    pass

def restore_pressed(id):
    RestoreFile().restore_file(id)
    refresh_items()

def refresh_items():
    for widget in scrollable_frame.winfo_children():
        widget.destroy()
    create_items()

def create_items():
    with open(data_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    for item in data:
        frame_item = customtkinter.CTkFrame(scrollable_frame, border_width=1)
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
        textbox.tag_config("font_1", cnf={"font":font_1})
        textbox.tag_config("font_2", cnf={"font":font_2})
        textbox.pack(side="left", padx=3, pady=(3, 3))
        textbox.configure(state="disabled")

        icon_restore_path_dark = os.path.join(current_dir, "image", "undo_dark.png")
        icon_restore_path_light = os.path.join(current_dir, "image", "undo_light.png")
        icon_restore = customtkinter.CTkImage(
            light_image=Image.open(icon_restore_path_light),
            dark_image=Image.open(icon_restore_path_dark),
            size=(35, 35)
        )
        id = item["ID"]
        restore_button = customtkinter.CTkButton(frame_item, image=icon_restore, text="", command= lambda file_id=id: restore_pressed(file_id), fg_color="gray", height=45, width=45)
        restore_button.pack(side="top", anchor="nw",padx=5, pady=5)

def main():
    global app, scrollable_frame, font_1, font_2
    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("blue")

    app = customtkinter.CTk()
    app.geometry("700x600")
    app.title("Backtrack")

    font_1 = CTkFont("Georgia", 18)
    font_2 = CTkFont("Arial", 14, slant="italic")

    panel = customtkinter.CTkFrame(app, height=50)
    panel.pack(side="top", fill="x", padx=10, pady=10)

    icon_settings_path = os.path.join(current_dir, "image", "settings.png")
    icon_settings = customtkinter.CTkImage(
        light_image=Image.open(icon_settings_path),
        dark_image=Image.open(icon_settings_path),
        size=(35, 35)
    )
    settings = customtkinter.CTkButton(panel, image=icon_settings, text="", command=settings_pressed, width=40)
    settings.pack(side="right", padx=10, pady=5)

    scrollable_frame = customtkinter.CTkScrollableFrame(app)
    scrollable_frame.pack(side="top", fill="both", expand=True, padx=10, pady=(0, 10))

    create_items()
    app.mainloop()

main()