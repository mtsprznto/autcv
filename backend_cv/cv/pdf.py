from fpdf import FPDF
from datetime import datetime

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.utils import formatear_proyecto, limpiar_texto

class PDF(FPDF):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 1. Registro de la fuente Unicode (Asegúrate que la ruta sea correcta)
        # Registramos Roboto1 para estilo normal y negrita
        self.add_font("Roboto", style="", fname="fonts/Roboto-Regular.ttf", uni=True)
        self.add_font("Roboto", style="B", fname="fonts/Roboto-Bold.ttf", uni=True)

        # Guardamos mes y año al instanciar
        ahora = datetime.now()
        self.mes = ahora.strftime("%B")   
        self.año = ahora.strftime("%Y")   

        self.tecnologias_experiencia = {}  # Se setea desde fuera
        self.contacto = {}


    def header(self):
        self.set_font("Arial", "B", 9)
        self.cell(0, 9, limpiar_texto("Resume"), ln=True, align="R")
        self.ln(0)
        self.cell(0, 2, limpiar_texto(f"{self.mes} {self.año} rev"), ln=True, align="R")
        self.ln(2)

    def section_title(self, title):
        self.set_font("Roboto", "B", 12)
        self.set_fill_color(255, 255, 255)
        self.cell(0, 5, limpiar_texto(title), ln=True, fill=True)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(3)

    def multi_section(self, items):
        self.set_font("Roboto", "", 10)
        for line in items:
            self.multi_cell(0, 6, limpiar_texto(line))
        self.ln(2)

    def paragraph(self, text):
        self.set_font("Roboto", "", 10)
        self.multi_cell(0, 6, limpiar_texto(text))
        self.ln(1)

    def sub_paragraph(self, keywords):
        self.set_font("Roboto", "I", 9)
        self.set_text_color(100, 100, 100)  # Gris suave
        self.multi_cell(0, 5, f"{keywords}", align="L")
        self.set_text_color(0, 0, 0)  # Restaurar color negro


    def texto_doble_alineado(self, izquierda: str, derecha: str, estilo="B", tamaño=10):
        """Imprime dos textos en una sola línea: uno alineado a la izquierda y otro a la derecha"""
        self.set_font("Roboto", estilo, tamaño)
        page_width = self.w - 2 * self.l_margin

        derecha_width = self.get_string_width(derecha)
        self.set_x(self.l_margin)
        self.cell(page_width - derecha_width, 6, "")  # espacio hasta texto derecha
        self.cell(derecha_width, 6, derecha, ln=0, align="R")

        self.set_xy(self.l_margin, self.get_y())  # volver al inicio horizontal
        self.cell(page_width, 6, izquierda, ln=1, align="L")


    def proyectos_dinamicos(self, repos: list, max_items=5):
        self.section_title("Proyectos Relevantes (Automáticos)")
        self.set_font("Roboto", "", 10)

        for i, repo in enumerate(repos[:max_items]):
            texto = formatear_proyecto(repo)
            self.multi_cell(0, 6, limpiar_texto(texto))
            self.ln(1)


    def render_proyecto(self, proyecto: dict):
        """Recibe un dict con info del proyecto y lo muestra con formato estilizado"""
        titulo = limpiar_texto(proyecto.get("titulo", ""))
        descripcion = limpiar_texto(proyecto.get("descripcion", ""))
        fecha = proyecto.get("fecha", "")
        url = proyecto.get("url", "")
        lenguajes_completos = proyecto.get("lenguajes_completos", {})
        sitio_web = proyecto.get("sitio_web", "")
        topics = proyecto.get("topics", [])

        # Título en negrita
        self.set_font("Roboto", "B", 10)
        self.multi_cell(0, 6, titulo)

        # Descripción normal
        self.set_font("Roboto", "", 10)
        self.multi_cell(0, 6, descripcion)

        
        # Lenguajes completos
        if lenguajes_completos:
            self.set_font("Roboto", "I", 9)
            self.multi_cell(0, 6, f"Lenguajes: {', '.join(lenguajes_completos.keys())}   |   Actualizado: {fecha}")

        # Topics
        if topics:
            self.set_font("Roboto", "", 9)
            self.multi_cell(0, 6, f"Etiquetas: {', '.join(topics)}")

        # GitHub URL
        if url:
            self.set_text_color(0, 0, 255)
            self.set_font("Roboto", "I", 9)
            self.multi_cell(0, 6, f"Repositorio: {url}")
            self.set_text_color(0, 0, 0)

        # Sitio web si existe
        if sitio_web:
            self.set_text_color(0, 102, 204)
            self.set_font("Roboto", "I", 9)
            self.multi_cell(0, 6, f"Demo: {sitio_web}")
            self.set_text_color(0, 0, 0)

        self.ln(2)
    
    def footer(self):
        self.ln(5)
        self.set_y(-25)
        self.set_font("Roboto", size=7)
        self.set_text_color(100, 100, 100)

        # Línea superior
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(2)

        # Tecnología y años
        tech_line = ", ".join([f"{k}: {v}" for k, v in self.tecnologias_experiencia.items()])
        self.multi_cell(0, 4, f"Technology's year experience: {tech_line}", align="L")
        self.ln(1)

        # Contacto
        contacto_line = f"{self.contacto['profesion']} | Email: {self.contacto['email']} | Mobile: {self.contacto['telefono']}"
        self.cell(0, 4, contacto_line, align="L")



