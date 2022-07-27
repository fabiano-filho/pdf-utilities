import os, shutil
from time import sleep
from functions import *
from PyPDF2 import PdfFileWriter, PdfFileMerger, PdfFileReader
from PDF import Pdf
import subprocess
import math
from multiprocessing import Process

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

def execute_compression(inputpdfs, path_output: str = '.\\compressed') -> None:
    for inputpdf in inputpdfs:
        name_arq = inputpdf.split("\\")[-1]
        if not os.path.exists('compressed'):
            os.makedirs('compressed')
        subprocess.call([
            'python', 'pdf_compressor.py','-o',
            f'{os.path.join(path_output, name_arq.split(".")[0] + "compressed.pdf")}', '-c', '3',
            f'{inputpdf}'
        ])

sep_pdf(pdfReader, 10)
# shutil.rmtree('temp')

# for item in os.listdir('temp'):
#     execute_compression(f'.\\temp\\{item}')

# list_pdfs = []
# for item in os.listdir('compressed'):
#     pdf = Pdf('.\\compressed\\' + item)
#     list_pdfs.append(pdf)
# merge_pdf(list_pdfs)
# shutil.rmtree('compressed')


lista = os.listdir('temp')
def listasMenores(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
    return lst

n = math.ceil(len(lista)/3)
listasDivididas = list(listasMenores(lista, n))
# print(listasDivididas)

lista_process_1 = [i for i in listasDivididas[0]]
lista_process_2 = [i for i in listasDivididas[1]]
lista_process_3 = [i for i in listasDivididas[2]]

# p1 = Process(target=execute_compression, args=(lista_process_1,))
# p2 = Process(target=execute_compression, args=(lista_process_2,))
# p3 = Process(target=execute_compression, args=(lista_process_3,))

# p1.start()
# p2.start()
# p3.start()

execute_compression(lista_process_1)
execute_compression(lista_process_2)
execute_compression(lista_process_3)

list_pdfs = []
for item in os.listdir('compressed'):
    pdf = Pdf('.\\compressed\\' + item)
    list_pdfs.append(pdf)
merge_pdf(list_pdfs)
shutil.rmtree('compressed')