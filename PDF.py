from functions import *

class Pdf():
    def __init__(self, path) -> None:
        self.path = path
        self.name = path.split('/')[-1].split('.')[0]
        self.extension = path.split('.')[-1]
        self.pdf = PdfFileReader(path)
        self.npages = self.pdf.numPages
    
    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return self.path

if __name__ == '__main__':
    p1 = Pdf('exemplos_pdf/Cartilha Copevid Promotores.pdf')
    # p2 = Pdf('exemplos_pdf/PDF 1.pdf')
    # list_pdfs = [p1, p2]
    # merge_pdf(list_pdfs)
    # merged = Pdf('merged.pdf')
    compress_pdf([p1])
    # teste()