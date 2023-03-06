import os
import shutil
import time
from datetime import datetime

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

FOLDERS = {
    "source": "/Users/user/Desktop/dev/bangkok-genomic/move-labs/source",
    "temp": "/Users/user/Desktop/dev/bangkok-genomic/move-labs/temp",
    "dest": "/Users/user/Desktop/dev/bangkok-genomic/move-labs/dest"
}

def get_source_files(source):
    """Get all files from source directory"""
    files = []
    for file in os.listdir(source):
        if os.path.isfile(os.path.join(source, file)):
            files.append(file)
    files.sort()

    return files

def validate_file_name(file_name):
    """Validate file name"""
    if len(file_name.split("_")) == 3:
        if file_name.split("_")[2].endswith(".pdf"):
            return True
    
    return False

def get_lab_name(file_name):
    """Get lab name from file name"""
    if not validate_file_name(file_name):
        return None
    
    file_name = file_name.split("_")[2]
    
    return file_name[0:file_name.find(".pdf")].strip()

def create_temp_folder(temp_path, today_date):
    """Create temp folder"""
    temp_path = os.path.normpath(temp_path)
    today_date = os.path.normpath(today_date)

    if not os.path.exists(temp_path):
        os.mkdir(temp_path)

    if not os.path.exists(f"""{temp_path}/{today_date}"""):
        os.mkdir(f"""{temp_path}/{today_date}""")

def copy_file_to_temp_folder(file_name, temp_folder):
    """Copy file to temp folder"""

    shutil.copyfile(os.path.normpath(file_name), os.path.normpath(temp_folder))

def open_folder(input, folder_type="source"):
    """Open folder"""
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        FOLDERS[folder_type] = folder_selected
        input.configure(text=folder_selected)

def create_main_temp_folder(source_folder):
    """Delete temp folder"""
    temp_folder = f"""{source_folder}/temp"""
    if os.path.exists(os.path.normpath(temp_folder)):
        shutil.rmtree(os.path.normpath(temp_folder))

    os.mkdir(os.path.normpath(temp_folder))

    return temp_folder

def preview(btn_move, tree):
    tree.delete(*tree.get_children())
    main_tree = dict()
    files = get_source_files(FOLDERS["source"])
    today_date = datetime.now().strftime("%Y-%m-%d")
    tree.heading('#0', text=f"""{today_date}""", anchor=tk.W)
    
    temp_folder = create_main_temp_folder(FOLDERS["source"])

    id = 0
    for file in files:
        lab_name = get_lab_name(file)
        temp_path = f"""{temp_folder}/{lab_name}"""
        create_temp_folder(temp_path, today_date)
        copy_file_to_temp_folder(f"""{FOLDERS["source"]}/{file}""", f"""{temp_path}/{today_date}/{file}""")
      
        if lab_name not in main_tree:
            main_tree[lab_name] = {
                "id": id,
                "files": []
            }
            tree.insert("", "end", text=lab_name, iid=id)
            id += 1

        main_tree[lab_name]["files"].append(file)
        tree.insert("", "end", text=file, iid=id)
        tree.move(id, main_tree[lab_name]["id"], len(main_tree[lab_name]["files"]) - 1)
        id += 1

    for lab in main_tree:
        tree.item(main_tree[lab]["id"], text=f"""{lab} ({len(main_tree[lab]["files"])})""")

    btn_move.configure(state=tk.NORMAL)

def move(tree):
    files = get_source_files(FOLDERS["source"])
    today_date = datetime.now().strftime("%Y-%m-%d")
    tree.heading('#0', text=f"""{today_date}""", anchor=tk.W)
    
    dest_folder = FOLDERS["dest"]

    id = 0
    for file in files:
        time.sleep(1)
        lab_name = get_lab_name(file)
        dest_path = f"""{dest_folder}/{lab_name}"""
        create_temp_folder(dest_path, today_date)
        copy_file_to_temp_folder(f"""{FOLDERS["source"]}/{file}""", f"""{dest_path}/{today_date}/{file}""")
        id += 1
    tk.messagebox.showinfo("Move labs", "Move labs completed")

def main():
    window = tk.Tk()
    window.title("Move labs")

    tree = ttk.Treeview(window)
    yscrollbar = ttk.Scrollbar(window, orient ="vertical", command = tree.yview)
    tree.configure(yscrollcommand=yscrollbar.set)

    frm_buttons = tk.Frame(window, relief=tk.RAISED, bd=2)
    btn_move = tk.Button(frm_buttons, text="Move", fg="green", state=tk.DISABLED, command=lambda: move(tree))
    btn_preview = tk.Button(frm_buttons, text="Preview", command=lambda: preview(btn_move, tree))

    frm_input = tk.Frame(window, relief=tk.RAISED, bd=2)
    label_source = tk.Label(frm_input, text="Source folder")
    input_source = tk.Label(frm_input, height=1, text=FOLDERS["source"])
    btn_source = tk.Button(frm_input, text="...", command=lambda: open_folder(input_source, "source"))

    label_dest = tk.Label(frm_input, text="Dest folder")
    input_dest = tk.Label(frm_input, height=1, text=FOLDERS["dest"])
    btn_dest = tk.Button(frm_input, text="...", command=lambda: open_folder(input_dest, "dest"))

    btn_preview.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    btn_move.grid(row=1, column=0, sticky="nsew", padx=5)

    frm_buttons.grid(row=0, column=0, sticky="nsew")
    frm_input.grid(row=0, column=1, sticky="nsew")
    
    label_source.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
    input_source.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
    btn_source.grid(row=0, column=3, sticky="nsew", padx=5, pady=5)
    label_dest.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)
    input_dest.grid(row=2, column=2, sticky="nsew", padx=5, pady=5)
    btn_dest.grid(row=2, column=3, sticky="nsew", padx=5, pady=5)

    tree.grid(row=1, column=0, columnspan=2, sticky="nsew")
    yscrollbar.grid(row=1, column=1, sticky='nse')
    yscrollbar.configure(command=tree.yview)

    window.grid_columnconfigure(1, weight=1)
    window.grid_rowconfigure(1, weight=1)

    window.mainloop()

if __name__ == "__main__":
    main()
