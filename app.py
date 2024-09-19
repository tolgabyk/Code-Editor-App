import subprocess
import autopep8
from fpdf import FPDF
from io import BytesIO
import streamlit as st

# Kodun diline göre formatlama fonksiyonu
def formatCode(code, language):
    if language == 'Python':
        return autopep8.fix_code(code)
    elif language == 'JavaScript':
        result = subprocess.run(['prettier', '--stdin-filepath', 'file.js'], input=code, text=True, capture_output=True)
        return result.stdout
    elif language == 'HTML/CSS':
        result = subprocess.run(['html-beautify'], input=code, text=True, capture_output=True)
        return result.stdout
    elif language == 'Java':
        result = subprocess.run(['google-java-format', '--stdin'], input=code, text=True, capture_output=True)
        return result.stdout
    elif language == 'C#':
        result = subprocess.run(['dotnet', 'format'], input=code, text=True, capture_output=True)
        return result.stdout
    else:
        return "This language is not supported"

# PDF oluşturma fonksiyonu 
def createPDF(code):
    pdf = FPDF()
    pdf.add_page()

    # Tam dosya yolunu belirleyin (örn: '/path/to/DejaVuSans.ttf')
    pdf.add_font('DejaVu', '', './dejavu-sans-ttf-2.37/ttf/DejaVuSans.ttf', uni=True)
    pdf.set_font("DejaVu", size=12)

    for line in code.split('\n'):
        pdf.cell(200, 10, txt=line, ln=True, align='L')
    
    output = BytesIO()
    pdf.output(output)
    output.seek(0)
    return output

# Streamlit Kullanıcı Arayüzü
st.title("Code Editor")

# Kullanıcıdan kod ve dil bilgisi alınması
codeInput = st.text_area("Copy Your Code:")
language = st.selectbox("Choose your language:", ['Python', 'JavaScript', 'HTML/CSS', 'Java', 'C#'])

# Formatla butonu
if st.button("Edit"):
    if codeInput:
        # Kodu formatla
        formattedCode = formatCode(codeInput, language)
        
        # Düzenlenmiş kodu göster
        st.subheader("Edited Code:")
        st.code(formattedCode, language=language.lower())

        # PDF oluştur
        pdfFile = createPDF(formattedCode)

        # PDF indirme butonu
        st.download_button(label="Download As PDF", data=pdfFile, file_name="formatted_code.pdf", mime="application/pdf")
    else:
        st.warning("Please copy your code!")
