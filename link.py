# Resources
# https://pythonhosted.org/PyPDF2/PdfFileWriter.html
# https://www.adobe.com/content/dam/acom/en/devnet/pdf/pdfs/pdf_reference_archives/PDFReference.pdf

from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.generic import RectangleObject
from os import path
import fitz

pdf_writer = PdfFileWriter()
pdf_reader = PdfFileReader(open('Starter10_Blue.pdf', 'rb'))
# pdf_reader = PdfFileReader(open('Starter9.pdf', 'rb'))
# pdf_reader = PdfFileReader('Starter9_Blue.pdf')

### READ IN PDF
doc = fitz.open("SCOTTSDALE_ZAHNER_100CD_SET_V3.pdf")


# get page dimensions
x1, y1, x2, y2 = pdf_reader.getPage(0).mediaBox
print(f'x1, x2: {x1, x2}\ny1, y2: {y1,y2}')



print("page text")
for page in doc:
    ### SEARCH
    text = "DET Z100"
    text_instances = page.search_for(text)
    if (len(text_instances) > 1):
        print (text_instances)
        pdf_writer.addLink(
            pagenum=0,  # index of the page on which to place the link
            pagedest=1,  # index of the page to which the link should go
            # clickable area x1, y1, x2, y2 (starts bottom left corner)
            rect=RectangleObject([(text_instances.x0), (y2-text_instances.y0), (text_instances.x1), (y2-text_instances.y1)]),
            # border
            # fit

)
    # print (page.get_text())
    
    # print (page.get_text("xml"))


# get text
# pageText = pdf_reader.getPage(1).extractText()
# pageText = pdf_reader.pages[0].extractText()
# pageText = pdf_reader.getFormTextFields()
# pageText = pdf_reader.getFields()
# pageText = pdf_reader.getPage(1).getContents()
# print("page text", pageText.getObject())

# for page in pdf_reader.pages:
#     if "/Annots" in page:
#         print("annots")
#         for annot in page["/Annots"]:
#             subtype = annot.getObject()["/Subtype"]
#             if subtype == "/Text":
#                 print(annot.getObject()["/Contents"])



# add each page in pdf to pdf writer
num_of_pages = pdf_reader.getNumPages()

for page in range(num_of_pages):
    current_page = pdf_reader.getPage(page)
    pdf_writer.addPage(current_page)
print(f'{(770), (y2-104), (800), (y2-130)}')
# Add Link
pdf_writer.addLink(
    pagenum=0,  # index of the page on which to place the link
    pagedest=1,  # index of the page to which the link should go
    # clickable area x1, y1, x2, y2 (starts bottom left corner)
    rect=RectangleObject([(570), (y2-550), (650), (y2-600)]),
    # border
    # fit

)

with open(path.abspath('pdf_with_link.pdf'), 'wb') as link_pdf:
    pdf_writer.write(link_pdf)
