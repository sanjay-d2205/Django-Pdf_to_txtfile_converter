from django.shortcuts import render
from PyPDF2 import PdfFileReader, PdfFileWriter
from django.http import HttpResponse
import io
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage

# Create your views here.
def index(request):
    showTextFile = 0
    return render(request,'base.html',{"showTextFile":showTextFile})

def textFileConverter(request):
    # txt = ''
    if request.method == 'POST':
        showTextFile = 1
        pdfFile = request.FILES['pdfFile']
        request.session['extractedText'] = extract_text_from_pdf(pdfFile)
        # pdf = PdfFileReader(pdfFile) 
        # for page_num in range(pdf.numPages):
        #     pageObj = pdf.getPage(page_num)
        #     txt = txt + pageObj.extractText()
        # request.session['extractedText'] = txt 
    return render(request,'base.html',{"showTextFile":showTextFile})

def export_text_file(request):
    file_data = request.session.get('extractedText')
    response = HttpResponse(file_data, content_type='application/text charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="content.txt"'
    return response

def extract_text_from_pdf(pdf_path):
    txt = ''
    pdfFileObj = pdf_path.read()
    pdfReader = io.BytesIO(pdfFileObj)
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    
    for page in PDFPage.get_pages(pdfReader, 
                                    caching=True,
                                    check_extractable=True):
        page_interpreter.process_page(page)
        
        text = fake_file_handle.getvalue()
    
    converter.close()
    fake_file_handle.close()
    
    if text:
        txt = text
    return txt