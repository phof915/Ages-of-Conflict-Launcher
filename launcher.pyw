import os
import shutil
import subprocess
from tkinter import Tk, ttk, Label, Listbox, Scrollbar, Button, RIGHT, LEFT, Y, VERTICAL, END, Text, Frame, BOTTOM, CENTER

class UnityLauncherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AOC Launcher (unofficial)")
        self.root.state("zoomed")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        # Create tabs
        self.create_tab("AOC Versions", "AOC Versions")
        self.create_tab("AOC Demos", "AOC Demos")

    def create_tab(self, tab_title, folder_name):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=tab_title)

        # UI elements
        source_folder_label = Label(tab, text=f"{tab_title}:", font=("Arial", 20))
        source_folder_label.pack(pady=10)

        frame = Frame(tab)
        frame.pack(side=LEFT, fill="both", expand=True)

        source_folder_listbox = Listbox(frame, font=("Arial", 18), selectmode="SINGLE", exportselection=False)
        source_folder_listbox.pack(side=LEFT, fill="both", expand=True)

        scrollbar = Scrollbar(frame, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y)
        scrollbar.config(command=source_folder_listbox.yview)
        source_folder_listbox.config(yscrollcommand=scrollbar.set)

        play_button = Button(tab, text="Play", font=("Arial", 24), command=lambda: self.launch_game(folder_name, source_folder_listbox))
        play_button.pack(pady=10, side=BOTTOM, anchor=CENTER)

        info_text = Text(tab, font=("Arial", 10), height=10, width=30, wrap="word", state="disabled")
        info_text.pack(side=RIGHT, fill="both", expand=True)

        # Bind the selection event to update the info_text
        source_folder_listbox.bind("<<ListboxSelect>>", lambda event: self.update_info_text(folder_name, source_folder_listbox, info_text))

        # Variables
        source_folders = self.get_source_folders(folder_name)

        # Set default folder in the code
        default_folder_path = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Ages of Conflict World War Simulator"
        executable_name = "Ages of Conflict.exe"

        # Set initial values in UI
        source_folder_listbox.insert(END, *source_folders)
        source_folder_listbox.select_set(0)

        # Display initial message in the info panel
        self.display_info_message(info_text, "No version selected.")

    def get_source_folders(self, folder_name):
        # Get a list of source folders from the specified subfolder
        source_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), folder_name)
        return [item for item in os.listdir(source_folder) if os.path.isdir(os.path.join(source_folder, item))]

    def replace_folders(self, folder_name, source_folder_listbox):
        selected_index = source_folder_listbox.curselection()
        if not selected_index:
            print("Please select a source folder.")
            return

        source_folder_name = source_folder_listbox.get(selected_index)
        source_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), folder_name, source_folder_name)
        destination_folder = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Ages of Conflict World War Simulator"

        # Files that should not be removed
        preserved_files = ["Ages of Conflict.exe", "UnityPlayer.dll", "UnityCrashHandler64.exe"]

        try:
            # Ensure that both source and destination folders exist
            if not os.path.exists(source_folder) or not os.path.exists(destination_folder):
                print("Source or destination folder does not exist.")
                return

            # Delete the contents of the destination folder, excluding preserved files
            for item in os.listdir(destination_folder):
                item_path = os.path.join(destination_folder, item)
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                elif item not in preserved_files:
                    os.remove(item_path)

            # Copy the contents from the source folder to the destination folder, excluding preserved files
            for item in os.listdir(source_folder):
                source_item = os.path.join(source_folder, item)
                destination_item = os.path.join(destination_folder, item)

                if os.path.isdir(source_item):
                    shutil.copytree(source_item, destination_item, symlinks=True)
                elif item not in preserved_files:
                    shutil.copy2(source_item, destination_item)

            print("Contents replaced successfully.")
        except Exception as e:
            print(f"Error replacing contents: {e}")

    def launch_game(self, folder_name, source_folder_listbox):
        self.replace_folders(folder_name, source_folder_listbox)

        # Assuming the game executable is named "Ages of Conflict.exe"
        game_exe_path = os.path.join("C:\\Program Files (x86)\\Steam\\steamapps\\common\\Ages of Conflict World War Simulator", "Ages of Conflict.exe")

        if os.path.exists(game_exe_path):
            subprocess.Popen([game_exe_path])
            print("Game launched.")
        else:
            print("Game executable Ages of Conflict.exe not found.")

    def update_info_text(self, folder_name, source_folder_listbox, info_text):
        selected_index = source_folder_listbox.curselection()
        if not selected_index:
            # Display message when no version is selected
            self.display_info_message(info_text, "No version selected.")
            return

        source_folder_name = source_folder_listbox.get(selected_index)
        source_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), folder_name, source_folder_name)
        info_file_path = os.path.join(source_folder, "info.txt")

        try:
            with open(info_file_path, "r", encoding="utf-8") as info_file:
                info_content = info_file.read()
                info_text.config(state="normal")  # Enable editing temporarily
                info_text.delete(1.0, END)
                info_text.insert(END, info_content)
                info_text.config(state="disabled")  # Make the text widget read-only
        except FileNotFoundError:
            info_text.config(state="normal")
            info_text.delete(1.0, END)
            info_text.insert(END, "info.txt not found.")
            info_text.config(state="disabled")

    def display_info_message(self, info_text, message):
        info_text.config(state="normal")
        info_text.delete(1.0, END)
        info_text.insert(END, message)
        info_text.config(state="disabled")

if __name__ == "__main__":
    root = Tk()
    app = UnityLauncherApp(root)
    root.mainloop()
