import customtkinter
from PIL import Image
import json
import os


data_file = os.path.join("database", "data.json")

def settings_pressed():
    pass

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("600x600")
app.title("Backtrack")

panel = customtkinter.CTkFrame(app, height=50)
panel.pack(side="top", fill="x", padx=10, pady=10)

current_dir = os.path.dirname(os.path.abspath(__file__))
icon_path = os.path.join(current_dir, "image", "settings.png")
icon_settings = customtkinter.CTkImage(
    light_image=Image.open(icon_path),
    dark_image=Image.open(icon_path),
    size=(35, 35)
)
settings = customtkinter.CTkButton(panel, image=icon_settings, text="", command=settings_pressed, width=40)
settings.pack(side="right", padx=10, pady=5)

scrollable_frame = customtkinter.CTkScrollableFrame(app)
scrollable_frame.pack(side="top", fill="both", expand=True, padx=10, pady=(0, 10))


def create_items():
    with open(data_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    for item in data:
        frame_item = customtkinter.CTkFrame(scrollable_frame)
        frame_item.pack(side="top", fill="x")

        textbox = customtkinter.CTkTextbox(frame_item, height=70, font=("Arial", 16))
        if item["File name"]:
            file_name = f"File name: {str(item["File name"])}\n"
        if item["Original path"]:
            original_path = f"Original path: {str(item["Original path"])}"
        textbox.insert("0.0", file_name)
        textbox.insert("10.10",original_path)
        textbox.pack(side="top", fill="x", padx=3, pady=(3, 0))
        textbox.configure(state="disabled")

create_items()

app.mainloop()