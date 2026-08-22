import sys
import time
import textwrap
import webbrowser
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

CONFIG_IDIOMAS = {
    "KOREAN": {
        "fuente_archivo": "malgun.ttf", 
        "nombre_comun": "Malgun Gothic", 
        "size": 32, "size_mp4": 65, "width": 18, 
        "idiomas": ["Korean"]
    },
    "CJK": {
        "fuente_archivo": "msyh.ttc", 
        "nombre_comun": "Microsoft YaHei", 
        "size": 32, "size_mp4": 60, "width": 18, 
        "idiomas": ["Chinese", "Japanese"]
    },
    "ARABIC_PERSIAN_URDU": {
        "fuente_archivo": "segoeui.ttf", 
        "nombre_comun": "Segoe UI", 
        "size": 32, "size_mp4": 60, "width": 38, 
        "idiomas": ["Arabic", "Persian", "Urdu", "Pashto", "Kurdish", "Punjabi-Pakistan"]
    },
    "HEBREW": {
        "fuente_archivo": "segoeui.ttf", 
        "nombre_comun": "Segoe UI", 
        "size": 32, "size_mp4": 60, "width": 38, 
        "idiomas": ["Hebrew"]
    },
    "LEELAWADEE_SCRIPTS": {
        "fuente_archivo": [
            "LeelawUI.ttf", 
            "LeelaUIb.ttf", 
            "leelawad.ttf", 
            "LEELAWAD.TTF",
            "laoui.ttf"
        ], 
        "nombre_comun": "Leelawadee UI", 
        "size": 30, "size_mp4": 75, "width": 30, 
        "idiomas": ["Thai", "Lao"]
    },
    "BURMESE": {
        "fuente_archivo": "mmrtext.ttf", 
        "nombre_comun": "Myanmar Text", 
        "size": 30, "size_mp4": 70, "width": 30, 
        "idiomas": ["Burmese"]
    },
    "INDIC_SCRIPTS": {
        "fuente_archivo": ["nirmala.ttc", "Nirmala.ttf", "nirmalab.ttf", "NirmalaB.ttf"], 
        "nombre_comun": "Nirmala UI", 
        "size": 30, "size_mp4": 80, "width": 32, 
        "idiomas": [
            "Bengali", "Punjabi-India", "Telugu", "Tamil", 
            "Nepali", "Hindi", "Marathi", "Sinhala", "Gujarati", "Malayalam"
        ]
    },
    "GEORGIAN": {
        "fuente_archivo": "sylfaen.ttf", 
        "nombre_comun": "Sylfaen", 
        "size": 30, "size_mp4": 70, "width": 35, 
        "idiomas": ["Georgian"]
    },
    "ETHIOPIC": {
        "fuente_archivo": "ebrima.ttf", 
        "nombre_comun": "Ebrima", 
        "size": 30, "size_mp4": 75, "width": 35, 
        "idiomas": ["Amharic"]
    },
    "ARMENIAN": {
        "fuente_archivo": "segoeui.ttf", 
        "nombre_comun": "Segoe UI", 
        "size": 30, "size_mp4": 60, "width": 38, 
        "idiomas": ["Armenian"]
    },
    "CYRILLIC": {
        "fuente_archivo": "segoeui.ttf", 
        "nombre_comun": "Segoe UI", 
        "size": 28, "size_mp4": 60, "width": 45, 
        "idiomas": ["Russian", "Ukrainian", "Belarusian", "Bulgarian", "Serbian", "Macedonian", "Kazakh", "Mongolian"]
    },
    "LATIN_STANDARD": {
        "fuente_archivo": "segoeui.ttf", 
        "nombre_comun": "Segoe UI", 
        "size": 28, "size_mp4": 60, "width": 45, 
        "idiomas": [
            "Spanish", "English", "Italian", "French", "Portuguese", "German", "Polish", "Dutch",
            "Turkish", "Indonesian", "Filipino", "Vietnamese", "Swahili", "Romanian", "Malay", "Hausa",
            "Greek", "Yoruba", "Sundanese", "Zulu", "Afrikaans", "Hungarian", "Czech", "Swedish",
            "Albanian", "Croatian", "Danish", "Finnish", "Slovak", "Norwegian", "Lombard", "Bosnian",
            "Lithuanian", "Pangasinan", "Slovenian", "Galician", "Irish", "Estonian", "Latin", "Catalan",
            "Quechua", "Azerbaijani"
        ]
    }
}

LISTA_IDIOMAS = sorted([
    "Spanish", "English", "Italian", "French", "Portuguese", "German", "Polish", "Ukrainian",
    "Russian", "Dutch", "Chinese", "Japanese", "Korean", "Arabic", "Turkish", "Persian",
    "Indonesian", "Bengali", "Urdu", "Filipino", "Vietnamese", "Hindi", "Swahili", "Romanian",
    "Punjabi-Pakistan", "Punjabi-India", "Telugu", "Malay", "Tamil", "Hausa", "Thai",
    "Greek", "Yoruba", "Pashto", "Sundanese", "Kurdish", "Burmese", "Amharic", "Nepali",
    "Zulu", "Afrikaans", "Hungarian", "Serbian", "Czech", "Swedish", "Hebrew", "Bulgarian",
    "Albanian", "Belarusian", "Armenian", "Croatian", "Danish", "Mongolian", "Finnish", "Slovak",
    "Norwegian", "Lombard", "Bosnian", "Lithuanian", "Pangasinan", "Macedonian", "Slovenian",
    "Galician", "Irish", "Estonian", "Latin", "Catalan", "Marathi", "Sinhala", "Gujarati",
    "Quechua", "Georgian", "Azerbaijani", "Lao", "Kazakh", "Malayalam"
])

FPS = 30
SIGNOS_PUNTO = ['.', '?', '!', ':', '。', '？', '！', '।', '؟']
SIGNOS_COMA = [',', ';', '，', '；', '،', '、']

FORMATOS_VIDEO = {
    "16:9 Horizontal (1920x1080)": {"res": (1920, 1080), "preview": "1000x562", "width_factor": 1.0},
    "9:16 Vertical (1080x1920)": {"res": (1080, 1920), "preview": "450x800", "width_factor": 0.5}
}

class SimuladorSubtitulos:
    def __init__(self, root):
        self.root = root
        self.root.title("Control Panel - Subtitles Pro")
        self.root.geometry("520x660")
        self.root.resizable(False, False)

        self.escribiendo = False
        self.pausado = False
        self.arrastrando_slider = False
        self.ruta_archivo = ""
        self.bloques_subtitulos = []
        self.tiempos_bloques = []
        self.tiempo_total_segundos = 0
        self.tiempo_original_base = 0
        self.indice_bloque_actual = 0

        self.vel_base = 0.050
        self.pausa_punto = 0.600
        self.pausa_coma = 0.300
        self.tiempo_lectura = 3.0

        self.font_family_gui = "Segoe UI"
        self.font_files = "segoeui.ttf"
        self.font_size = 28
        self.font_size_mp4 = 60
        self.ancho_linea_base = 45
        self.ancho_linea = 45

        self.crear_menu_superior()

        self.ventana_proyeccion = tk.Toplevel(self.root)
        self.ventana_proyeccion.title("PREVIEW SCREEN")
        self.ventana_proyeccion.geometry("1000x562")
        self.ventana_proyeccion.configure(bg="#126e47")

        self.root.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)
        self.ventana_proyeccion.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)

        self.canvas = tk.Canvas(
            self.ventana_proyeccion,
            bg=self.ventana_proyeccion["bg"],
            highlightthickness=0,
            bd=0
        )
        self.canvas.pack(fill="both", expand=True)

        frame = ttk.Frame(self.root, padding=15)
        frame.pack(fill="both", expand=True)

        # Configuración de Idioma
        ttk.Label(frame, text="Text Language:", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.combo_idioma = ttk.Combobox(frame, values=LISTA_IDIOMAS, state="readonly")
        self.combo_idioma.set("English")
        self.combo_idioma.pack(fill="x", pady=(2, 6))
        self.combo_idioma.bind("<<ComboboxSelected>>", self.al_cambiar_idioma)

        # Configuración de Aspect Ratio / Formato
        ttk.Label(frame, text="Video Output Format:", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.combo_formato = ttk.Combobox(frame, values=list(FORMATOS_VIDEO.keys()), state="readonly")
        self.combo_formato.set("16:9 Horizontal (1920x1080)")
        self.combo_formato.pack(fill="x", pady=(2, 6))
        self.combo_formato.bind("<<ComboboxSelected>>", self.al_cambiar_formato)

        self.lbl_archivo = ttk.Label(frame, text="No file selected", wraplength=480)
        self.lbl_archivo.pack(fill="x", pady=2)

        self.btn_cargar = ttk.Button(frame, text="📂 Select TXT File", command=self.seleccionar_archivo)
        self.btn_cargar.pack(fill="x", pady=4)

        self.frame_tiempo_adj = ttk.LabelFrame(frame, text=" Final Duration Adjustment (±50%) ", padding=8)
        self.frame_tiempo_adj.pack(fill="x", pady=6)

        self.lbl_ritmo_info = ttk.Label(self.frame_tiempo_adj, text="Load a TXT file to enable speed adjustment", font=("Segoe UI", 9))
        self.lbl_ritmo_info.pack(anchor="center", pady=(0, 4))

        self.slider_ritmo_var = tk.DoubleVar(value=0)
        self.slider_ritmo = ttk.Scale(
            self.frame_tiempo_adj, 
            from_=-50, 
            to=50, 
            orient="horizontal", 
            variable=self.slider_ritmo_var,
            command=self.al_mover_slider_ritmo,
            state="disabled"
        )
        self.slider_ritmo.pack(fill="x")

        frame_marcas = ttk.Frame(self.frame_tiempo_adj)
        frame_marcas.pack(fill="x", pady=(2, 0))
        ttk.Label(frame_marcas, text="-50% (Very Fast)", font=("Segoe UI", 8)).pack(side="left")
        ttk.Label(frame_marcas, text="0% (Original)", font=("Segoe UI", 8, "bold")).pack(side="left", expand=True)
        ttk.Label(frame_marcas, text="+50% (Very Slow)", font=("Segoe UI", 8)).pack(side="right")

        ttk.Separator(frame, orient='horizontal').pack(fill='x', pady=6)

        frame_slider = ttk.LabelFrame(frame, text=" Timeline & Progress Control ", padding=8)
        frame_slider.pack(fill="x", pady=4)

        self.slider_var = tk.DoubleVar(value=0)
        self.slider = ttk.Scale(
            frame_slider, 
            from_=0, 
            to=100, 
            orient="horizontal", 
            variable=self.slider_var,
            command=self.al_mover_slider
        )
        self.slider.pack(fill="x")
        self.slider.bind("<ButtonPress-1>", self.al_iniciar_arrastre)
        self.slider.bind("<ButtonRelease-1>", self.al_soltar_arrastre)

        self.lbl_tiempo = ttk.Label(frame_slider, text="00:00 / 00:00 (0%)", font=("Segoe UI", 10, "bold"))
        self.lbl_tiempo.pack(anchor="center", pady=(5, 0))

        self.lbl_progreso = ttk.Label(frame_slider, text="Block: 0 / 0")
        self.lbl_progreso.pack(anchor="e")

        self.btn_iniciar = ttk.Button(frame, text="▶ Live Preview", command=self.iniciar, state="disabled")
        self.btn_iniciar.pack(fill="x", pady=3)

        frame_ctrl = ttk.Frame(frame)
        frame_ctrl.pack(fill="x", pady=3)
        
        self.btn_pausar = ttk.Button(frame_ctrl, text="⏸ Pause", command=self.alternar_pausa, state="disabled")
        self.btn_pausar.pack(side="left", fill="x", expand=True, padx=(0,4))

        self.btn_reiniciar = ttk.Button(frame_ctrl, text="🔄 Reset", command=self.reiniciar, state="disabled")
        self.btn_reiniciar.pack(side="left", fill="x", expand=True)

        ttk.Separator(frame, orient='horizontal').pack(fill='x', pady=6)

        self.btn_exportar = ttk.Button(frame, text="🎬 EXPORT TO MP4 FILE", command=self.exportar_mp4, state="disabled")
        self.btn_exportar.pack(fill="x", ipady=4)

        self.al_cambiar_idioma()

    def cerrar_aplicacion(self):
        self.escribiendo = False
        self.pausado = False
        try:
            self.root.destroy()
        except Exception:
            pass

    def crear_menu_superior(self):
        barra_menu = tk.Menu(self.root)
        menu_ayuda = tk.Menu(barra_menu, tearoff=0)
        menu_ayuda.add_command(label="About / Credits", command=self.mostrar_acerca_de)
        barra_menu.add_cascade(label="Help", menu=menu_ayuda)
        self.root.config(menu=barra_menu)

    def mostrar_acerca_de(self):
        ventana_about = tk.Toplevel(self.root)
        ventana_about.title("About - Subtitles Pro")
        ventana_about.geometry("380x250")
        ventana_about.resizable(False, False)
        ventana_about.configure(bg="#1a202c")
        
        ventana_about.transient(self.root)
        ventana_about.grab_set()

        tk.Label(ventana_about, text="Subtitles Pro Generator", font=("Segoe UI", 14, "bold"), fg="#ffffff", bg="#1a202c").pack(pady=(20, 5))
        tk.Label(ventana_about, text="Developed by José Galindo", font=("Segoe UI", 11, "bold"), fg="#319795", bg="#1a202c").pack(pady=2)
        tk.Label(ventana_about, text="Pro Content Automation Tool", font=("Segoe UI", 9, "italic"), fg="#a0aec0", bg="#1a202c").pack(pady=(0, 15))

        btn_web = tk.Button(
            ventana_about, 
            text="🌐 Visit GABRIELS.WORK", 
            font=("Segoe UI", 10, "bold"), 
            bg="#319795", 
            fg="white", 
            activebackground="#2b6cb0", 
            activeforeground="white",
            relief="flat", 
            padx=12, 
            pady=6, 
            command=lambda: webbrowser.open("https://gabriels.work"), 
            cursor="hand2"
        )
        btn_web.pack(pady=10)
        tk.Label(ventana_about, text="© All rights reserved", font=("Segoe UI", 8), fg="#718096", bg="#1a202c").pack(side="bottom", pady=10)

    def al_cambiar_formato(self, event=None):
        fmt_info = FORMATOS_VIDEO.get(self.combo_formato.get())
        if fmt_info:
            self.ventana_proyeccion.geometry(fmt_info["preview"])
            self.calcular_ancho_linea()
            if self.ruta_archivo:
                self.preprocesar_texto()

    def al_cambiar_idioma(self, event=None):
        idioma = self.combo_idioma.get()
        config_encontrada = None
        
        for grupo, datos in CONFIG_IDIOMAS.items():
            if idioma in datos["idiomas"]:
                config_encontrada = datos
                break

        if not config_encontrada:
            return

        self.font_files = config_encontrada["fuente_archivo"]
        self.font_family_gui = config_encontrada["nombre_comun"]
        self.font_size = config_encontrada["size"]
        self.font_size_mp4 = config_encontrada.get("size_mp4", 60)
        self.ancho_linea_base = config_encontrada["width"]

        self.calcular_ancho_linea()

        if self.ruta_archivo:
            self.preprocesar_texto()

    def calcular_ancho_linea(self):
        fmt_info = FORMATOS_VIDEO.get(self.combo_formato.get(), {})
        factor = fmt_info.get("width_factor", 1.0)
        self.ancho_linea = max(int(self.ancho_linea_base * factor), 10)

    def seleccionar_archivo(self):
        archivo = filedialog.askopenfilename(
            title="Select Text File",
            filetypes=[("Text Files (*.txt)", "*.txt"), ("All Files", "*.*")]
        )
        if archivo:
            self.ruta_archivo = archivo
            nombre = os.path.basename(archivo)
            self.lbl_archivo.configure(text=f"File: {nombre}")
            
            self.slider_ritmo_var.set(0)
            self.slider_ritmo.configure(state="normal")
            
            self.vel_base = 0.050
            self.pausa_punto = 0.600
            self.pausa_coma = 0.300
            self.tiempo_lectura = 3.0
            
            self.preprocesar_texto()
            self.tiempo_original_base = self.tiempo_total_segundos
            
            self.actualizar_texto_ritmo(0)

            self.btn_iniciar.configure(state="normal")
            self.btn_exportar.configure(state="normal")

    def preprocesar_texto(self):
        try:
            with open(self.ruta_archivo, "r", encoding="utf-8") as file:
                texto_completo = file.read()
        except Exception as e:
            messagebox.showerror("Error", f"Could not read the file:\n{e}")
            return

        lineas_limpias = [l.strip() for l in texto_completo.splitlines() if l.strip() != ""]
        texto_unificado = " ".join(lineas_limpias)
        renglones = textwrap.wrap(texto_unificado, width=self.ancho_linea)

        self.bloques_subtitulos = []
        for i in range(0, len(renglones), 2):
            bloque = renglones[i:i+2]
            self.bloques_subtitulos.append("\n".join(bloque))

        self.recalcular_tiempos()

    def recalcular_tiempos(self):
        self.tiempos_bloques = []
        frames_acumulados = 0

        for bloque in self.bloques_subtitulos:
            for car in bloque:
                if car in SIGNOS_PUNTO:
                    duracion = self.pausa_punto
                elif car in SIGNOS_COMA:
                    duracion = self.pausa_coma
                elif car == '\n':
                    duracion = 0.1
                else:
                    duracion = self.vel_base
                
                num_f = int(round(duracion * FPS))
                frames_acumulados += max(1, num_f)
            
            frames_acumulados += int(round(self.tiempo_lectura * FPS))
            self.tiempos_bloques.append(frames_acumulados / float(FPS))

        self.tiempo_total_segundos = frames_acumulados / float(FPS) if FPS > 0 else 0
        total = len(self.bloques_subtitulos)
        self.slider.configure(to=max(total - 1, 0))
        self.actualizar_etiqueta_progreso(0)

    def al_mover_slider_ritmo(self, val):
        if not self.ruta_archivo or self.tiempo_original_base == 0:
            return

        porcentaje_variacion = float(val)
        delta = 1.0 + (porcentaje_variacion / 100.0)

        self.vel_base = 0.050 * delta
        self.pausa_punto = 0.600 * delta
        self.pausa_coma = 0.300 * delta
        self.tiempo_lectura = 3.0 * delta

        self.recalcular_tiempos()
        self.actualizar_texto_ritmo(porcentaje_variacion)

    def actualizar_texto_ritmo(self, pct):
        fmt_total = self.formatear_tiempo(self.tiempo_total_segundos)
        signo = "+" if pct > 0 else ""
        self.lbl_ritmo_info.configure(
            text=f"Adjustment: {signo}{pct:.1f}%  |  Final Duration: {fmt_total}",
            font=("Segoe UI", 9, "bold")
        )

    def formatear_tiempo(self, segundos):
        horas = int(segundos // 3600)
        minutos = int((segundos % 3600) // 60)
        segs = int(segundos % 60)
        if horas > 0:
            return f"{horas:02d}:{minutos:02d}:{segs:02d}"
        else:
            return f"{minutos:02d}:{segs:02d}"

    def actualizar_etiqueta_progreso(self, indice):
        total = len(self.bloques_subtitulos)
        if total == 0:
            self.lbl_tiempo.configure(text="00:00 / 00:00 (0%)")
            self.lbl_progreso.configure(text="Block: 0 / 0")
            return

        tiempo_actual = self.tiempos_bloques[indice] if indice < len(self.tiempos_bloques) else self.tiempo_total_segundos
        porcentaje = int((tiempo_actual / max(self.tiempo_total_segundos, 1)) * 100)
        
        t_actual_fmt = self.formatear_tiempo(tiempo_actual)
        t_total_fmt = self.formatear_tiempo(self.tiempo_total_segundos)

        self.lbl_tiempo.configure(text=f"{t_actual_fmt} / {t_total_fmt} ({porcentaje}%)")
        self.lbl_progreso.configure(text=f"Block: {indice + 1} / {total}")

    def al_iniciar_arrastre(self, event):
        self.arrastrando_slider = True

    def al_soltar_arrastre(self, event):
        self.arrastrando_slider = False
        if self.bloques_subtitulos:
            nuevo_idx = int(round(self.slider_var.get()))
            self.indice_bloque_actual = nuevo_idx
            bloque_texto = self.bloques_subtitulos[self.indice_bloque_actual]
            self.actualizar_pantalla_con_sombra(bloque_texto)

    def al_mover_slider(self, val):
        if self.arrastrando_slider and self.bloques_subtitulos:
            idx = int(round(float(val)))
            self.actualizar_etiqueta_progreso(idx)
            bloque_texto = self.bloques_subtitulos[idx]
            self.actualizar_pantalla_con_sombra(bloque_texto)

    def actualizar_pantalla_con_sombra(self, texto):
        try:
            self.canvas.delete("all")
            if not texto: return

            x = self.canvas.winfo_width() / 2
            y = self.canvas.winfo_height() / 2

            fuente_config = (self.font_family_gui, self.font_size, "bold")
            d = 3

            self.canvas.create_text(x-d, y-d, text=texto, font=fuente_config, fill="black", justify="center", anchor="center")
            self.canvas.create_text(x+d, y-d, text=texto, font=fuente_config, fill="black", justify="center", anchor="center")
            self.canvas.create_text(x-d, y+d, text=texto, font=fuente_config, fill="black", justify="center", anchor="center")
            self.canvas.create_text(x+d, y+d, text=texto, font=fuente_config, fill="black", justify="center", anchor="center")
            self.canvas.create_text(x, y, text=texto, font=fuente_config, fill="white", justify="center", anchor="center")
        except Exception:
            pass

    def iniciar(self):
        if not self.escribiendo and self.bloques_subtitulos:
            self.escribiendo = True
            self.pausado = False
            self.combo_idioma.configure(state="disabled")
            self.combo_formato.configure(state="disabled")
            self.btn_cargar.configure(state="disabled")
            self.slider_ritmo.configure(state="disabled")
            self.btn_iniciar.configure(state="disabled")
            self.btn_exportar.configure(state="disabled")
            self.btn_pausar.configure(state="normal", text="⏸ Pause")
            self.btn_reiniciar.configure(state="normal")
            
            self.ventana_proyeccion.update_idletasks()
            self.hilo_escritura = threading.Thread(target=self.bucle_escritura, daemon=True)
            self.hilo_escritura.start()

    def alternar_pausa(self):
        self.pausado = not self.pausado
        self.btn_pausar.configure(text="▶ Resume" if self.pausado else "⏸ Pause")

    def reiniciar(self):
        self.escribiendo = False
        self.pausado = False
        self.indice_bloque_actual = 0
        self.slider_var.set(0)
        self.actualizar_etiqueta_progreso(0)
        self.actualizar_pantalla_con_sombra("")
        
        self.combo_idioma.configure(state="readonly")
        self.combo_formato.configure(state="readonly")
        self.btn_cargar.configure(state="normal")
        self.slider_ritmo.configure(state="normal" if self.ruta_archivo else "disabled")
        self.btn_iniciar.configure(state="normal" if self.ruta_archivo else "disabled")
        self.btn_exportar.configure(state="normal" if self.ruta_archivo else "disabled")
        self.btn_pausar.configure(state="disabled", text="⏸ Pause")
        self.btn_reiniciar.configure(state="disabled")

    def bucle_escritura(self):
        while self.indice_bloque_actual < len(self.bloques_subtitulos):
            if not self.escribiendo: break

            bloque = self.bloques_subtitulos[self.indice_bloque_actual]
            texto_acumulado = ""

            if not self.arrastrando_slider:
                self.root.after(0, self.slider_var.set, self.indice_bloque_actual)
                self.root.after(0, self.actualizar_etiqueta_progreso, self.indice_bloque_actual)

            for caracter in bloque:
                while self.pausado or self.arrastrando_slider:
                    if not self.escribiendo: break
                    time.sleep(0.1)

                if not self.escribiendo: break

                texto_acumulado += caracter
                self.root.after(0, self.actualizar_pantalla_con_sombra, texto_acumulado)

                if caracter in SIGNOS_PUNTO:
                    pausa = self.pausa_punto
                elif caracter in SIGNOS_COMA:
                    pausa = self.pausa_coma
                elif caracter == '\n':
                    pausa = 0.1
                else:
                    pausa = self.vel_base

                time.sleep(pausa)

            if self.escribiendo:
                time.sleep(self.tiempo_lectura)

            self.indice_bloque_actual += 1

        self.root.after(0, self.reiniciar)

    def obtener_ruta_fuente_sistema(self, candidatas_fuente):
        windir = os.environ.get("WINDIR", "C:\\Windows")
        if isinstance(candidatas_fuente, str):
            candidatas_fuente = [candidatas_fuente]

        for nombre_archivo in candidatas_fuente:
            ruta_candidata = os.path.join(windir, "Fonts", nombre_archivo)
            if os.path.isfile(ruta_candidata):
                return ruta_candidata
        return None

    def verificar_o_buscar_fuente(self, tamano_px):
        idioma_actual = self.combo_idioma.get()
        ruta_fuente = self.obtener_ruta_fuente_sistema(self.font_files)

        if not ruta_fuente:
            fuentes_str = ", ".join(self.font_files) if isinstance(self.font_files, list) else self.font_files
            msg_error = (
                f"⚠️ MISSING REQUIRED WINDOWS FONT\n\n"
                f"• Target Language: {idioma_actual}\n"
                f"• Required Font File(s): {fuentes_str} ({self.font_family_gui})\n"
                f"• System Status: Font file not found in C:\\Windows\\Fonts\\\n\n"
                f"To export videos in this language without rendering errors:\n\n"
                f"1. Install the required Windows font ('{self.font_family_gui}').\n"
                f"2. Double-click the .ttf or .ttc font file.\n"
                f"3. Click 'Install' at the top of the Windows preview window.\n"
                f"4. Restart this application and try exporting again."
            )
            messagebox.showerror("Font Verification Failed", msg_error)
            return None

        try:
            if ruta_fuente.lower().endswith(".ttc"):
                try:
                    return ImageFont.truetype(ruta_fuente, tamano_px, index=0)
                except Exception:
                    return ImageFont.truetype(ruta_fuente, tamano_px, index=1)
            else:
                return ImageFont.truetype(ruta_fuente, tamano_px)
        except Exception as e:
            messagebox.showerror("Font Error", f"Unable to load font file:\n{e}")
            return None

    def exportar_mp4(self):
        if not self.bloques_subtitulos: return

        fuente_validada = self.verificar_o_buscar_fuente(self.font_size_mp4)
        if fuente_validada is None:
            return

        ruta_salida = filedialog.asksaveasfilename(
            title="Save MP4 Video",
            defaultextension=".mp4",
            filetypes=[("MP4 Video", "*.mp4")]
        )
        if not ruta_salida: return

        self.btn_exportar.configure(state="disabled")
        self.btn_iniciar.configure(state="disabled")
        self.combo_formato.configure(state="disabled")
        self.btn_cargar.configure(state="disabled")
        self.slider_ritmo.configure(state="disabled")

        threading.Thread(target=self._proceso_render_mp4, args=(ruta_salida, fuente_validada), daemon=True).start()

    def _proceso_render_mp4(self, ruta_salida, fuente):
        fmt_info = FORMATOS_VIDEO.get(self.combo_formato.get(), {"res": (1920, 1080)})
        ANCHO, ALTO = fmt_info["res"]
        COLOR_FONDO = (18, 110, 71)
        
        try:
            fourcc = cv2.VideoWriter_fourcc(*'avc1')
            out = cv2.VideoWriter(ruta_salida, fourcc, float(FPS), (ANCHO, ALTO))
            if not out.isOpened():
                raise Exception("avc1 not supported")
        except:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(ruta_salida, fourcc, float(FPS), (ANCHO, ALTO))

        d_sombra = 4

        for idx, bloque in enumerate(self.bloques_subtitulos):
            texto_acumulado = ""

            for caracter in bloque:
                texto_acumulado += caracter
                
                img = Image.new("RGB", (ANCHO, ALTO), COLOR_FONDO)
                draw = ImageDraw.Draw(img)

                try:
                    bbox = draw.multiline_textbbox((0, 0), texto_acumulado, font=fuente, align="center")
                    text_w = bbox[2] - bbox[0]
                    text_h = bbox[3] - bbox[1]
                except Exception:
                    text_w, text_h = 800, 200

                x = (ANCHO - text_w) // 2
                y = (ALTO - text_h) // 2

                for dx, dy in [(-d_sombra,-d_sombra), (d_sombra,-d_sombra), (-d_sombra,d_sombra), (d_sombra,d_sombra)]:
                    draw.multiline_text((x+dx, y+dy), texto_acumulado, font=fuente, fill="black", align="center")

                draw.multiline_text((x, y), texto_acumulado, font=fuente, fill="white", align="center")

                frame_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

                if caracter in SIGNOS_PUNTO:
                    duracion = self.pausa_punto
                elif caracter in SIGNOS_COMA:
                    duracion = self.pausa_coma
                elif caracter == '\n':
                    duracion = 0.1
                else:
                    duracion = self.vel_base

                num_frames = int(round(duracion * FPS))
                if num_frames < 1:
                    num_frames = 1

                for _ in range(num_frames):
                    out.write(frame_cv)

            num_frames_espera = int(round(self.tiempo_lectura * FPS))
            for _ in range(num_frames_espera):
                out.write(frame_cv)

            self.root.after(0, self.slider_var.set, idx)
            self.root.after(0, self.actualizar_etiqueta_progreso, idx)

        out.release()
        
        self.root.after(0, lambda: messagebox.showinfo("Completed!", f"MP4 file successfully exported to:\n{ruta_salida}"))
        self.root.after(0, self.reiniciar)

if __name__ == "__main__":
    root = tk.Tk()
    try:
        style = ttk.Style()
        style.theme_use('clam')
    except:
        pass
        
    app = SimuladorSubtitulos(root)
    root.mainloop()