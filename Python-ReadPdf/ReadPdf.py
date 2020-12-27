# ReadPdf
# By Murat Erenturk
import logging as log
import datetime
import PyPDF2   

ToolName='ReadPdf'
ToolVersion='0.5.20201224.1'
LogFileName=ToolName+'.log'
log.basicConfig(filename=LogFileName,filemode='w',format='%(asctime)s,%(levelname)s,%(message)s', level=log.INFO)
log.info(ToolName+","+ToolVersion)
utc_dt = datetime.datetime.now(datetime.timezone.utc) # UTC time
start=utc_dt.astimezone() # local time
log.debug('Started on '+str(start))
pdfFileObj = open('sample.pdf', 'rb')  
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)  
pageObj = pdfReader.getPage(0)  
log.info(pageObj.extractText())  
pdfFileObj.close()  
print('Done')