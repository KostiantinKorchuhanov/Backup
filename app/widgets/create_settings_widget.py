import customtkinter
import shelve

class SettingsWindow:
    def __init__(self, app):
        self.app = app
        self.top_level_settings = None
        self.color_themes = ["blue", "green"]

    def create_settings(self):
        if self.top_level_settings and self.top_level_settings.winfo_exists():
            self.top_level_settings.lift()
            self.top_level_settings.focus()
            return

        with shelve.open("settings") as db:
            current_theme = db.get("theme", "System")

        self.top_level_settings = customtkinter.CTkToplevel(self.app)
        self.top_level_settings.geometry("300x250")
        self.top_level_settings.title("Settings")

        label_theme = customtkinter.CTkLabel(
            self.top_level_settings,
            text="Theme Settings",
            font=("Inter", 16)
        )
        label_theme.pack(side="top", pady=(10, 5))

        self.theme_options = customtkinter.CTkOptionMenu(
            self.top_level_settings,
            values=["System", "Dark", "Light"],
            command=self.change_theme
        )
        self.theme_options.set(current_theme)
        self.theme_options.pack(pady=(5, 5))

        label_colors = customtkinter.CTkLabel(
            self.top_level_settings,
            text="Color Settings",
            font=("Inter", 16)
        )
        label_colors.pack(side="top", pady=(10, 5))

        color_frame = customtkinter.CTkFrame(self.top_level_settings, fg_color="transparent")
        color_frame.pack(padx=10, pady=(5, 10))

        for i, color in enumerate(self.color_themes):
            color_button = customtkinter.CTkButton(
                color_frame, fg_color=color, width=30, height=30, text="",
                command=lambda button_color=color: self.change_color_theme(button_color)
            )
            color_button.grid(row=i//4, column=i%4, padx=(10, 5), pady=(10, 5))

    def change_theme(self, option):
        customtkinter.set_appearance_mode(option)
        with shelve.open("settings") as db:
            db["theme"] = option

    def change_color_theme(self, color):
        customtkinter.set_default_color_theme(color)
        with shelve.open("settings") as db:
            db["color_theme"] = color
