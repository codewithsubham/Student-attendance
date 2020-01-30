import urllib.request
import os 
update_path = "http://visionitlabs.com/firmware/"
install_path = os.getcwd()

update_file_list = ["main_loop.py", "sync.py"]


#constant
PWD = os.getcwd()
ARCHIVE_LOCATION = PWD+'/archive'

print(PWD)


#asdad
def check_remote_version(filename):
    file_url = update_path + filename
    res = urllib.request.urlopen(file_url)
    data = res.readline()
    
    # print the version number e.g 1.0.0
    version_number = data.decode('utf-8').strip().split(' ')[1]
    return  version_number

def check_local_version(filename):
    # check file version from local device
    res = open(install_path+'/'+filename , 'r')
    version_number = res.readline().strip().split(' ')[1]
    return version_number

def download_remote_file(filename):
    file_url = update_path + filename
    res = urllib.request.urlopen(file_url)
    data = res.read()
    print(data.decode('utf-8'))
    script = open(filename , "w+")
    script.write(data.decode('utf-8'))
    
    
def log(message):
    print(message)
    return


def difference(remote_version , local_version):
    f1 = remote_version 
    f2 = local_version

    if f1.split('.')[0] > f2.split('.')[0]:
        log('major is updated')
        return True;
    elif f1.split('.')[0] < f2.split('.')[0]:
        log('major is outdated')
        return False
    elif f1.split('.')[1] > f2.split('.')[1]:
        log('minor is changed')
        return True
    elif f1.split('.')[1] < f2.split('.')[1]:
        log('minor is outdated')
        return False
    elif f1.split('.')[2] > f2.split('.')[2]:
        log('revison is changed')
        return True
    elif f1.split('.')[2] < f2.split('.')[2]:
        log('revision is outdated')
        return False
    else:
        print("version same")
        return False



def check_directory(directory_path):
      if not os.path.exists(directory_path):
        try:
          if not os.makedirs(directory_path):
            return True
            #logs(f"{directory_path} was created" , MAIN_FILE_LOG_PATH)
            return True
        except:
            #logs(f"{directory_path} was created" ,MAIN_FILE_LOG_PATH)
            logs('error while creating Transaction directory')
            return False
      else:
        return True

def move_file(input_file , output_file):
    try:
        os.rename(input_file, output_file)
        return True
    except:
        return False
    finally:
        return True
 

for filename in update_file_list:
    try:
      #  log("Checking updates for " + filename)
        
        log(check_remote_version(filename))
        log(check_local_version(filename))
        need_to_update = difference(check_remote_version(filename) , check_local_version(filename))
        if need_to_update:
            print('update is required updating')    
            check_directory(ARCHIVE_LOCATION)
            log(move_file(f'{PWD}/{filename}' , f'{ARCHIVE_LOCATION}/{filename}'))
            download_remote_file(filename)  
    except:
        log("Error updating " + filename)
    else:
        log("Update complete")
    finally:
        log("Exiting")



