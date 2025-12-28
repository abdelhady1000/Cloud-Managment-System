import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
from vm_manager import create_vm_logic
from docker_manager import *
from config_manager import load_vm_config, set_iso_path

class CloudManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cloud Management System")
        self.root.geometry("950x750")
        self.root.configure(bg="#2c3e50")

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TNotebook", background="#2c3e50", borderwidth=0)
        self.style.configure("TNotebook.Tab", background="#34495e", foreground="white", padding=[10, 5])
        self.style.map("TNotebook.Tab", background=[("selected", "#3498db")])
        self.style.configure("Action.TButton", background="#27ae60", foreground="white", font=('Helvetica', 10, 'bold'))
        self.style.configure("Danger.TButton", background="#c0392b", foreground="white", font=('Helvetica', 10, 'bold'))

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        self.setup_vm_tab()
        self.setup_docker_image_tab()
        self.setup_container_tab()
        self.setup_build_tab()

    def setup_vm_tab(self):
        vm_frame = tk.Frame(self.notebook, bg="#ecf0f1")
        self.notebook.add(vm_frame, text=" VM Management ")
        tk.Label(vm_frame, text="Configuration Settings", font=("Helvetica", 14, "bold"), bg="#ecf0f1", fg="#000000").grid(row=0, column=0, columnspan=2, pady=20)
        
        labels = ["VM Name:", "CPU Cores:", "Memory (MB):", "Disk (GB):"]
        self.vm_entries = []
        for i, text in enumerate(labels):
            tk.Label(vm_frame, text=text, bg="#ecf0f1", fg="#000000", font=("Helvetica", 10, "bold")).grid(row=i+1, column=0, padx=20, pady=10, sticky="e")
            entry = ttk.Entry(vm_frame, width=35)
            entry.grid(row=i+1, column=1, padx=20, pady=10, sticky="w")
            self.vm_entries.append(entry)
        
        btn_frame = tk.Frame(vm_frame, bg="#ecf0f1")
        btn_frame.grid(row=5, column=0, columnspan=2, pady=25, sticky="w", padx=20)
        ttk.Button(btn_frame, text="Select ISO File", style="Action.TButton", command=self.select_iso).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Load Config File", style="Action.TButton", command=self.load_config_handler).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Launch Virtual Machine", style="Action.TButton", command=self.create_vm_handler).pack(side="left", padx=10)



    def select_iso(self):
        path = filedialog.askopenfilename(title="Select Ubuntu ISO", filetypes=[("ISO files", "*.iso")])
        if path:
            set_iso_path(path)
            messagebox.showinfo("ISO Selected", f"ISO Path set to: {path}")

    def setup_docker_image_tab(self):
        img_frame = tk.Frame(self.notebook, bg="#ecf0f1")
        self.notebook.add(img_frame, text=" Image Search ")
        tk.Label(img_frame, text="Search Docker Images", font=("Helvetica", 12, "bold"), bg="#ecf0f1", fg="#000000").pack(pady=10)
        self.search_entry = ttk.Entry(img_frame, width=50)
        self.search_entry.pack(pady=5)
        
        btn_box = tk.Frame(img_frame, bg="#ecf0f1")
        btn_box.pack(pady=5)
        ttk.Button(btn_box, text="Local Search", command=self.ui_search_local).pack(side="left", padx=5)
        ttk.Button(btn_box, text="Hub Search", command=self.ui_search_hub).pack(side="left", padx=5)

        self.img_display = scrolledtext.ScrolledText(img_frame, height=18, bg="#1e1e1e", fg="#ffffff")
        self.img_display.pack(padx=20, pady=10, fill="both", expand=True)
        ttk.Button(img_frame, text="List All Images", style="Action.TButton", command=self.ui_list_images).pack(pady=10)

    def setup_container_tab(self):
        cont_frame = tk.Frame(self.notebook, bg="#ecf0f1")
        self.notebook.add(cont_frame, text=" Live Containers ")
        self.cont_display = scrolledtext.ScrolledText(cont_frame, height=18, bg="#1e1e1e", fg="#2ecc71")
        self.cont_display.pack(padx=20, pady=10, fill="both", expand=True)
        ttk.Button(cont_frame, text="Refresh Containers", style="Action.TButton", command=self.ui_list_containers).pack(pady=5)
        
        stop_box = tk.LabelFrame(cont_frame, text=" Stop Container ", bg="#ecf0f1", fg="#000000", font=("Helvetica", 10, "bold"), padx=10, pady=10)
        stop_box.pack(padx=20, pady=10, fill="x")
        tk.Label(stop_box, text="ID/Name:", bg="#ecf0f1", fg="#000000").pack(side="left", padx=5)
        self.stop_entry = ttk.Entry(stop_box)
        self.stop_entry.pack(side="left", padx=5, expand=True, fill="x")
        ttk.Button(stop_box, text="Stop", style="Danger.TButton", command=self.ui_stop_container).pack(side="left", padx=5)

    def setup_build_tab(self):
        build_frame = tk.Frame(self.notebook, bg="#ecf0f1")
        self.notebook.add(build_frame, text=" Build Tools ")

        create_box = tk.LabelFrame(build_frame, text=" Dockerfile Creator ", bg="#ecf0f1", fg="#000000", font=("Helvetica", 10, "bold"), padx=10, pady=10)
        create_box.pack(padx=20, pady=10, fill="both", expand=True)
        
        tk.Label(create_box, text="Save Folder Path:", bg="#ecf0f1", fg="#000000").pack(anchor="w")
        self.df_path_entry = ttk.Entry(create_box)
        self.df_path_entry.pack(fill="x", pady=2)
        
        tk.Label(create_box, text="Dockerfile Content:", bg="#ecf0f1", fg="#000000").pack(anchor="w")
        self.df_editor = scrolledtext.ScrolledText(create_box, height=8)
        self.df_editor.pack(fill="both", expand=True, pady=2)
        ttk.Button(create_box, text="Save Dockerfile", style="Action.TButton", command=self.ui_save_df).pack(pady=5)

        builder_box = tk.LabelFrame(build_frame, text=" Image Builder ", bg="#ecf0f1", fg="#000000", font=("Helvetica", 10, "bold"), padx=10, pady=10)
        builder_box.pack(padx=20, pady=10, fill="x")
        
        grid_f = tk.Frame(builder_box, bg="#ecf0f1")
        grid_f.pack(fill="x")
        tk.Label(grid_f, text="Dockerfile Full Path:", bg="#ecf0f1", fg="#000000").grid(row=0, column=0, sticky="e")
        self.build_path_entry = ttk.Entry(grid_f)
        self.build_path_entry.grid(row=0, column=1, sticky="we", padx=5)
        tk.Label(grid_f, text="Image Name:", bg="#ecf0f1", fg="#000000").grid(row=1, column=0, sticky="e")
        self.build_name_entry = ttk.Entry(grid_f)
        self.build_name_entry.grid(row=1, column=1, sticky="we", padx=5)
        tk.Label(grid_f, text="Tag:", bg="#ecf0f1", fg="#000000").grid(row=1, column=2, sticky="e")
        self.build_tag_entry = ttk.Entry(grid_f)
        self.build_tag_entry.grid(row=1, column=3, sticky="we", padx=5)
        grid_f.columnconfigure(1, weight=3)
        
        ttk.Button(builder_box, text="Start Build", style="Action.TButton", command=self.ui_build_image).pack(pady=10)

    def create_vm_handler(self):
        try:
            name = self.vm_entries[0].get().strip()
            cpu = int(self.vm_entries[1].get())
            mem = int(self.vm_entries[2].get())
            disk = int(self.vm_entries[3].get())

            # Input sanitization
            if not name:
                messagebox.showerror("Error", "VM name cannot be empty")
                return
            if any(c in r'\/:*?"<>|' for c in name):
                messagebox.showerror("Error", "VM name contains invalid characters")
                return
            if cpu <= 0 or mem <= 0 or disk <= 0:
                messagebox.showerror("Error", "CPU, memory, and disk must be positive numbers")
                return

            res = create_vm_logic(name, cpu, mem, disk)
            messagebox.showinfo("Result", res)
        except ValueError:
            messagebox.showerror("Error", "CPU, memory, and disk must be integers")
    def load_config_handler(self):
        path = filedialog.askopenfilename(title="Select VM Config File", filetypes=[("JSON files", "*.json")])
        if not path:
            return

        res = load_vm_config(path)

        if res[0] is None:
            messagebox.showerror("Config Error", res[1])
            return

        name, cpu, memory, disk = res

        # Fill form automatically
        self.vm_entries[0].delete(0, tk.END)
        self.vm_entries[0].insert(0, name)

        self.vm_entries[1].delete(0, tk.END)
        self.vm_entries[1].insert(0, cpu)

        self.vm_entries[2].delete(0, tk.END)
        self.vm_entries[2].insert(0, memory)

        self.vm_entries[3].delete(0, tk.END)
        self.vm_entries[3].insert(0, disk)

        messagebox.showinfo("Config Loaded", "VM configuration loaded successfully")

    def ui_save_df(self):
        res = save_dockerfile(self.df_path_entry.get(), self.df_editor.get(1.0, tk.END))
        messagebox.showinfo("File System", res)

    def ui_build_image(self):
        res = build_image(self.build_path_entry.get(), self.build_name_entry.get().strip().replace(" ", "_").lower(),self.build_tag_entry.get().strip())
        self.img_display.delete(1.0, tk.END)
        self.img_display.insert(tk.END, res)
        self.notebook.select(1) # Switch to Image Search tab to see output

    def ui_list_images(self):
        self.img_display.delete(1.0, tk.END)
        self.img_display.insert(tk.END, docker_image_list())

    def ui_search_local(self):
        self.img_display.delete(1.0, tk.END)
        self.img_display.insert(tk.END, search_local(self.search_entry.get()))

    def ui_search_hub(self):
        self.img_display.delete(1.0, tk.END)
        self.img_display.insert(tk.END, search_hub(self.search_entry.get()))

    def ui_list_containers(self):
        self.cont_display.delete(1.0, tk.END)
        self.cont_display.insert(tk.END, docker_container_list())

    def ui_stop_container(self):
        res = docker_stop_container(self.stop_entry.get())
        messagebox.showinfo("Docker", res)
        self.ui_list_containers()
