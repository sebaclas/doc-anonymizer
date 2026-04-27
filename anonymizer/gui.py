"""
ANON V — Desktop Pro
Rediseño de la GUI con stepper horizontal, wallpaper de fondo y branding INVAP.
Implementación CustomTkinter — preserva toda la lógica de la versión anterior.
"""

import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import sys
import customtkinter as ctk
from pathlib import Path

# Importar lógica del core (sin cambios)
from anonymizer.detectors import detector
from anonymizer.matcher import EntityMatcher
from anonymizer import mapping as mapping_mod
from anonymizer.utils import extract_document, anonymize_document
from anonymizer.config import current_settings, SETTINGS_PATH


# ============================================================
# PALETA Y CONSTANTES VISUALES
# ============================================================
COLOR_BG          = "#111827"   # fondo base
COLOR_PANEL       = "#18181C"   # frames principales
COLOR_PANEL_ALT   = "#1F1F25"   # tarjetas internas
COLOR_BORDER      = "#2A2A32"
COLOR_BORDER_SOFT = "#22222A"
COLOR_TEXT        = "#ECECF0"
COLOR_TEXT_DIM    = "#9A9AA5"
COLOR_TEXT_MUTED  = "#60606B"
COLOR_ACCENT      = "#4FB3FF"   # azul técnico
COLOR_ACCENT_DARK = "#2E8FD9"
COLOR_SUCCESS     = "#3DBE8B"
COLOR_SUCCESS_DARK = "#2D9B6E"
COLOR_WARNING     = "#E6B04A"
COLOR_DANGER      = "#D66A6A"

WIN_W = 1050
WIN_H = 720


def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    full_path = os.path.join(base_path, relative_path)
    if not os.path.exists(full_path):
        asset_fallback = os.path.join(base_path, "docs", "assets", relative_path)
        if os.path.exists(asset_fallback):
            return asset_fallback

    return full_path


# Configuración de apariencia
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class AnonymizerGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ANON V — Desktop Pro")
        self.geometry(f"{WIN_W}x{WIN_H}")
        self.minsize(WIN_W, WIN_H)
        self.configure(fg_color=COLOR_BG)

        # Estado interno
        self.doc_path = None
        self.xlsx_path = None
        self.matcher = EntityMatcher()
        self.active_step = 1  # paso activo del stepper

        self._setup_ui()
        self._render_step_content()

        # Cargar archivo si se pasa como argumento
        if len(sys.argv) > 1:
            self._handle_command_line_args(sys.argv[1])

    # ============================================================
    # UI SETUP
    # ============================================================
    def _setup_ui(self):
        # Contenedor principal
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.place(x=0, y=0, relwidth=1, relheight=1)

        # ---------- HEADER ----------
        self.header_frame = ctk.CTkFrame(self.main_container, fg_color="transparent", height=60)
        self.header_frame.pack(fill="x", padx=28, pady=(22, 0))
        self.header_frame.pack_propagate(False)

        # Wordmark ANON V (texto + glifo simple)
        self.brand_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.brand_frame.pack(side="left")

        # Glifo geométrico simple usando un Canvas
        self.brand_canvas = tk.Canvas(self.brand_frame, width=42, height=30,
                                      bg=COLOR_BG, highlightthickness=0, bd=0)
        # No podemos hacer transparente el canvas; lo evitamos y solo usamos texto.
        self.brand_canvas.destroy()

        self.brand_label = ctk.CTkLabel(
            self.brand_frame,
            text="▌▍▌▎  ANON V",
            font=ctk.CTkFont(family="Consolas", size=20, weight="bold"),
            text_color=COLOR_TEXT,
        )
        self.brand_label.pack(side="left", pady=10)

        # Botones header (derecha)
        self.btn_help = ctk.CTkButton(
            self.header_frame, text="?  Ayuda", width=90, height=30,
            fg_color="transparent", hover_color=COLOR_PANEL_ALT,
            text_color=COLOR_TEXT_DIM, border_width=1, border_color=COLOR_BORDER,
            font=ctk.CTkFont(size=12),
            command=self._show_help,
        )
        self.btn_help.pack(side="right", padx=(8, 0), pady=15)

        self.btn_settings = ctk.CTkButton(
            self.header_frame, text="⚙  Ajustes", width=90, height=30,
            fg_color="transparent", hover_color=COLOR_PANEL_ALT,
            text_color=COLOR_TEXT_DIM, border_width=1, border_color=COLOR_BORDER,
            font=ctk.CTkFont(size=12),
            command=self._open_settings,
        )
        self.btn_settings.pack(side="right", pady=15)

        # ---------- STEPPER ----------
        self.stepper_frame = ctk.CTkFrame(self.main_container, fg_color="transparent", height=70)
        self.stepper_frame.pack(fill="x", padx=28, pady=(18, 0))
        self.stepper_frame.pack_propagate(False)

        self.step_widgets = []  # se llena en _render_stepper
        self._render_stepper()

        # ---------- PANEL DEL PASO ACTIVO ----------
        self.step_panel = ctk.CTkFrame(
            self.main_container,
            fg_color=COLOR_PANEL,
            border_width=1, border_color=COLOR_BORDER_SOFT,
            corner_radius=10,
        )
        self.step_panel.pack(fill="both", expand=True, padx=28, pady=(20, 12))

        # ---------- BARRA INFERIOR (utilidades) ----------
        self.bottom_bar = ctk.CTkFrame(
            self.main_container,
            fg_color=("#0A0A0C", "#0A0A0C"),
            border_width=0, corner_radius=0, height=44,
        )
        self.bottom_bar.pack(fill="x", side="bottom")
        self.bottom_bar.pack_propagate(False)

        # Línea superior de la barra
        self.bottom_sep = ctk.CTkFrame(self.bottom_bar, fg_color=COLOR_BORDER, height=1)
        self.bottom_sep.pack(fill="x", side="top")

        # Acciones secundarias (izquierda)
        self.bottom_left = ctk.CTkFrame(self.bottom_bar, fg_color="transparent")
        self.bottom_left.pack(side="left", padx=24, pady=8)

        self.btn_revert = ctk.CTkButton(
            self.bottom_left, text="↩  Revertir", width=100, height=28,
            fg_color="transparent", hover_color=COLOR_PANEL_ALT,
            text_color=COLOR_TEXT_DIM,
            font=ctk.CTkFont(size=11),
            command=self._run_deanonymize,
        )
        self.btn_revert.pack(side="left", padx=(0, 4))

        self.btn_regex_editor = ctk.CTkButton(
            self.bottom_left, text="⌕  Editor Regex", width=110, height=28,
            fg_color="transparent", hover_color=COLOR_PANEL_ALT,
            text_color=COLOR_TEXT_DIM,
            font=ctk.CTkFont(size=11),
            command=self._open_regex_editor,
        )
        self.btn_regex_editor.pack(side="left", padx=4)

        self.btn_manage_db = ctk.CTkButton(
            self.bottom_left, text="⛁  Base de datos", width=120, height=28,
            fg_color="transparent", hover_color=COLOR_PANEL_ALT,
            text_color=COLOR_TEXT_DIM,
            font=ctk.CTkFont(size=11),
            command=self._manage_db,
        )
        self.btn_manage_db.pack(side="left", padx=4)

        # Status + INVAP (derecha)
        self.bottom_right = ctk.CTkFrame(self.bottom_bar, fg_color="transparent")
        self.bottom_right.pack(side="right", padx=24, pady=8)

        self.status_bar = ctk.CTkLabel(
            self.bottom_right, text="●  listo",
            font=ctk.CTkFont(family="Consolas", size=11),
            text_color=COLOR_SUCCESS,
        )
        self.status_bar.pack(side="right")

    # ============================================================
    # STEPPER (badges 1-2-3 con conector)
    # ============================================================
    def _render_stepper(self):
        for w in self.step_widgets:
            w.destroy()
        self.step_widgets = []

        steps = [
            (1, "DOCUMENTO", "elegir archivo"),
            (2, "MAPEO",     "detectar entidades"),
            (3, "GENERAR",   "aplicar anonimización"),
        ]

        for i, (n, label, sub) in enumerate(steps):
            state = "done" if n < self.active_step else ("active" if n == self.active_step else "pending")

            # Badge circular
            if state == "done":
                badge_bg, badge_fg, badge_border = COLOR_SUCCESS, "#06130D", COLOR_SUCCESS
                badge_text = "✓"
            elif state == "active":
                badge_bg, badge_fg, badge_border = COLOR_ACCENT, "#06121E", COLOR_ACCENT
                badge_text = str(n)
            else:
                badge_bg, badge_fg, badge_border = "transparent", COLOR_TEXT_DIM, COLOR_BORDER
                badge_text = str(n)

            badge_hover = COLOR_PANEL_ALT if badge_bg == "transparent" else badge_bg
            badge = ctk.CTkButton(
                self.stepper_frame, text=badge_text,
                width=32, height=32, corner_radius=16,
                fg_color=badge_bg, hover_color=badge_hover,
                text_color=badge_fg,
                border_width=1, border_color=badge_border,
                font=ctk.CTkFont(family="Consolas", size=13, weight="bold"),
                command=lambda step_n=n: self._goto_step(step_n),
            )
            badge.pack(side="left", padx=(0, 12), pady=18)
            self.step_widgets.append(badge)

            # Etiquetas
            lbl_frame = ctk.CTkFrame(self.stepper_frame, fg_color="transparent")
            lbl_frame.pack(side="left", padx=(0, 4), pady=12)
            self.step_widgets.append(lbl_frame)

            title_color = COLOR_TEXT_DIM if state == "pending" else COLOR_TEXT
            lbl_main = ctk.CTkLabel(
                lbl_frame, text=label,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=title_color,
                anchor="w",
            )
            lbl_main.pack(anchor="w")

            lbl_sub = ctk.CTkLabel(
                lbl_frame, text=sub,
                font=ctk.CTkFont(family="Consolas", size=10),
                text_color=COLOR_TEXT_MUTED,
                anchor="w",
            )
            lbl_sub.pack(anchor="w")

            # Conector (excepto último)
            if i < len(steps) - 1:
                connector_color = COLOR_SUCCESS if state == "done" else COLOR_BORDER
                connector = ctk.CTkFrame(
                    self.stepper_frame, fg_color=connector_color, height=1,
                )
                connector.pack(side="left", fill="x", expand=True, padx=18, pady=30)
                self.step_widgets.append(connector)

    def _goto_step(self, step_n):
        # Solo permitir avanzar a pasos accesibles
        if step_n == 1:
            pass  # siempre accesible
        elif step_n == 2 and not self.doc_path:
            return
        elif step_n == 3 and not (self.doc_path and self.xlsx_path):
            return

        self.active_step = step_n
        self._render_stepper()
        self._render_step_content()

    def _auto_advance(self):
        """Avanzar automáticamente al siguiente paso disponible."""
        if self.doc_path and self.xlsx_path:
            self.active_step = 3
        elif self.doc_path:
            self.active_step = 2
        else:
            self.active_step = 1
        self._render_stepper()
        self._render_step_content()

    # ============================================================
    # CONTENIDO POR PASO
    # ============================================================
    def _render_step_content(self):
        # Limpiar panel
        for child in self.step_panel.winfo_children():
            child.destroy()

        if self.active_step == 1:
            self._build_step1()
        elif self.active_step == 2:
            self._build_step2()
        else:
            self._build_step3()

    def _kicker(self, parent, text):
        return ctk.CTkLabel(
            parent, text=text,
            font=ctk.CTkFont(family="Consolas", size=10, weight="bold"),
            text_color=COLOR_ACCENT,
        )

    def _title(self, parent, text):
        return ctk.CTkLabel(
            parent, text=text,
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COLOR_TEXT,
        )

    def _subtitle(self, parent, text, wraplength=560):
        return ctk.CTkLabel(
            parent, text=text,
            font=ctk.CTkFont(size=13),
            text_color=COLOR_TEXT_DIM,
            wraplength=wraplength, justify="left",
        )

    # ----- PASO 1 -----
    def _build_step1(self):
        wrap = ctk.CTkFrame(self.step_panel, fg_color="transparent")
        wrap.pack(fill="both", expand=True, padx=30, pady=26)

        self._kicker(wrap, "PASO 01 — DOCUMENTO ORIGINAL").pack(anchor="w", pady=(0, 8))
        self._title(wrap, "Elegí el documento a anonimizar").pack(anchor="w", pady=(0, 6))
        self._subtitle(wrap,
            "Se aceptan documentos Word (.docx) y PDF. El archivo original no se modifica: "
            "siempre se genera una copia anonimizada en la misma carpeta."
        ).pack(anchor="w", pady=(0, 22))

        # Dropzone
        has_doc = self.doc_path is not None
        dropzone = ctk.CTkFrame(
            wrap,
            fg_color=COLOR_PANEL_ALT if has_doc else "#0F0F12",
            border_width=2, border_color=COLOR_ACCENT if has_doc else COLOR_BORDER,
            corner_radius=8,
        )
        dropzone.pack(fill="both", expand=True)

        if has_doc:
            ctk.CTkLabel(dropzone, text="📄", font=ctk.CTkFont(size=36),
                         text_color=COLOR_ACCENT).pack(pady=(28, 8))
            ctk.CTkLabel(dropzone, text=self.doc_path.name,
                         font=ctk.CTkFont(size=14, weight="bold"),
                         text_color=COLOR_TEXT).pack()
            try:
                size_kb = self.doc_path.stat().st_size // 1024
                size_str = f"{self.doc_path.suffix.lower().lstrip('.')} · {size_kb} kb · listo para detección"
            except Exception:
                size_str = self.doc_path.suffix.lower().lstrip(".")
            ctk.CTkLabel(dropzone, text=size_str,
                         font=ctk.CTkFont(family="Consolas", size=11),
                         text_color=COLOR_TEXT_MUTED).pack(pady=(4, 12))
            ctk.CTkButton(
                dropzone, text="Cambiar archivo",
                width=140, height=32,
                fg_color="transparent", hover_color=COLOR_PANEL,
                text_color=COLOR_TEXT, border_width=1, border_color=COLOR_BORDER,
                command=self._select_doc,
            ).pack(pady=(0, 26))
        else:
            ctk.CTkLabel(dropzone, text="⬆", font=ctk.CTkFont(size=40),
                         text_color=COLOR_TEXT_MUTED).pack(pady=(36, 10))
            ctk.CTkLabel(dropzone, text="Arrastrá un archivo aquí o usá el botón",
                         font=ctk.CTkFont(size=13),
                         text_color=COLOR_TEXT_DIM).pack()
            ctk.CTkLabel(dropzone, text="formatos soportados:  .docx   ·   .pdf",
                         font=ctk.CTkFont(family="Consolas", size=11),
                         text_color=COLOR_TEXT_MUTED).pack(pady=(6, 16))
            ctk.CTkButton(
                dropzone, text="Seleccionar archivo",
                width=180, height=38,
                fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_DARK,
                text_color="#06121E",
                font=ctk.CTkFont(size=13, weight="bold"),
                command=self._select_doc,
            ).pack(pady=(0, 36))

        # Footer del paso
        nav = ctk.CTkFrame(wrap, fg_color="transparent")
        nav.pack(fill="x", pady=(18, 0))

        ctk.CTkButton(
            nav, text="Continuar a Mapeo  →",
            width=180, height=38,
            fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_DARK,
            text_color="#06121E",
            font=ctk.CTkFont(size=13, weight="bold"),
            state="normal" if has_doc else "disabled",
            command=lambda: self._goto_step(2),
        ).pack(side="right")

    # ----- PASO 2 -----
    def _build_step2(self):
        wrap = ctk.CTkFrame(self.step_panel, fg_color="transparent")
        wrap.pack(fill="both", expand=True, padx=30, pady=26)

        self._kicker(wrap, "PASO 02 — MAPEO DE ENTIDADES").pack(anchor="w", pady=(0, 8))
        self._title(wrap, "Detectá o cargá el mapeo").pack(anchor="w", pady=(0, 6))
        self._subtitle(wrap,
            "ANON V buscará nombres, direcciones y otras entidades en el documento "
            "y generará un Excel editable con los pseudónimos sugeridos."
        ).pack(anchor="w", pady=(0, 22))

        # Dos tarjetas lado a lado
        cards = ctk.CTkFrame(wrap, fg_color="transparent")
        cards.pack(fill="x", pady=(0, 14))

        # Card 1 — recomendado
        card1 = ctk.CTkFrame(
            cards, fg_color=COLOR_PANEL_ALT,
            border_width=1, border_color=COLOR_ACCENT, corner_radius=8,
        )
        card1.pack(side="left", fill="both", expand=True, padx=(0, 7))

        c1 = ctk.CTkFrame(card1, fg_color="transparent")
        c1.pack(fill="both", expand=True, padx=20, pady=18)
        ctk.CTkLabel(c1, text="● RECOMENDADO",
                     font=ctk.CTkFont(family="Consolas", size=10, weight="bold"),
                     text_color=COLOR_ACCENT).pack(anchor="w", pady=(0, 6))
        ctk.CTkLabel(c1, text="Detección automática",
                     font=ctk.CTkFont(size=14, weight="bold"),
                     text_color=COLOR_TEXT).pack(anchor="w")
        ctk.CTkLabel(c1,
                     text="Analiza el documento y genera un Excel nuevo con\nentidades detectadas y pseudónimos sugeridos.",
                     font=ctk.CTkFont(size=11),
                     text_color=COLOR_TEXT_DIM, justify="left").pack(anchor="w", pady=(6, 14))
        self.btn_detect = ctk.CTkButton(
            c1, text="Detectar y generar Excel",
            height=32,
            fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_DARK,
            text_color="#06121E",
            font=ctk.CTkFont(size=12, weight="bold"),
            state="normal" if self.doc_path else "disabled",
            command=self._run_detection,
        )
        self.btn_detect.pack(anchor="w")

        # Card 2 — alternativa
        card2 = ctk.CTkFrame(
            cards, fg_color=COLOR_PANEL_ALT,
            border_width=1, border_color=COLOR_BORDER_SOFT, corner_radius=8,
        )
        card2.pack(side="left", fill="both", expand=True, padx=(7, 0))

        c2 = ctk.CTkFrame(card2, fg_color="transparent")
        c2.pack(fill="both", expand=True, padx=20, pady=18)
        ctk.CTkLabel(c2, text="ALTERNATIVA",
                     font=ctk.CTkFont(family="Consolas", size=10, weight="bold"),
                     text_color=COLOR_TEXT_DIM).pack(anchor="w", pady=(0, 6))
        ctk.CTkLabel(c2, text="Cargar Excel existente",
                     font=ctk.CTkFont(size=14, weight="bold"),
                     text_color=COLOR_TEXT).pack(anchor="w")
        ctk.CTkLabel(c2,
                     text="Reutilizá un mapeo generado previamente para\nmantener consistencia entre documentos.",
                     font=ctk.CTkFont(size=11),
                     text_color=COLOR_TEXT_DIM, justify="left").pack(anchor="w", pady=(6, 14))
        ctk.CTkButton(
            c2, text="Seleccionar Excel (.xlsx)",
            height=32,
            fg_color="transparent", hover_color=COLOR_PANEL,
            text_color=COLOR_TEXT,
            border_width=1, border_color=COLOR_BORDER,
            font=ctk.CTkFont(size=12),
            command=self._load_existing_xlsx,
        ).pack(anchor="w")

        # Estado
        if self.xlsx_path:
            status_frame = ctk.CTkFrame(
                wrap, fg_color="#0F1F18",
                border_width=1, border_color=COLOR_SUCCESS, corner_radius=4,
            )
            status_frame.pack(fill="x", pady=(8, 0))
            ctk.CTkLabel(
                status_frame,
                text=f"✓  mapeo cargado: {self.xlsx_path.name}",
                font=ctk.CTkFont(family="Consolas", size=11),
                text_color=COLOR_SUCCESS,
            ).pack(anchor="w", padx=14, pady=10)

            self.btn_open_xlsx = ctk.CTkButton(
                wrap, text="Abrir Excel para revisión",
                width=180, height=30,
                fg_color="transparent", hover_color=COLOR_PANEL,
                text_color=COLOR_TEXT, border_width=1, border_color=COLOR_BORDER,
                font=ctk.CTkFont(size=11),
                command=self._open_excel,
            )
            self.btn_open_xlsx.pack(anchor="w", pady=(8, 0))
        else:
            status_frame = ctk.CTkFrame(
                wrap, fg_color="#1A1612",
                border_width=1, border_color=COLOR_BORDER, corner_radius=4,
            )
            status_frame.pack(fill="x", pady=(8, 0))
            ctk.CTkLabel(
                status_frame,
                text="⚠  mapeo no definido — generá uno nuevo o cargá un Excel existente",
                font=ctk.CTkFont(family="Consolas", size=11),
                text_color=COLOR_WARNING,
            ).pack(anchor="w", padx=14, pady=10)

        # Footer del paso
        nav = ctk.CTkFrame(wrap, fg_color="transparent")
        nav.pack(fill="x", side="bottom", pady=(18, 0))

        ctk.CTkButton(
            nav, text="←  Volver",
            width=90, height=32,
            fg_color="transparent", hover_color=COLOR_PANEL_ALT,
            text_color=COLOR_TEXT_DIM,
            font=ctk.CTkFont(size=12),
            command=lambda: self._goto_step(1),
        ).pack(side="left")

        ctk.CTkButton(
            nav, text="Continuar a Generar  →",
            width=200, height=38,
            fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_DARK,
            text_color="#06121E",
            font=ctk.CTkFont(size=13, weight="bold"),
            state="normal" if (self.doc_path and self.xlsx_path) else "disabled",
            command=lambda: self._goto_step(3),
        ).pack(side="right")

    # ----- PASO 3 -----
    def _build_step3(self):
        wrap = ctk.CTkFrame(self.step_panel, fg_color="transparent")
        wrap.pack(fill="both", expand=True, padx=30, pady=26)

        self._kicker(wrap, "PASO 03 — GENERAR").pack(anchor="w", pady=(0, 8))
        self._title(wrap, "Todo listo para anonimizar").pack(anchor="w", pady=(0, 6))
        self._subtitle(wrap,
            "Se creará una copia del documento con los pseudónimos aplicados. "
            "El original se conserva intacto."
        ).pack(anchor="w", pady=(0, 22))

        # Resumen de archivos
        summary = ctk.CTkFrame(wrap, fg_color="transparent")
        summary.pack(fill="x", pady=(0, 14))

        for col, (kicker, name) in enumerate([
            ("DOCUMENTO", self.doc_path.name if self.doc_path else "—"),
            ("MAPEO", self.xlsx_path.name if self.xlsx_path else "—"),
        ]):
            card = ctk.CTkFrame(
                summary, fg_color=COLOR_PANEL_ALT,
                border_width=1, border_color=COLOR_BORDER_SOFT, corner_radius=6,
            )
            card.pack(side="left", fill="both", expand=True,
                      padx=(0, 6) if col == 0 else (6, 0))
            inner = ctk.CTkFrame(card, fg_color="transparent")
            inner.pack(fill="both", expand=True, padx=16, pady=14)
            ctk.CTkLabel(inner, text=kicker,
                         font=ctk.CTkFont(family="Consolas", size=10, weight="bold"),
                         text_color=COLOR_TEXT_MUTED).pack(anchor="w", pady=(0, 4))
            ctk.CTkLabel(inner, text=name,
                         font=ctk.CTkFont(size=13, weight="bold"),
                         text_color=COLOR_TEXT, anchor="w").pack(anchor="w")

        # Confirmación verde
        if self.doc_path:
            output_name = f"{self.doc_path.stem}_anonimizado{self.doc_path.suffix}"
        else:
            output_name = "(documento)_anonimizado"

        confirm = ctk.CTkFrame(
            wrap, fg_color="#0F1F18",
            border_width=1, border_color=COLOR_SUCCESS, corner_radius=6,
        )
        confirm.pack(fill="x", pady=(0, 14))
        ctk.CTkLabel(
            confirm,
            text=f"✓  Listo. Se generará  {output_name}  en la misma carpeta.",
            font=ctk.CTkFont(family="Consolas", size=12),
            text_color=COLOR_TEXT, justify="left",
        ).pack(anchor="w", padx=16, pady=12)

        # Footer
        nav = ctk.CTkFrame(wrap, fg_color="transparent")
        nav.pack(fill="x", side="bottom", pady=(18, 0))

        ctk.CTkButton(
            nav, text="←  Volver",
            width=90, height=32,
            fg_color="transparent", hover_color=COLOR_PANEL_ALT,
            text_color=COLOR_TEXT_DIM,
            font=ctk.CTkFont(size=12),
            command=lambda: self._goto_step(2),
        ).pack(side="left")

        self.btn_apply = ctk.CTkButton(
            nav, text="GENERAR DOCUMENTO ANONIMIZADO",
            height=42,
            fg_color=COLOR_SUCCESS, hover_color=COLOR_SUCCESS_DARK,
            text_color="#06130D",
            font=ctk.CTkFont(size=13, weight="bold"),
            state="normal" if (self.doc_path and self.xlsx_path) else "disabled",
            command=self._run_apply,
        )
        self.btn_apply.pack(side="right")

    # ============================================================
    # WALLPAPER RESIZE
    # ============================================================
    # ============================================================
    # COMMAND-LINE / DRAG & DROP
    # ============================================================
    def _handle_command_line_args(self, file_path):
        potential_path = Path(file_path)
        if potential_path.exists() and potential_path.suffix.lower() in [".docx", ".pdf"]:
            self.doc_path = potential_path
            self._auto_advance()

    # ============================================================
    # LÓGICA — PRESERVADA DEL ORIGINAL
    # ============================================================
    def _select_doc(self):
        filename = filedialog.askopenfilename(
            filetypes=[
                ("Documentos Soportados", "*.docx *.pdf"),
                ("Word", "*.docx"),
                ("PDF", "*.pdf"),
            ]
        )
        if filename:
            self.doc_path = Path(filename)
            self.status_bar.configure(text=f"●  documento: {self.doc_path.name}", text_color=COLOR_TEXT_DIM)
            self._auto_advance()

    def _load_existing_xlsx(self):
        filename = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
        if filename:
            self.xlsx_path = Path(filename)
            self.status_bar.configure(text=f"●  mapeo: {self.xlsx_path.name}", text_color=COLOR_TEXT_DIM)
            self._auto_advance()

    def _check_ready(self):
        # Mantenido por compatibilidad; el stepper hace la habilitación.
        pass

    def _open_excel(self):
        if self.xlsx_path and self.xlsx_path.exists():
            os.startfile(self.xlsx_path)

    def _run_detection(self):
        if not self.doc_path:
            messagebox.showwarning("Atención", "Primero debes seleccionar un documento.")
            return

        suggested = self.doc_path.parent / f"{self.doc_path.stem}_mapeo.xlsx"
        self.xlsx_path = Path(suggested)

        try:
            self.btn_detect.configure(state="disabled", text="Procesando...")
        except Exception:
            pass
        self.status_bar.configure(text=f"●  procesando {self.doc_path.suffix.upper()}...",
                                   text_color=COLOR_WARNING)

        threading.Thread(target=self._detection_thread, daemon=True).start()

    def _detection_thread(self):
        try:
            from anonymizer.known_entities import load
            from anonymizer.matcher import EntityMatcher

            doc = extract_document(self.doc_path)
            fresh_db = load()
            entities = detector.detect_all(doc, known_entities=fresh_db)

            matcher = EntityMatcher()
            matcher.db = fresh_db

            rows = []
            seen = set()
            generator = mapping_mod.AutoPseudonymGenerator()

            for ent in entities:
                ent_key = (ent.text, ent.entity_type)
                if ent_key in seen:
                    continue
                seen.add(ent_key)

                pseudo = matcher.match(ent.text, ent.entity_type)

                if pseudo:
                    origen = "DB"
                    accion = "s"
                else:
                    pseudo = generator.get_pseudonym(ent.text, ent.entity_type.value)
                    origen = ent.source.upper()
                    accion = ""

                rows.append({
                    "original": ent.text,
                    "contexto": ent.context,
                    "tipo": ent.entity_type.value,
                    "pseudonimo": pseudo,
                    "accion": accion,
                    "guardar_db": "",
                    "origen": origen
                })

            mapping_mod.save_extended_excel(rows, self.xlsx_path)
            self.after(0, self._detection_success)

        except Exception as e:
            error_str = str(e)
            self.after(0, lambda: self._process_error(f"Error en detección: {error_str}"))

    def _detection_success(self):
        self.status_bar.configure(text=f"●  excel generado: {self.xlsx_path.name}",
                                   text_color=COLOR_SUCCESS)
        self._auto_advance()

        if messagebox.askyesno("Éxito",
                               f"Detección completada.\nSe ha generado {self.xlsx_path.name}\n\n"
                               "¿Quieres abrir el Excel ahora para revisarlo?"):
            self._open_excel()

    def _run_apply(self):
        if not (self.doc_path and self.xlsx_path):
            return

        output_file = self.doc_path.parent / f"{self.doc_path.stem}_anonimizado{self.doc_path.suffix}"

        try:
            self.btn_apply.configure(state="disabled", text="Generando copia...")
        except Exception:
            pass
        self.status_bar.configure(text="●  aplicando anonimización...",
                                   text_color=COLOR_WARNING)

        threading.Thread(target=self._apply_thread, args=(output_file,), daemon=True).start()

    def _apply_thread(self, output_file):
        try:
            full_data = mapping_mod.load_extended_data(self.xlsx_path)

            if not full_data:
                self.after(0, lambda: messagebox.showwarning(
                    "Vacio", "No se encontraron reemplazos con acción 's' en el Excel."))
                self.after(0, self._apply_finished)
                return

            mapping = {d["original"]: d["pseudonimo"] for d in full_data}
            modes = {d["original"]: d.get("modo", "palabra") for d in full_data}

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

            anonymize_document(self.doc_path, output_file, mapping, modes)

            msg = f"Documento guardado: {output_file.name}"
            if db_added > 0:
                msg += f"\nSe agregaron {db_added} entidades a la DB maestra."

            self.after(0, lambda m=msg: self._apply_success(output_file, m))

        except Exception as e:
            error_str = str(e)
            self.after(0, lambda: self._process_error(f"Error al anonimizar: {error_str}"))

    def _apply_success(self, output_file, message):
        self._apply_finished()
        self.status_bar.configure(text=f"●  {output_file.name}", text_color=COLOR_SUCCESS)
        if messagebox.askyesno("Completado", f"{message}\n\n¿Deseas abrir la carpeta contenedora?"):
            os.startfile(output_file.parent)

    def _apply_finished(self):
        try:
            self.btn_apply.configure(state="normal", text="GENERAR DOCUMENTO ANONIMIZADO")
        except Exception:
            pass

    def _process_error(self, msg):
        try:
            self.btn_detect.configure(state="normal", text="Detectar y generar Excel")
        except Exception:
            pass
        try:
            self.btn_apply.configure(state="normal", text="GENERAR DOCUMENTO ANONIMIZADO")
        except Exception:
            pass
        self.status_bar.configure(text="●  error", text_color=COLOR_DANGER)
        messagebox.showerror("Error", msg)

    def _manage_db(self):
        try:
            from anonymizer import known_entities as ke
            db_path = Path(current_settings.db_path)

            if not db_path.exists():
                ke.save([])

            self.status_bar.configure(text=f"●  abriendo db maestra: {db_path.name}",
                                       text_color=COLOR_TEXT_DIM)
            os.startfile(db_path)

            messagebox.showinfo(
                "Base de Datos Maestra",
                "Se ha abierto el Excel de la Base de Datos Maestra.\n\n"
                "Los cambios que guardes en Excel se aplicarán automáticamente "
                "la próxima vez que inicies un proceso de detección.\n\n"
                "Nota: Si borras filas en el Excel, dejarán de detectarse."
            )

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir la DB: {str(e)}")

    def _open_regex_editor(self):
        try:
            from anonymizer.regex_editor import RegexEditorWindow
            editor = RegexEditorWindow(self)
            editor.focus()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el editor de regex: {str(e)}")

    def _run_deanonymize(self):
        filename = filedialog.askopenfilename(
            title="Paso 1: Seleccionar documento anonimizado",
            filetypes=[("Documentos Soportados", "*.docx *.pdf"),
                       ("Word", "*.docx"), ("PDF", "*.pdf")],
        )
        if not filename:
            return
        anon_path = Path(filename)

        xlsx_name = filedialog.askopenfilename(
            title="Paso 2: Seleccionar archivo Excel de mapeo",
            filetypes=[("Excel", "*.xlsx")],
        )
        if not xlsx_name:
            return
        mapping_path = Path(xlsx_name)

        out_filename = filedialog.asksaveasfilename(
            title="Paso 3: Guardar documento restaurado",
            defaultextension=anon_path.suffix,
            initialfile=f"{anon_path.stem}_original{anon_path.suffix}",
            filetypes=[("Word", "*.docx"), ("PDF", "*.pdf")],
        )
        if not out_filename:
            return

        output_path = Path(out_filename)
        self.btn_revert.configure(state="disabled", text="Revirtiendo...")
        self.status_bar.configure(text=f"●  restaurando {anon_path.name}...",
                                   text_color=COLOR_WARNING)

        threading.Thread(
            target=self._deanonymize_thread,
            args=(anon_path, output_path, mapping_path),
            daemon=True,
        ).start()

    def _deanonymize_thread(self, anon_path: Path, output_path: Path, mapping_path: Path):
        try:
            from anonymizer import replacer
            if anon_path.suffix.lower() == ".docx":
                replacer.deanonymize_docx(anon_path, output_path, mapping_path)
            else:
                replacer.deanonymize_pdf(anon_path, output_path, mapping_path)

            self.after(0, lambda: self._deanonymize_success(output_path))
        except Exception as e:
            error_str = str(e)
            self.after(0, lambda: self._deanonymize_error(error_str))

    def _deanonymize_success(self, output_path: Path):
        self.btn_revert.configure(state="normal", text="↩  Revertir")
        self.status_bar.configure(text=f"●  restaurado: {output_path.name}",
                                   text_color=COLOR_SUCCESS)
        if messagebox.askyesno(
            "Completado",
            f"Documento restaurado exitosamente:\n{output_path.name}\n\n¿Deseas abrir la carpeta?"
        ):
            os.startfile(output_path.parent)

    def _deanonymize_error(self, msg: str):
        self.btn_revert.configure(state="normal", text="↩  Revertir")
        self.status_bar.configure(text="●  error en reversión", text_color=COLOR_DANGER)
        messagebox.showerror("Error al revertir", msg)

    def _open_settings(self):
        if SETTINGS_PATH.exists():
            os.startfile(SETTINGS_PATH)
        else:
            messagebox.showerror("Error", "No se encontró el archivo de ajustes.")

    def _show_help(self):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        paths_to_check = [
            get_resource_path("docs/mini_manual.html"),
            get_resource_path("mini_manual.html"),
            Path(base_dir) / "docs" / "mini_manual.html",
            Path(base_dir) / "mini_manual.html"
        ]

        found_file = None
        for p in paths_to_check:
            if p and Path(p).exists():
                found_file = p
                break

        if found_file:
            try:
                os.startfile(str(found_file))
                self.status_bar.configure(text=f"●  ayuda: {Path(found_file).name}",
                                           text_color=COLOR_TEXT_DIM)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir el manual HTML:\n{str(e)}")
        else:
            messagebox.showerror("Archivo No Encontrado",
                                  "No se pudo encontrar 'mini_manual.html'.")


if __name__ == "__main__":
    app = AnonymizerGUI()
    app.mainloop()
