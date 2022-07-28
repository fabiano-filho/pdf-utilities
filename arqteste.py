import multiprocessing
import os, shutil
from time import sleep, time
from functions import *
from PyPDF2 import PdfFileWriter, PdfFileReader
from PDF import Pdf
import subprocess
import math
from multiprocessing import Process

def sep_pdf(inputpdf: PdfFileReader, limite: int) -> None:
    num_pages = inputpdf.numPages
    if limite > num_pages:
        n = 3 if num_pages > 3 else 1
        limite = math.ceil(num_pages / n)
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

def execute_compression(inputpdfs:list, path_output: str = '.\\compressed') -> None:
    """" Recebe um lista de pdfs e comprime cada um deles utilizando o ghostscript """
    for inputpdf in inputpdfs:
        name_arq = inputpdf.split("\\")[-1]
        if not os.path.exists('compressed'):
            os.makedirs('compressed')
        subprocess.call([
            'python', 'pdf_compressor.py','-o',
            f'{os.path.join(path_output, name_arq.split(".")[0] + "compressed.pdf")}', '-c', '3',
            f'{inputpdf}'
        ])

def listasMenores(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
    return lst

if __name__ == '__main__':
    pdfFileObj = open('exemplos_pdf\\Cartilha Copevid Promotores.pdf', 'rb') 
    pdfReader = PdfFileReader(pdfFileObj) 
    sep_pdf(pdfReader, 15)
    lista = list(map(lambda x: ".\\temp\\" + x, os.listdir('temp')))

    n = math.ceil(len(lista) / 3)
    listasDivididas = list(listasMenores(lista, n))

    processos = []
    time_start = time()
    for item in listasDivididas:
        p = Process(target=execute_compression, args=(item,))
        p.start()
        processos.append(p)

    for p in processos:
        p.join()

    time_end = time()
    print(f'Tempo de execução: {time_end - time_start}')
 
    list_pdfs = []
    for item in os.listdir('compressed'):
        pdf = Pdf('.\\compressed\\' + item)
        list_pdfs.append(pdf)
    merge_pdf(list_pdfs)
    shutil.rmtree('compressed')
    shutil.rmtree('temp')