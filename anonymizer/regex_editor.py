import tkinter as tk
import customtkinter as ctk
import re
import logging
from typing import List, Dict, Optional
from anonymizer.models import EntityType
from anonymizer.config import load_custom_patterns, save_custom_patterns

logger = logging.getLogger(__name__)

class RegexEditorWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Editor de Patrones Regex")
        self.geometry("900x700")
        self.after(100, self._bring_to_front)
        
        # Load patterns
        self.all_patterns = load_custom_patterns()
        self.selected_index = -1
        
        # Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=3) # List
        self.grid_rowconfigure(2, weight=2) # Edition/Test
        
        # Header
        self.header = ctk.CTkLabel(self, text="Gestión de Patrones Regex", font=ctk.CTkFont(size=20, weight="bold"))
        self.header.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        
        # List Section
        self.list_frame = ctk.CTkScrollableFrame(self, label_text="LISTA DE PATRONES ACTIVOS")
        self.list_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        
        # Edition / Test Section
        self.edit_frame = ctk.CTkFrame(self)
        self.edit_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        self.setup_edit_ui()
        
        # Initial Render
        self.refresh_list()

    def _bring_to_front(self):
        self.lift()
        self.focus_force()

    def setup_edit_ui(self):
        self.edit_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(self.edit_frame, text="EDICIÓN Y PRUEBA", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=2, pady=5)
        
        # Name
        ctk.CTkLabel(self.edit_frame, text="Nombre:").grid(row=1, column=0, padx=10, sticky="e")
        self.name_entry = ctk.CTkEntry(self.edit_frame)
        self.name_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        
        # Type
        ctk.CTkLabel(self.edit_frame, text="Tipo:").grid(row=2, column=0, padx=10, sticky="e")
        self.type_var = tk.StringVar(value=EntityType.CUSTOM.value)
        self.type_menu = ctk.CTkOptionMenu(self.edit_frame, values=[t.value for t in EntityType], variable=self.type_var)
        self.type_menu.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        
        # Pattern
        ctk.CTkLabel(self.edit_frame, text="Regex:").grid(row=3, column=0, padx=10, sticky="e")
        self.pattern_entry = ctk.CTkEntry(self.edit_frame, font=("Courier", 12))
        self.pattern_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        
        # Test Text
        ctk.CTkLabel(self.edit_frame, text="Prueba:").grid(row=4, column=0, padx=10, sticky="ne")
        self.test_text = ctk.CTkTextbox(self.edit_frame, height=80)
        self.test_text.grid(row=4, column=1, padx=10, pady=5, sticky="ew")
        
        # Buttons
        btn_frame = ctk.CTkFrame(self.edit_frame, fg_color="transparent")
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        self.save_btn = ctk.CTkButton(btn_frame, text="💾 Guardar Cambios", command=self.save_current)
        self.save_btn.pack(side="left", padx=5)
        
        self.test_btn = ctk.CTkButton(btn_frame, text="🔍 Probar", command=self.run_test)
        self.test_btn.pack(side="left", padx=5)
        
        self.new_btn = ctk.CTkButton(btn_frame, text="➕ Nuevo Patrón", command=self.clear_edit, fg_color="#2ecc71", hover_color="#27ae60")
        self.new_btn.pack(side="left", padx=5)
        
        self.restore_btn = ctk.CTkButton(btn_frame, text="🔄 Restaurar Defaults", command=self.restore_defaults, fg_color="#9b59b6", hover_color="#8e44ad")
        self.restore_btn.pack(side="left", padx=5)

        # Status Label
        self.status_label = ctk.CTkLabel(self.edit_frame, text="", font=ctk.CTkFont(size=12))
        self.status_label.grid(row=6, column=0, columnspan=2, pady=5)

    def refresh_list(self):
        # Clear frame
        for widget in self.list_frame.winfo_children():
            widget.destroy()
            
        for i, p in enumerate(self.all_patterns):
            row = ctk.CTkFrame(self.list_frame)
            row.pack(fill="x", padx=5, pady=2)
            
            # Switch
            enabled_var = tk.BooleanVar(value=p.get("enabled", True))
            cb = ctk.CTkSwitch(row, text="", variable=enabled_var, width=40, 
                               command=lambda i=i, v=enabled_var: self.toggle_pattern(i, v.get()))
            cb.pack(side="left", padx=5)
            
            # Info
            name_label = ctk.CTkLabel(row, text=f"{p['name']} ({p['type']})", width=200, anchor="w")
            name_label.pack(side="left", padx=5)
            
            pattern_text = p['pattern'][:50] + "..." if len(p['pattern']) > 50 else p['pattern']
            pattern_label = ctk.CTkLabel(row, text=pattern_text, font=("Courier", 11), text_color="gray")
            pattern_label.pack(side="left", padx=10, expand=True, fill="x")
            
            # Buttons
            edit_btn = ctk.CTkButton(row, text="✏️", width=30, command=lambda i=i: self.load_for_edit(i))
            edit_btn.pack(side="left", padx=2)
            
            del_btn = ctk.CTkButton(row, text="🗑️", width=30, fg_color="#e74c3c", hover_color="#c0392b",
                                    command=lambda i=i: self.confirm_delete(i))
            del_btn.pack(side="left", padx=2)

    def toggle_pattern(self, index, value):
        self.all_patterns[index]["enabled"] = value
        save_custom_patterns(self.all_patterns)

    def load_for_edit(self, index):
        self.selected_index = index
        p = self.all_patterns[index]
        self.name_entry.delete(0, "end")
        self.name_entry.insert(0, p["name"])
        self.type_var.set(p["type"])
        self.pattern_entry.delete(0, "end")
        self.pattern_entry.insert(0, p["pattern"])
        self.status_label.configure(text="", text_color="white")

    def clear_edit(self):
        self.selected_index = -1
        self.name_entry.delete(0, "end")
        self.pattern_entry.delete(0, "end")
        self.type_var.set(EntityType.CUSTOM.value)
        self.status_label.configure(text="", text_color="white")

    def save_current(self):
        name = self.name_entry.get().strip()
        pattern = self.pattern_entry.get().strip()
        
        if not name or not pattern:
            self.status_label.configure(text="Error: Nombre y Patrón son obligatorios", text_color="#e74c3c")
            return
            
        try:
            re.compile(pattern)
        except Exception as e:
            self.status_label.configure(text=f"Error en Regex: {e}", text_color="#e74c3c")
            return

        import time
        new_p = {
            "id": self.all_patterns[self.selected_index]["id"] if self.selected_index != -1 else f"user_{int(time.time())}",
            "name": name,
            "type": self.type_var.get(),
            "pattern": pattern,
            "enabled": True,
            "builtin": False if self.selected_index == -1 else self.all_patterns[self.selected_index].get("builtin", False)
        }
        
        if self.selected_index == -1:
            self.all_patterns.append(new_p)
        else:
            self.all_patterns[self.selected_index] = new_p
            
        save_custom_patterns(self.all_patterns)
        self.refresh_list()
        self.status_label.configure(text="✅ Guardado correctamente", text_color="#2ecc71")

    def run_test(self):
        pat = self.pattern_entry.get()
        text = self.test_text.get("1.0", "end-1c")
        
        # Clear tags
        self.test_text.tag_delete("highlight")
        
        if not pat:
            self.status_label.configure(text="Ingrese un patrón para probar", text_color="#e74c3c")
            return

        try:
            regex = re.compile(pat)
            matches = list(regex.finditer(text))
            
            # Highlight matches
            self.test_text.tag_config("highlight", background="#f1c40f", foreground="black")
            for m in matches:
                start_idx = f"1.0 + {m.start()} chars"
                end_idx = f"1.0 + {m.end()} chars"
                self.test_text.tag_add("highlight", start_idx, end_idx)
            
            self.status_label.configure(text=f"🔍 Encontrados {len(matches)} matches", text_color="#3498db")
        except Exception as e:
            self.status_label.configure(text=f"❌ Regex Inválida: {e}", text_color="#e74c3c")

    def confirm_delete(self, index):
        # Simplest delete for now
        self.all_patterns.pop(index)
        save_custom_patterns(self.all_patterns)
        self.refresh_list()

    def restore_defaults(self):
        from tkinter import messagebox
        if messagebox.askyesno("Confirmar", "¿Estás seguro de que quieres restaurar los patrones por defecto?\nEsto inyectará los patrones de fábrica faltantes."):
            from anonymizer.config import create_default_config
            self.all_patterns = create_default_config()
            self.refresh_list()
            self.status_label.configure(text="✅ Patrones restaurados", text_color="#2ecc71")
