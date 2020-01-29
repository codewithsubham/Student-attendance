import socket
import os.path
import requests
import sys
import time
import asyncio
#asdas
#server for connectivity check 
REMOTE_SERVER = "www.google.com"

#Directories CONST variables for files
TRASACTIONS_FILE_PATH = "Transactions/text.csv"
BUFFER_FILE_PATH = "Buffer/text.csv"
#Directories CONST variables
BUFFER_FOLDER_PATH = "Buffer/"
TRANSACTION_FOLDER_PATH = "Transactions/"
ASSEST_FOLDER_PATH = "Assest/"

#API'S URL
#TRANSACTIONS_API = 'http://visionitlabs.com/studentAttendence/api/v1/transaction/index.php'
TRANSACTIONS_API = "http://localhost/studentAttendence/api/v1/transaction/index1.php"
IDS_API =  "http://visionitlabs.com/studentAttendence/api/v2/allowedCards/"
STUDENT_IDS = []
DEVICE_ID = 123123123


##  FILE SYSTEM FUNCSTIONS
# check connect
def is_connected(hostname):
  try:
    host = socket.gethostbyname(hostname)
    s = socket.create_connection((host, 80))
    s.close()
    return True
  except:
     pass
  return False

#Check file is available or not
#Creates the directory if directory is not present
#needs directory path
def check_directory(directory_path):
    #open transaction file 
      if not os.path.exists(directory_path):
        # print('folder does not exits')
        # create a file 
        # os.makedirs return true if there is was error while creating file
        try:
          if not os.makedirs(directory_path):
            return True
        except:
            print('error while creating Transaction directory')
            return False
      else:
        return True
   

  

def create_tranactions_file():
  try:
       f = open(TRASACTIONS_FILE_PATH , "w")
       f.write('cardId , timestamp , flag')
       return True
  except:
      print("file was not created")
      return False


#recursive function to check same named file is present or not
#if present give it a new name
def checkfile_before_moving(new_file_name , status , i=0):
    if not status:
       if new_file_name in os.listdir(BUFFER_FOLDER_PATH):
          new_file_name = f'text_{i}.csv'
          print(new_file_name)
          return checkfile_before_moving(new_file_name , False , i+1)
       else:
         # checkfile_before_moving(new_file_name , True , 1)
          return f'{BUFFER_FOLDER_PATH}/{new_file_name}'
          
       
def move_file(input_file , output_file):
    """
      Before moving file
      checking is there any file left in buffer foder
      then rename file by incrementing 1 to total number of folder
     """
    number_of_files = os.listdir(BUFFER_FOLDER_PATH)
    #print(output_file.split('/')[1])
    if len(number_of_files) >= 1:
       output_file = f'{output_file.split(".")[0]}_{len(number_of_files)+1}.csv' 
    #output_file = checkfile_before_moving(output_file.split('/')[1], False , 1)
    try: 
        os.rename(input_file, output_file)
        create_tranactions_file()
        return True
    except:
        return False

def Clean_folder(path):
  remove_status = False
  try:
    if len(os.listdir(path)) > 0:
      for files in os.listdir(path):
          if os.remove(path+files):
            remove_status = False
          else:
            remove_status = True
    else:
      print("file was not present")
      remove_status = True
  except:
    remove_status = False
    print("malformed path")    
  return remove_status   

def create_ids_file(students_id):
    Status = False  
    print(students_id)
    Student_id_list = students_id.split("#")
    print(Student_id_list.pop(0))
    for target_list in Student_id_list:
        try:
          open(ASSEST_FOLDER_PATH+target_list , "w+")
          Status  = True
        except:
          Status = False  
    return Status  
    
def Valid_student_id(student_id):
  if student_id in os.listdir(ASSEST_FOLDER_PATH):
    return True
  else:
    return False

def write_transactions(file ,  cardId , timestamp , flag):
  try:
    f = open(file , "a")
    f.write(f'\n{cardId} , {timestamp} , {flag}')
    print("file written")
    return True
  except:
    print("unable to write file")
    return False  

def  httpcall_transaction(transactions_data , entries, username , password):
    status = False
    file={'fileToUpload':transactions_data}
    body={"username":username , 'password':password , 'deviceid':DEVICE_ID}
    try:
      r = requests.post(TRANSACTIONS_API , files=file , data=body)
      print(r.text)
      if r.status_code is 201 and r.text is '1':
        status = True   
      else:
        return False  
    except:
      status =  False;
  
    return status


def httpcall_getids():
    device_id = open('id.ini' , 'r')
    try:
      r = requests.post(IDS_API , params={'deviceId':device_id})
      if r.status_code is 200:
         return r.text
      else:
        return False   
    except:
      return False  

async def push_transaction():
  status = True
  while(status):
    file = os.listdir(BUFFER_FOLDER_PATH)
    if len(file) > 0:
      transactions_data = open(BUFFER_FOLDER_PATH+file[0] , "rb")
      transactions_entries = len(open(BUFFER_FOLDER_PATH+file[0], 'r').read().split('\n'))
      if not httpcall_transaction(transactions_data , transactions_entries-1 , 'admin' , 'Asd@12345'):
        print('file being not uploaded')
        await asyncio.sleep(5)
      else:
        os.remove(BUFFER_FOLDER_PATH+file[0])

    else:
      print('no file to upload')
      status = False
  return True    




async def sync():
  while True:
     await asyncio.sleep(2) # in Seconds
     print('asd')
    # empty all students id
     if Clean_folder(ASSEST_FOLDER_PATH):
       ids = httpcall_getids()
       print(ids)
       if create_ids_file(ids):
          time.sleep(2)
          print('sync was success')
       else:
         print('sync was not success')      
     else:
       print('folder was unclear')  
  # check ids is present or not
    
    
   
async def transaction_sync():
    while True:
      await asyncio.sleep(4) # in seconds
      if move_file(TRASACTIONS_FILE_PATH , BUFFER_FILE_PATH):
        time.sleep(2)
        await push_transaction()
      else:
          print('unable to move transaction uppload failed')

    



#while boot
print(check_directory(TRANSACTION_FOLDER_PATH))
print(check_directory(BUFFER_FOLDER_PATH))
print(check_directory(ASSEST_FOLDER_PATH))
print(create_tranactions_file())

#get ids

ids = httpcall_getids()
print(create_ids_file(ids))

time.sleep(5)

# sync function call 
loop = asyncio.get_event_loop()
cors = asyncio.wait([sync() , transaction_sync()])
loop.run_until_complete(cors)
