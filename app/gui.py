import shelve
import customtkinter
from PIL import Image
import os
from app.widgets.create_backup_widget import BackupWindow
from customtkinter import CTkFont
from app.widgets.create_items_widget import ItemsWindow
from app.widgets.create_settings_widget import SettingsWindow
from app.logging_config import setup_logging

current_dir = os.path.dirname(os.path.abspath(__file__))
data_file = os.path.join("database", "data.json")
top_level_add = None

def main():
    setup_logging()
    global app, scrollable_frame, font_1, font_2

    with shelve.open("settings") as db:
        saved_theme = db.get("theme", "System")
        saved_color = db.get("color_theme", "blue")

    customtkinter.set_appearance_mode(saved_theme)
    customtkinter.set_default_color_theme(saved_color)

    app = customtkinter.CTk()
    app.geometry("700x600")
    app.title("Backtrack")

    font_1 = CTkFont("Inter", 18)
    font_2 = CTkFont("Inter", 14, slant="italic")

    panel = customtkinter.CTkFrame(app, height=50)
    panel.pack(side="top", fill="x", padx=10, pady=10)

    scrollable_frame = customtkinter.CTkScrollableFrame(app)
    scrollable_frame.pack(side="top", fill="both", expand=True, padx=10, pady=(0, 10))

    items_window = ItemsWindow(
        scrollable_frame=scrollable_frame,
        data_file=data_file,
        font_1=font_1,
        font_2=font_2,
        current_dir=current_dir
    )

    icon_settings_path_light = os.path.join(current_dir, "image", "settings_light.png")
    icon_settings_path_dark = os.path.join(current_dir, "image", "settings_dark.png")
    icon_settings = customtkinter.CTkImage(
        light_image=Image.open(icon_settings_path_light),
        dark_image=Image.open(icon_settings_path_dark),
        size=(35, 35)
    )
    settings_pressed = SettingsWindow(app)
    settings = customtkinter.CTkButton(panel, image=icon_settings, text="", command=settings_pressed.create_settings, width=40, fg_color="gray")
    settings.pack(side="right", padx=10, pady=5)

    icon_add_path_light = os.path.join(current_dir, "image", "add_light.png")
    icon_add_path_dark = os.path.join(current_dir, "image", "add_dark.png")
    icon_add = customtkinter.CTkImage(
        light_image=Image.open(icon_add_path_light),
        dark_image=Image.open(icon_add_path_dark),
        size=(35, 35)
    )
    add = customtkinter.CTkButton(panel, image=icon_add, text="", command=BackupWindow(app, font_1).create_backup, width=40, fg_color="gray")
    add.pack(side="left", padx=10, pady=10)

    icon_reload_path_dark = os.path.join(current_dir, "image", "reload_dark.png")
    icon_reload = customtkinter.CTkImage(
        light_image=Image.open(icon_reload_path_dark),
        dark_image=Image.open(icon_reload_path_dark),
        size=(35, 35)
    )
    reload = customtkinter.CTkButton(panel, image=icon_reload, text="", command=items_window.refresh_items, width=40, fg_color="gray")
    reload.pack(side="left", padx=10, pady=10)

    items_window.create_items()
    app.mainloop()

if __name__ == '__main__':
    main()