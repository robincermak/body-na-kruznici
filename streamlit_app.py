import streamlit as st

st.title("Body na kružnici")
st.header("Parametry kružnice")

# informace
with st.sidebar:
    st.header("O autorovi")
    st.write("Jméno: Robin Čermák")
    st.write("Kruh: B1VS16")
    st.write("E-mail: 277729@vutbr.cz")
    st.header("Použité technologie:")
    st.write("Python, Streamlit, Matplotlib, Copilot")

# parametry / vstupy
col1, col2 = st.columns(2)
with col1:
    stred_x = st.number_input("Střed X [jednotka]", value=0.0, format="%f")
    radius = st.number_input("Poloměr [jednotka]", min_value=0.0, value=1.0, format="%f")
    jdntka = st.text_input("Jednotka (např. m)", value="m")
with col2:
    stred_y = st.number_input("Střed Y [jednotka]", value=0.0, format="%f")
    pocet_bodu = st.number_input("Počet bodů na kružnici", min_value=1, value=8, step=1)
    color = st.color_picker("Barva bodů", value="#FF0000")

import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(6, 6))

# výpočet souřadnic
uhel = np.linspace(0, 2 * np.pi, pocet_bodu, endpoint=False)
x_body = stred_x + radius * np.cos(uhel)
y_body = stred_y + radius * np.sin(uhel)

# vykreslení
kruznice = plt.Circle((stred_x, stred_y), radius, fill=False, color='blue', linestyle='--')
ax.add_artist(kruznice)
ax.scatter(x_body, y_body, color=color, s=80, zorder=3)
ax.axhline(stred_y, color='gray', linewidth=0.8, linestyle=':')
ax.axvline(stred_x, color='gray', linewidth=0.8, linestyle=':')
ax.set_xlabel(f"X [{jdntka}]")
ax.set_ylabel(f"Y [{jdntka}]")
ax.set_xticks(np.arange(stred_x - radius*1.5, stred_x + radius*1.6, radius/2))
ax.set_yticks(np.arange(stred_y - radius*1.5, stred_y + radius*1.6, radius/2))
ax.set_aspect('equal', adjustable='datalim')
ax.grid(True, linestyle=':')

st.pyplot(fig)

# PDF export
from fpdf import FPDF
import io
import os

def export_pdf(stred_x, stred_y, radius, pocet_bodu, color, jdntka, fig):
    img_bytes = io.BytesIO()
    fig.savefig(img_bytes, format='PNG')
    img_bytes.seek(0)
    with open("temp_img.png", "wb") as f:
        f.write(img_bytes.read())
    img_bytes.seek(0)

    pdf = FPDF()
    pdf.add_page()
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    if not os.path.exists(font_path):
        font_path = "DejaVuSans.ttf"
    pdf.add_font("DejaVu", style="", fname=font_path, uni=True)
    pdf.set_font("DejaVu", size=12)
    pdf.ln(2)
    pdf.set_font("DejaVu", size=11)
    pdf.cell(0, 10, "O autorovi:", ln=True)
    pdf.cell(0, 10, "Jméno: Robin Čermák", ln=True)
    pdf.cell(0, 10, "Kruh: B1VS16", ln=True)
    pdf.cell(0, 10, "E-mail: 277729@vutbr.cz", ln=True)
    pdf.ln(2)
    pdf.cell(0, 10, "Použité technologie:", ln=True)
    pdf.cell(0, 10, "Python, Streamlit, Matplotlib, Copilot", ln=True)
    pdf.ln(5)
    pdf.set_font("DejaVu", size=12)
    pdf.cell(0, 10, "Parametry kružnice:", ln=True)
    pdf.cell(0, 10, f"Střed: ({stred_x}, {stred_y}) [{jdntka}]", ln=True)
    pdf.cell(0, 10, f"Poloměr: {radius} [{jdntka}]", ln=True)
    pdf.cell(0, 10, f"Počet bodů: {pocet_bodu}", ln=True)
    pdf.cell(0, 10, f"Barva bodů: {color}", ln=True)
    pdf.cell(0, 10, f"Jednotka: {jdntka}", ln=True)
    pdf.ln(5)
    pdf.image("temp_img.png", x=10, y=pdf.get_y(), w=pdf.w - 20)

    pdf_bytes = io.BytesIO()
    pdf.output(pdf_bytes)
    pdf_bytes.seek(0)

    os.remove("temp_img.png")
    return pdf_bytes

if st.button("Exportovat do PDF"):
    pdf_bytes = export_pdf(stred_x, stred_y, radius, pocet_bodu, color, jdntka, fig)
    st.download_button("Stáhnout PDF", pdf_bytes, file_name="body_na_kruznici.pdf")
