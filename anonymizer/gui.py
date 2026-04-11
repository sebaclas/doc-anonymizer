import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from pathlib import Path

# Importar lógica del core
from anonymizer.detectors import detector
from anonymizer.matcher import EntityMatcher
from anonymizer import mapping as mapping_mod
from anonymizer.utils import extract_document, anonymize_document
from anonymizer.config import current_settings, SETTINGS_PATH

# Configuración de apariencia
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class AnonymizerGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Doc Anonymizer - Desktop Pro")
        self.geometry("700x550")

        # Estado interno
        self.doc_path = None
        self.xlsx_path = None
        self.matcher = EntityMatcher()

        self._setup_ui()

    def _setup_ui(self):
        # Header Frame para contener Titulo + Ayuda
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(pady=(20, 10), fill="x", padx=20)

        self.header = ctk.CTkLabel(self.header_frame, text="ANONYMIZER PRO", font=ctk.CTkFont(size=24, weight="bold"))
        self.header.pack(side="left")

        self.btn_help = ctk.CTkButton(self.header_frame, text="❓ Guía Rápida", 
                                      width=120, height=30,
                                      fg_color="#17a2b8", hover_color="#138496",
                                      command=self._show_help)
        self.btn_help.pack(side="right")

        self.btn_settings = ctk.CTkButton(self.header_frame, text="⚙️ Ajustes", 
                                          width=80, height=30,
                                          fg_color="#6c757d", hover_color="#5a6268",
                                          command=self._open_settings)
        self.btn_settings.pack(side="right", padx=10)

        self.subtitle = ctk.CTkLabel(self, text="Anonimización segura de Word y PDF", font=ctk.CTkFont(size=14))
        self.subtitle.pack(pady=(0, 20))

        # --- STEP 1: Document ---
        self.frame_step1 = ctk.CTkFrame(self)
        self.frame_step1.pack(padx=20, pady=10, fill="x")

        self.lbl_step1 = ctk.CTkLabel(self.frame_step1, text="PASO 1: Elegir Documento Original", font=ctk.CTkFont(weight="bold"))
        self.lbl_step1.pack(padx=10, pady=(5, 5))

        self.btn_doc = ctk.CTkButton(self.frame_step1, text="Seleccionar Archivo (Word o PDF)", command=self._select_doc)
        self.btn_doc.pack(pady=5)

        self.lbl_doc_path = ctk.CTkLabel(self.frame_step1, text="No se ha seleccionado archivo", text_color="gray")
        self.lbl_doc_path.pack(pady=5)

        # --- STEP 2: Mapping ---
        self.frame_step2 = ctk.CTkFrame(self)
        self.frame_step2.pack(padx=20, pady=10, fill="x")

        self.lbl_step2 = ctk.CTkLabel(self.frame_step2, text="PASO 2: Gestionar Mapeo de Entidades", font=ctk.CTkFont(weight="bold"))
        self.lbl_step2.pack(padx=10, pady=(5, 5))

        # Botones en grid
        self.btn_frame = ctk.CTkFrame(self.frame_step2, fg_color="transparent")
        self.btn_frame.pack(pady=5)

        self.btn_detect = ctk.CTkButton(self.btn_frame, text="Detectar y Generar Excel", 
                                        fg_color="#1072BA", hover_color="#0D5A94",
                                        command=self._run_detection)
        self.btn_detect.grid(row=0, column=0, padx=10)

        self.btn_load_xlsx = ctk.CTkButton(self.btn_frame, text="Cargar Excel Existente", 
                                          command=self._load_existing_xlsx)
        self.btn_load_xlsx.grid(row=0, column=1, padx=10)

        self.lbl_xlsx_path = ctk.CTkLabel(self.frame_step2, text="Mapeo no definido", text_color="gray")
        self.lbl_xlsx_path.pack(pady=5)

        self.btn_open_xlsx = ctk.CTkButton(self.frame_step2, text="Abrir Excel para Revisión", 
                                          state="disabled", fg_color="gray",
                                          command=self._open_excel)
        self.btn_open_xlsx.pack(pady=5)

        # --- STEP 4: Apply ---
        self.btn_apply = ctk.CTkButton(self, text="GENERAR DOCUMENTO ANONIMIZADO", 
                                      font=ctk.CTkFont(size=16, weight="bold"),
                                      fg_color="#28a745", hover_color="#218838",
                                      height=50,
                                      state="disabled",
                                      command=self._run_apply)
        self.btn_apply.pack(padx=20, pady=(20, 10), fill="x")

        # --- DATABASE MANAGEMENT ---
        self.frame_db = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_db.pack(padx=20, pady=5, fill="x")
        
        self.btn_manage_db = ctk.CTkButton(self.frame_db, text="⚙️ Abrir Base de Datos Maestra (Excel)", 
                                           fg_color="#6c757d", hover_color="#5a6268",
                                           command=self._manage_db)
        self.btn_manage_db.pack(side="right")

        self.btn_regex_editor = ctk.CTkButton(self.frame_db, text="🔍 Editor de Regex", 
                                           fg_color="#6c757d", hover_color="#5a6268",
                                           command=self._open_regex_editor)
        self.btn_regex_editor.pack(side="right", padx=10)

        # Barra de progreso / Status
        self.status_bar = ctk.CTkLabel(self, text="Listo", anchor="w")
        self.status_bar.pack(side="bottom", fill="x", padx=10, pady=5)

    def _select_doc(self):
        filename = filedialog.askopenfilename(filetypes=[("Documentos Soportados", "*.docx *.pdf"), ("Word", "*.docx"), ("PDF", "*.pdf")])
        if filename:
            self.doc_path = Path(filename)
            self.lbl_doc_path.configure(text=self.doc_path.name, text_color="white")
            self._check_ready()

    def _load_existing_xlsx(self):
        filename = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
        if filename:
            self.xlsx_path = Path(filename)
            self.lbl_xlsx_path.configure(text=self.xlsx_path.name, text_color="white")
            self.btn_open_xlsx.configure(state="normal", fg_color="#F39C12", hover_color="#E67E22")
            self._check_ready()

    def _check_ready(self):
        if self.doc_path and self.xlsx_path:
            self.btn_apply.configure(state="normal")
        else:
            self.btn_apply.configure(state="disabled")

    def _open_excel(self):
        if self.xlsx_path and self.xlsx_path.exists():
            os.startfile(self.xlsx_path)

    def _run_detection(self):
        if not self.doc_path:
            messagebox.showwarning("Atención", "Primero debes seleccionar un documento.")
            return
        
        # Sugerir nombre de archivo de salida
        suggested = self.doc_path.parent / f"{self.doc_path.stem}_mapeo.xlsx"
        self.xlsx_path = Path(suggested)
        
        self.btn_detect.configure(state="disabled", text="Procesando...")
        self.status_bar.configure(text=f"Procesando {self.doc_path.suffix.upper()}...")
        
        threading.Thread(target=self._detection_thread, daemon=True).start()

    def _detection_thread(self):
        try:
            from anonymizer.known_entities import load
            from anonymizer.matcher import EntityMatcher

            # 1. Extraer (usa dispatcher)
            doc = extract_document(self.doc_path)
            
            # 2. Cargar DB fresca del Excel
            fresh_db = load()
            
            # 3. Detectar
            entities = detector.detect_all(doc, known_entities=fresh_db)
            
            # 4. Match con DB
            matcher = EntityMatcher()
            matcher.db = fresh_db
            
            rows = []
            seen = set()
            for ent in entities:
                ent_key = (ent.text, ent.entity_type)
                if ent_key in seen:
                    continue
                seen.add(ent_key)
                
                pseudo = matcher.match(ent.text, ent.entity_type)
                rows.append({
                    "original": ent.text,
                    "tipo": ent.entity_type.value,
                    "pseudonimo": pseudo or "",
                    "accion": "s" if pseudo else "",
                    "guardar_db": "", # Columna nueva explícita
                    "origen": "DB" if pseudo else "NER"
                })
            
            # 4. Guardar
            mapping_mod.save_extended_excel(rows, self.xlsx_path)
            
            # Actualizar UI en main thread
            self.after(0, self._detection_success)
            
        except Exception as e:
            error_str = str(e)
            self.after(0, lambda: self._process_error(f"Error en detección: {error_str}"))

    def _detection_success(self):
        self.btn_detect.configure(state="normal", text="Detectar y Generar Excel")
        self.lbl_xlsx_path.configure(text=self.xlsx_path.name, text_color="white")
        self.btn_open_xlsx.configure(state="normal", fg_color="#F39C12", hover_color="#E67E22")
        self.status_bar.configure(text=f"Excel generado: {self.xlsx_path.name}")
        self._check_ready()
        
        if messagebox.askyesno("Éxito", f"Detección completada.\nSe ha generado {self.xlsx_path.name}\n\n¿Quieres abrir el Excel ahora para revisarlo?"):
            self._open_excel()

    def _run_apply(self):
        if not (self.doc_path and self.xlsx_path):
            return
            
        output_file = self.doc_path.parent / f"{self.doc_path.stem}_anonimizado{self.doc_path.suffix}"
        
        self.btn_apply.configure(state="disabled", text="Generando Copia...")
        self.status_bar.configure(text="Aplicando anonimización y guardando...")
        
        threading.Thread(target=self._apply_thread, args=(output_file,), daemon=True).start()

    def _apply_thread(self, output_file):
        try:
            # Ahora cargamos los datos extendidos para saber qué guardar en DB
            full_data = mapping_mod.load_extended_data(self.xlsx_path)
            
            if not full_data:
                self.after(0, lambda: messagebox.showwarning("Vacio", "No se encontraron reemplazos con acción 's' en el Excel."))
                self.after(0, self._apply_finished)
                return

            # Construir mapeo y modos para el reemplazo en documento
            mapping = {d["original"]: d["pseudonimo"] for d in full_data}
            modes = {d["original"]: d.get("modo", "palabra") for d in full_data}

            # 1. Alimentar base de datos maestra si se solicitó
            from anonymizer import known_entities as ke
            db_added = 0
            for d in full_data:
                if d.get("save_db"):
                    ke.add(ke.KnownEntity(
                        original=d["original"],
                        pseudonym=d["pseudonimo"],
                        entity_type=d.get("tipo", "PERSONALIZADO"),
                        aliases=d.get("aliases", []),
                        match_mode=d.get("modo", "palabra")
                    ))
                    db_added += 1

            # 2. Ejecutar anonimización
            anonymize_document(self.doc_path, output_file, mapping, modes)
            
            # Actualizar UI
            msg = f"Documento guardado: {output_file.name}"
            if db_added > 0:
                msg += f"\nSe agregaron {db_added} entidades a la DB maestra."
                
            self.after(0, lambda m=msg: self._apply_success(output_file, m))
            
        except Exception as e:
            error_str = str(e)
            self.after(0, lambda: self._process_error(f"Error al anonimizar: {error_str}"))

    def _apply_success(self, output_file, message):
        self._apply_finished()
        self.status_bar.configure(text=message)
        if messagebox.askyesno("Completado", f"{message}\n\n¿Deseas abrir la carpeta contenedora?"):
            os.startfile(output_file.parent)

    def _apply_finished(self):
        self.btn_apply.configure(state="normal", text="GENERAR DOCUMENTO ANONIMIZADO")

    def _process_error(self, msg):
        self.btn_detect.configure(state="normal", text="Detectar y Generar Excel")
        self.btn_apply.configure(state="normal", text="GENERAR DOCUMENTO ANONIMIZADO")
        self.status_bar.configure(text="Error detectado.")
        messagebox.showerror("Error", msg)

    def _manage_db(self):
        """Abre la base de datos maestra en Excel directamente."""
        try:
            from anonymizer import known_entities as ke
            db_path = Path(current_settings.db_path)
            
            # Aseguramos que el archivo exista antes de abrirlo
            if not db_path.exists():
                ke.save([]) # Crea archivo vacío con cabeceras
                
            self.status_bar.configure(text=f"Abriendo base de datos maestra: {db_path.name}")
            os.startfile(db_path)
            
            messagebox.showinfo("Base de Datos Maestra", 
                                "Se ha abierto el Excel de la Base de Datos Maestra.\n\n"
                                "Los cambios que guardes en Excel se aplicarán automáticamente "
                                "la próxima vez que inicies un proceso de detección.\n\n"
                                "Nota: Si borras filas en el Excel, dejarán de detectarse.")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir la DB: {str(e)}")

    def _open_regex_editor(self):
        try:
            from anonymizer.regex_editor import RegexEditorWindow
            editor = RegexEditorWindow(self)
            editor.focus()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el editor de regex: {str(e)}")

    def _open_settings(self):
        """Abre el archivo settings.json para edición manual."""
        if SETTINGS_PATH.exists():
            os.startfile(SETTINGS_PATH)
        else:
            messagebox.showerror("Error", "No se encontró el archivo de ajustes.")

    def _show_help(self):
        # 1. Buscar en todas las ubicaciones posibles (ahora en HTML)
        paths_to_check = [
            Path(__file__).resolve().parent.parent / "mini_manual.html",
            Path(__file__).resolve().parent / "mini_manual.html",
            Path.cwd() / "mini_manual.html"
        ]
        
        found_file = None
        for p in paths_to_check:
            if p.exists():
                found_file = p
                break
        
        if found_file:
            try:
                # El HTML se abre siempre perfecto en el navegador
                os.startfile(str(found_file))
                self.status_bar.configure(text=f"Abriendo ayuda: {found_file.name}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir el manual HTML:\n{str(e)}")
        else:
            messagebox.showerror("Archivo No Encontrado", "No se pudo encontrar 'mini_manual.html'.")

if __name__ == "__main__":
    app = AnonymizerGUI()
    app.mainloop()
