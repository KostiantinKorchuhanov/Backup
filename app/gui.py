import customtkinter
from PIL import Image
import json
import os
from datetime import datetime
from core.restore import RestoreFile
from core.cleaner import ClearByTime
from core.backup import BackupCreator
from customtkinter import CTkFont

current_dir = os.path.dirname(os.path.abspath(__file__))
data_file = os.path.join("database", "data.json")
top_level_add = None

def settings_pressed():
    pass

def create_backup():
    global top_level_add
    if top_level_add is None or not top_level_add.winfo_exists():
        top_level_add = customtkinter.CTkToplevel(app)
        top_level_add.title("Create a backup")
        top_level_add.geometry("700x200")
    else:
        top_level_add.focus()
        top_level_add.lift()

    label_path = customtkinter.CTkLabel(top_level_add, text="Full path to the file:", font=font_1)
    label_path.pack(side="top", anchor="n", padx=10, pady=(10, 5))

    entry_path = customtkinter.CTkEntry(top_level_add, placeholder_text="Path:", width=600)
    entry_path.pack(side="top", anchor="n", padx=10)

    label_time = customtkinter.CTkLabel(top_level_add, text="Time to store:", font=font_1)
    label_time.pack(side="top", anchor="n", padx=10, pady=(10, 5))

    time_frame = customtkinter.CTkFrame(top_level_add, fg_color="transparent")
    time_frame.pack(padx=10, pady=(10, 5))
    entry_time = customtkinter.CTkEntry(time_frame, placeholder_text="Time:", width=50)
    entry_time.pack(side="left", padx=10)

    def time_choosed(option):
        if option == "hour(s)":
            option = "h"
        else:
            option = "d"
        return option

    option_menu = customtkinter.CTkOptionMenu(time_frame, values=["hour(s)", "day(s)"], command=time_choosed)
    option_menu.pack(side="left")




def restore_pressed(id):
    RestoreFile().restore_file(id)
    refresh_items()

def refresh_items():
    ClearByTime().check_clean()
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
        restore_button.pack(side="top", anchor="nw", padx=5, pady=5)

def main():
    global app, scrollable_frame, font_1, font_2
    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("blue")

    app = customtkinter.CTk()
    app.geometry("700x600")
    app.title("Backtrack")

    font_1 = CTkFont("Inter", 18)
    font_2 = CTkFont("Inter", 14, slant="italic")

    panel = customtkinter.CTkFrame(app, height=50)
    panel.pack(side="top", fill="x", padx=10, pady=10)

    icon_settings_path = os.path.join(current_dir, "image", "settings.png")
    icon_settings = customtkinter.CTkImage(
        light_image=Image.open(icon_settings_path),
        dark_image=Image.open(icon_settings_path),
        size=(35, 35)
    )
    settings = customtkinter.CTkButton(panel, image=icon_settings, text="", command=settings_pressed, width=40, fg_color="gray")
    settings.pack(side="right", padx=10, pady=5)

    icon_add_path_light = os.path.join(current_dir, "image", "add_light.png")
    icon_add_path_dark = os.path.join(current_dir, "image", "add_dark.png")
    icon_add = customtkinter.CTkImage(
        light_image=Image.open(icon_add_path_light),
        dark_image=Image.open(icon_add_path_dark),
        size=(35, 35)
    )
    add = customtkinter.CTkButton(panel, image=icon_add, text="", command=create_backup, width=40, fg_color="gray")
    add.pack(side="left", padx=10, pady=10)


    scrollable_frame = customtkinter.CTkScrollableFrame(app)
    scrollable_frame.pack(side="top", fill="both", expand=True, padx=10, pady=(0, 10))

    create_items()
    app.mainloop()

main()