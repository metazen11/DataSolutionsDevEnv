import sys
import json
import os
import subprocess
from boto3.session import Session
import boto3
import zipfile

print('hello world')
ACCESS_KEY = 'AKIAQXX6JN6WOPENWSN6'
SECRET_KEY = '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'
BUCKET = 'datajobs'
    
#location where glue Stores its downloaded files
target = os.getcwd()+'/tmp'
os.mkdir(target)
print(target)

#job name is the name that talend uses internally and will create a sub folder in the zip package you will need to reference
#job_name = event['job_name']
job_name = 'ETL_Rics_InventoryOnHand_to_NS'
    
#file name is the actual filename that needs to be retrieved from S3 bucket
file_name = 'ETL_Rics_InventoryOnHand_to_NS_0.2'
#we send in a job_filename without the .zip so just adding that in
job_file_name = file_name+".zip" #jobname is a zip filename.   
print(job_file_name)
print(job_name)
#use the python aws api to get the file
s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY , aws_secret_access_key=SECRET_KEY)
s3.download_file(BUCKET,job_file_name, target+'/'+job_file_name)


# Get the list of all files and directories to see if file is there
path = os.path.abspath(os.getcwd())
dir_list = os.listdir(path)
print("Files and directories in '", path, "' :") 
print(dir_list)

print('trying to unzip file...')
#unzip file
with zipfile.ZipFile(target+'/'+job_file_name, 'r') as zipObj:
   # Extract all the contents of zip file in current directory
   zipObj.extractall(target)
jobpath = target+'/'+job_name
#current path
dir_list = os.listdir(os.getcwd())
print("Files and directories in '", os.getcwd(), "' :") 
print(dir_list)

#job path
dir_list = os.listdir(jobpath)
print("Files and directories in '", jobpath, "' :") 
print(dir_list)
job_exec = target+'/'+job_name+'/'+job_name+'_run.sh'
jar_file = target+'/'+job_name+'/etl_rics_inventoryonhand_to_ns_0_2.jar'
os.chmod(job_exec , 0o777)
os.chmod(jar_file , 0o777)

#update permissions
print('Updating permissions...')
cmd = ['chmod -R +x '+target+'/'] #
print(cmd)
p = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)
for line in p.stdout:
    print(line)
#p.wait()
print('permissions should be updated')
cmd = 'sudo yum install bash'
p = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)

print(job_exec)
cmd = '.' + job_exec #
print(cmd)
p = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)
for line in p.stdout:
    print(line)
#p.wait()
print(p.returncode)
print(job_exec)

#try a jar file?
#cmd = jar_file #
#print(cmd)
#p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
#for line in p.stdout:
#    print(line)
#p.wait()
#print(p.returncode)

#rc = os.system("sh "+job_exec)
print(rc)
print('Job Completed!')
