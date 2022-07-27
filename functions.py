from PyPDF2 import PdfFileWriter, PdfFileMerger, PdfFileReader
import os

def merge_pdf(pdf_files: list) -> None:
    """ Merge all pdfs in a list """
    merger = PdfFileMerger()
    name_new_file = ''
    for pdf in pdf_files:
        merger.append(pdf.path)
        name_new_file += pdf.name + '_'
    if not os.path.exists('merged'):
            os.makedirs('merged')
    merger.write('.\\merged\\merged.pdf')
    merger.close()


def compress_pdf(pdf_files) -> None:
    """ Compress a pdf file """
    writer = PdfFileWriter()  
    name_new_file = '' 
    for pdf in pdf_files:
        reader = PdfFileReader(pdf.path)
        name_new_file += pdf.name + '_'
        for page in reader.pages:
            if '/Annots' in page:
                del page['/Annots']
            page.compress_content_streams()
            writer.addPage(page)
        
    with open(f'.\\compressed\\{name_new_file}compressed.pdf', 'wb') as f:
        writer.write(f)
    

