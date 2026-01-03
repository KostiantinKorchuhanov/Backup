'''
import customtkinter

class WarningWindow:
    def __init__(self, master, font_1):
        self.master = master
        self.font_1 = font_1
        self.top_level_warning = None

    def create_warning(self, text):
        self.text = text
        if self.top_level_warning and self.top_level_warning.winfo_exists():
            self.top_level_warning.lift()
            self.top_level_warning.focus()
        else:
            self.top_level_warning = customtkinter.CTkToplevel(self.master)
            self.top_level_warning.title("Warning")
            self.top_level_warning.geometry("300x200")

        button_frame = customtkinter.CTkFrame(height=70)
        button_frame.pack(fill="x", side="bottom")

        self.top_level_warning.resizable(False, False)
        button_confirm = customtkinter.CTkButton(text="Confirm")
        button_confirm.pack()

'''