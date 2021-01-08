# ReadPdf
# By Murat Erenturk
import os
import logging as log
import datetime
import pandas as pd
import PyPDF2
import camelot

ToolName='ReadPdf'
ToolVersion='0.5.20201224.1'
LogFileName=ToolName+'.log'
Filename1='sample.pdf'
Filename2='sample2.pdf'

log.basicConfig(filename=LogFileName,filemode='w',format='%(asctime)s,%(levelname)s,%(message)s', level=log.INFO)
log.info(ToolName+","+ToolVersion)
utc_dt = datetime.datetime.now(datetime.timezone.utc) # UTC time
start=utc_dt.astimezone() # local time
log.debug('Started on '+str(start))
if os.path.exists(Filename1)==False:
    log.error(Filename1+" does not exist")
    exit(1)
log.debug('Reading file:'+Filename1)
pdfFileObj = open(Filename1, 'rb')  
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)  
pageObj = pdfReader.getPage(0)  
log.info(pageObj.extractText())  
pdfFileObj.close()

if os.path.exists(Filename2)==False:
    log.error(Filename2+" does not exist")
    exit(1)
log.debug('Reading file:'+Filename2)
tablelist=camelot.read_pdf(Filename2,pages='1',password=None,flavor='stream',suppress_stdout=False,
    layout_kwargs={})
log.info(str(tablelist[0].parsing_report))
df=tablelist[0].df
df.to_csv('extracted.csv')
print('Done')