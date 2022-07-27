import os 
from functions import *
from PyPDF2 import PdfFileWriter, PdfFileMerger, PdfFileReader
from PDF import Pdf

pdfFileObj = open('exemplos_pdf\\Cartilha Copevid Promotores.pdf', 'rb') 
pdfReader = PdfFileReader(pdfFileObj) 
n = pdfReader.numPages

def sep_pdf(inputpdf, limite: int) -> None:
    num_pages = inputpdf.numPages
    for i in range(0, num_pages, limite):
        initial = i
        output = PdfFileWriter()

        for j in range(i, i + limite):
            if j == num_pages:
                break
            else:
                output.addPage(inputpdf.getPage(j))
                final = j

        # Cria pasta temp se n existir
        if not os.path.exists('temp'):
            os.makedirs('temp')
                
        with open(".\\temp\\document-page{}-{}.pdf".format(initial, final), "wb") as outputStream:
            output.write(outputStream)
        

sep_pdf(pdfReader, 10)
list_pdfs = []
for item in os.listdir('temp'):
    pdf = Pdf('.\\temp\\' + item)
    list_pdfs.append(pdf)
merge_pdf(list_pdfs)