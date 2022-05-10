# Resources
# https://pythonhosted.org/PyPDF2/PdfFileWriter.html
# https://www.adobe.com/content/dam/acom/en/devnet/pdf/pdfs/pdf_reference_archives/PDFReference.pdf

from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.generic import RectangleObject
from os import path
import fitz 
import json
from spellchecker import SpellChecker

import csv

pdfLink = r"SCOTTSDALE_ZAHNER_100CD_SET_V3.pdf"

# ------- using fitz to read the text and search through to find items
# ------- PDFwriter to writ stuff

pdf_writer = PdfFileWriter()
pdf_reader = PdfFileReader(open(pdfLink, 'rb'))
# pdf_reader = PdfFileReader(open('Starter9.pdf', 'rb'))
# pdf_reader = PdfFileReader('Starter9_Blue.pdf')

### READ IN PDF
doc = fitz.open(pdfLink)


# get page dimensions
x1, y1, x2, y2 = pdf_reader.getPage(0).mediaBox
print(f'x1, x2: {x1, x2}\ny1, y2: {y1,y2}')


print("page count is {0}".format(doc.page_count))
print("page entity is ", doc)

SearchText = ['XC-A501','XC-A502','XC-A503','XC-A504','XC-A505', 'XC-D501', 'XC-D502']
callouts = []
details = []

def misspelledWords ():
    textList = page.get_text('text').split('\n')

def foundDetail (page, searchTxt):
    
    # find each word in the detail list and get its rect. 
    # need to exlude detail pages
    rect = []
    width = page.rect.width - 300
    height = page.rect.height - 200
    
    wlist = page.get_text("words")  # make the word list
    for w in wlist:  # scan through all words on page
        if searchTxt in w[4]:  # w[4] is the word's string
            if (w[0] < width and w[1] < height):
                print ('found')
                r = fitz.Rect(w[:4])  # make rect from word bbox
                rect.append(r)
                print (w)
                # page.add_underline_annot(r)  # underline
    
    return page.number, rect


def getDetailPage(page, searchTxt):
    # print ('found page')
    # print ('found detail on page')
    # find page that detail links to on it
    # assume lower right hand corner only
    # only one page per many detail
    width = page.rect.width - 300
    height = page.rect.height - 200
    rect = []
    pageNumber = -1

    wlist = page.get_text("words")  # make the word list
    for w in wlist:  # scan through all words on page
        if searchTxt in w[4]:  # w[4] is the word's string
            if (w[0] > width and w[1] > height):
                print ('found page')
                print (width, height, page.number )
                # r = fitz.Rect(w[:4])  # make rect from word bbox
                pageNumber = page.number
                # rect.append(r)
                # page.add_underline_annot(r)  # underline

    return pageNumber



def addLinkstoDetail():
    print ('links added')

def notFound():
    print ('details not found')



def writeCsv(pathToFile, header, data, encoding='UTF8', newline=''):
    # open the file in the write mode
    with open(pathToFile, 'w') as f:
        # create the csv writer
        writer = csv.writer(f)
        # write the header
        writer.writerow(header)

        # write multiple rows
        writer.writerows(data)


## -----------------------end functions -----------------------
detpageNumber= -1
detailRect = []
pages = []
detials = []
detailLinkOkj = {}

for detailName in SearchText:
    detailLinkOkj[detailName] = {'toPages':[], 'destPage':[]}
    # detailLinkOkj[detailName]['pages'] = []
    
print ('no idea', detailLinkOkj)
for page in doc:
    print('-----------page', page)
    
    for detailName in SearchText:
        
        # detpageNumber = getDetailPage(page, "XC-D501")
        detpageNumber = getDetailPage(page, detailName)
        
        if (detpageNumber != -1):
            pages.append(detpageNumber)
            detailLinkOkj[detailName]['toPages'].append(detpageNumber)

        # [pgNum, detailRect ]= foundDetail(page, "XC-D501")
        [pgNum, detailRect ]= foundDetail(page, detailName)

        if(len(detailRect)>0):
            detials.append({pgNum: detailRect})
            detailLinkOkj[detailName]['destPage'].append({pgNum: detailRect})
    
# print ('no idea', detailLinkOkj)
# print ( 'page report', pages, detials)
#----add links to pages

for eachDetailObj in detailLinkOkj:
    # print('eachDetailObj', eachDetailObj)
    # print('detailLinkOkj[eachDetailObj][pages]', detailLinkOkj[eachDetailObj]['pages'])
    for eachDestPage in detailLinkOkj[eachDetailObj]['toPages']:
        # print ('each', eachDestPage)
        for eachRect in detailLinkOkj[eachDetailObj]['destPage']:
            # print('eachRect',eachRect)
            # testKey = [k for k, v in each.items()]
            detailPage = list(eachRect.keys())[0]
            detailRect = list(eachRect.values())[0]
            # print('detailPage',detailRect)

            if (detailPage != pages[0]):
                # print('detailRect', detailRect)
                lnks = doc[detailPage].links()
                # print('links', lnks)

                for everyRect in detailRect:
                    pageToLink = doc[detailPage]
                    # print('pageToLink', pageToLink)
                    print ('about to link', eachDestPage, detailPage, everyRect)

                    # lnks = {'kind': 1, 'xref': 864, 'from': everyRect, 'type': 'goto', 'page': pages[0], 'to': fitz.Point(100.0, 200.0), 'zoom': 0.0}
                    lnks = {'kind': 1, 'xref': 864, 'from': everyRect, 'type': 'goto', 'page': eachDestPage, 'to': fitz.Point(100.0, 200.0), 'zoom': 0.5}
                    pageToLink.insert_link(lnks)
                    page = doc.reload_page(pageToLink)
        


# for each in detials:
#     # print ('each', each)
#     # testKey = [k for k, v in each.items()]
#     detailPage = list(each.keys())[0]
#     detailRect = list(each.values())[0]
#     # print('detailPage',detailPage)
#     if (detailPage != pages[0]):
#         # print('detailRect', detailRect)
#         lnks = doc[detailPage].links()
#         # print('links', lnks)

#         for everyRect in detailRect:
#             pageToLink = doc[detailPage]
#             # print('pageToLink', pageToLink)
#             # print ('about to link',detailPage, everyRect)

#             # lnks = {'kind': 1, 'xref': 864, 'from': everyRect, 'type': 'goto', 'page': pages[0], 'to': fitz.Point(100.0, 200.0), 'zoom': 0.0}
#             lnks = {'kind': 1, 'xref': 864, 'from': everyRect, 'type': 'goto', 'page': detailPage, 'to': fitz.Point(100.0, 200.0), 'zoom': 0.5}
#             pageToLink.insert_link(lnks)
#             page = doc.reload_page(pageToLink)
# # doc[2].doc[detpageNumber]

 
doc.ez_save('pdfLinks.pdf')


misspelledList = []
pageHeader = []

print("page text")
for page in doc:
# page = doc[0]
    ### SEARCH
    # print('-----------page', page)
    pageHeader.append(page)
    # textToCheck = page.get_text('text')
    # --- spell check---------------------------------------------------------------
    textListClean =[]
    new_string = []
    updateMisspelled = []
    textList = page.get_text('text').split('\n')
    for each in textList:
        # print (len(each))
        if (len(each) > 0):
            # print (each)
            splitText = each.split(' ')
            if(len(splitText)>1):
                for i in splitText:
                    textListClean.append(i)
            else:
                # print (len(splitText))
                textListClean.append(splitText[0])

    for stringy in textListClean:
        cleanstring = ''.join(char for char in stringy if char.isalnum())

        #remove exceptions 
        if len(cleanstring) > 1:
            new_string.append(''.join(char for char in stringy if char.isalnum()))

    spell = SpellChecker()
    misspelled = spell.unknown(new_string)

    misspelledList.append(misspelled)

    # print (misspelled)



writeCsv('report.csv', pageHeader, misspelledList )




    # --- linking---------------------------------------------------------------
    # --earlier pages link to later pages
    # -- can use input list of details

    # text options
    # print('text', page.get_text('text')) # gets words only
    # print('blocks', page.get_text('blocks')) # Yikes - too much, seems well contained but a mess
    # print('words', page.get_text('words')) # gets list of word and rect xy, xy
    #print('json', page.get_text('json')) # gets structured items with word and bbox xy, xy
    # print('xml', page.get_text('xml')) #formating only
    

    myJSON =  json.loads('{0}'.format(page.get_text('json')))
    # print(myJSON['lines'])
    # print(myJSON['blocks'])
    jsonData = myJSON['blocks']
    for x in jsonData:
            # keys = x.keys()
            # print(keys)
            # values = x.values()
            # print(values)
            if ('lines' in x.keys()):
                # print(x['lines'][0]['spans'][0]['text'])
                values = x['lines']
            
            # for ix in values:
            #     # print(ix)
            #     if type(ix) != int:
            #         if len(ix)>1:
            #             keysix = ix.keys()
            #             # print(keysix)
            #     # valuesix = ix.values()
            #     # print(valuesix)
    



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

# # add each page in pdf to pdf writer
# num_of_pages = pdf_reader.getNumPages()

# for page in range(num_of_pages):
#     current_page = pdf_reader.getPage(page)
#     pdf_writer.addPage(current_page)
# print(f'{(770), (y2-104), (800), (y2-130)}')
# # Add Link
# pdf_writer.addLink(
#     pagenum=0,  # index of the page on which to place the link
#     pagedest=1,  # index of the page to which the link should go
#     # clickable area x1, y1, x2, y2 (starts bottom left corner)
#     rect=RectangleObject([(570), (y2-550), (650), (y2-600)]),
#     # border
#     # fit

# )

# with open(path.abspath('pdf_with_link.pdf'), 'wb') as link_pdf:
#     pdf_writer.write(link_pdf)
