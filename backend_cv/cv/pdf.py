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
        self.set_font("Roboto", "B", 16)
        self.cell(0, 10, "Matias Pérez Nauto", ln=False, align="L")
        self.set_font("Roboto", "", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f"{self.mes} {self.año}", ln=True, align="R")
        self.set_text_color(0, 0, 0)
        self.set_font("Roboto", "", 9)
        self.set_text_color(100, 100, 100)
        self.cell(0, 4, "contacto@mtsprz.org  |  +56 975475781  |  Ingeniería en Ejecución en Informática", ln=True)
        self.set_text_color(0, 0, 0)
        self.ln(2)
        self.set_draw_color(180, 180, 180)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(3)

    def section_title(self, title):
        self.set_font("Roboto", "B", 9)
        self.set_text_color(43, 108, 176)
        self.cell(0, 5, limpiar_texto(title.upper()), ln=True)
        self.set_text_color(0, 0, 0)
        self.set_draw_color(43, 108, 176)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.set_draw_color(0, 0, 0)
        self.ln(3)

    def render_education_entry(self, institution, years, degree):
        page_w = self.w - self.l_margin - self.r_margin
        self.set_font("Roboto", "B", 10)
        inst_w = min(self.get_string_width(institution) + 2, page_w * 0.7)
        self.cell(inst_w, 5, institution, ln=0)
        self.set_font("Roboto", "", 9)
        self.set_text_color(120, 120, 120)
        self.cell(page_w - inst_w, 5, years, ln=True, align="R")
        self.set_text_color(43, 108, 176)
        self.set_font("Roboto", "", 9)
        self.multi_cell(0, 4, degree, ln=True)
        self.set_text_color(0, 0, 0)
        self.ln(2)

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
    
    def render_experience(self, empresa, fecha, titulo, business, scope, stack, cicd, datasources):
        page_w = self.w - self.l_margin - self.r_margin

        # Empresa (bold) + Fecha (gray right)
        self.set_font("Roboto", "B", 10)
        emp_w = min(self.get_string_width(empresa) + 2, page_w * 0.65)
        self.cell(emp_w, 5, empresa, ln=0)
        self.set_font("Roboto", "", 9)
        self.set_text_color(120, 120, 120)
        self.cell(page_w - emp_w, 5, fecha, ln=True, align="R")
        self.set_text_color(0, 0, 0)

        # Título en azul
        if titulo:
            self.set_text_color(43, 108, 176)
            self.set_font("Roboto", "", 9)
            self.multi_cell(0, 4, titulo, ln=True)
            self.set_text_color(0, 0, 0)

        # Negocio (gray)
        if business:
            self.set_font("Roboto", "", 9)
            self.set_text_color(120, 120, 120)
            self.multi_cell(0, 4, business, ln=True)
            self.set_text_color(0, 0, 0)

        # Descripción/Scope
        if scope:
            self.set_font("Roboto", "", 9)
            self.set_text_color(40, 40, 40)
            self.multi_cell(0, 4, scope, ln=True)
            self.set_text_color(0, 0, 0)

        self.ln(1)

        # Tech line separada por |
        parts = []
        if stack: parts.append(f"Stack: {stack}")
        if cicd:  parts.append(f"CI/CD: {cicd}")
        if datasources: parts.append(f"DB: {datasources}")
        if parts:
            self.set_font("Roboto", "", 8)
            self.set_text_color(80, 80, 80)
            self.multi_cell(0, 4, "  |  ".join(parts), ln=True)
            self.set_text_color(0, 0, 0)

        # Separador suave
        self.set_draw_color(200, 200, 200)
        self.line(self.l_margin, self.get_y() + 1, self.w - self.r_margin, self.get_y() + 1)
        self.set_draw_color(0, 0, 0)
        self.ln(4)

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
        self.multi_cell(0, 4, f"Año de experiencia en tecnología: {tech_line}", align="L")
        self.ln(1)

        # Contacto
        contacto_line = f"{self.contacto['profesion']} | Email: {self.contacto['email']} | Teléfono: {self.contacto['telefono']}"
        self.cell(0, 4, contacto_line, align="L")



