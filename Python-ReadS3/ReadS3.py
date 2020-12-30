# ReadS3
# By Murat Erenturk
import sys
import os
import logging as log
import datetime
import boto3
from botocore.exceptions import *
from botocore.errorfactory import *
import traceback

def ClientAPIErrorMessage(ObjectName,err):
    error_code = int(err['Error']['Code'])
    error_message = err['Error']['Message']
    switcher={
        403: "You dont have permissions on "+ObjectName+ " for this operation",
        404: ObjectName+" does not exist"
    }
    return switcher.get(error_code,str(error_code)+","+error_message)

def GetS3Bucket(ProfileName,BucketName):
    try:
        session=boto3.Session(profile_name=ProfileName)
        s3=session.resource('s3')
        s3.meta.client.head_bucket(Bucket=BucketName)
        log.debug("Bucket created")
        return s3.Bucket(BucketName)
    except ProfileNotFound as PNF:
        log.error(PNF.args[0])
        return None
    except ClientError as error:
        log.error(ClientAPIErrorMessage(BucketName,error.response))
        return None
    except:
        log.error(traceback.format_exc())
        return None

# This function returns:
# 0 if there is error
# 1 if object is a file
# 2 if object is a folder
def PathObjectType(Path):
    if len(Path)==0:
        return 0
    Folder=os.path.dirname(Path)
    Name=os.path.basename(Path)
    if (len(Name)>0):
        return 1
    if (len(Folder)>0 and len(Name)==0):
        return 2
    return 0 

def DownloadFile(BucketObj,Path):
    try:
        BucketName=BucketObj.name
        Folder=os.path.dirname(Path)
        Name=os.path.basename(Path)
        if len(Folder)>0:
            RemoteObjectName=Folder+'/'+Name
        else:
            RemoteObjectName=Name
        FileName=Name
        log.debug("Object:"+RemoteObjectName+","+FileName)
        BucketObj.download_file(RemoteObjectName,FileName)
        return True
    except ClientError as error:
        log.error(ClientAPIErrorMessage(BucketName+":"+Path,error.response))
        return False
    except:
        log.error(traceback.format_exc())   
        return False

ToolName='ReadS3'
ToolVersion='0.5.20201228.1'
LogFileName=ToolName+'.log'
log.basicConfig(filename=LogFileName,filemode='w',format='%(asctime)s,%(levelname)s,%(message)s', level=log.INFO)
log.info(ToolName+","+ToolVersion)
utc_dt = datetime.datetime.now(datetime.timezone.utc) # UTC time
start=utc_dt.astimezone() # local time
log.debug('Started on '+str(start))
ProfileName='s3reader'
BucketName='testshare31415'

#Connect To Bucket
s3Bckt=GetS3Bucket(ProfileName,BucketName)
if s3Bckt==None:
    print("Failed")
    sys.exit(0)

#List contents and download files
log.info("Contents of bucket "+BucketName)
for obj in s3Bckt.objects.all():
    Name=obj.key
    Size=str(obj.size)
    if PathObjectType(Name)==1:
        res=DownloadFile(s3Bckt,Name)
        if res:
            log.info("File:"+Name+","+Size+", downloaded")
        else:
            log.warning("File:"+Name+","+Size+",failed to download")
    elif PathObjectType(Name)==2:
        log.info("Folder:"+Name+","+Size)
    else:
        log.warning("Unknown object type "+Name)
print('Done')