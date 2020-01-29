import urllib.request
update_path = "http://localhost/firmware/"
install_path = "/Users/subham/python/studentAttendance/local/"

update_file_list = ["main_loop.py", "sync.py"]


def check_remote_update(filename):
    file_url = update_path + filename
    res = urllib.request.urlopen(file_url)
    data = res.readline()
    
    # print the version number e.g 1.0.0
    version_number = data.decode('utf-8').strip().split(' ')[1]
    return  version_number

def check_local_update(filename):
    # check file version from local device
    res = open(install_path+filename , 'r')
    version_number = res.readline().strip().split(' ')[1]
    return version_number


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







for filename in update_file_list:
    try:
      #  log("Checking updates for " + filename)
        
        print(check_remote_update(filename))
        print(check_local_update(filename))
        
        print(difference(check_remote_update(filename) , check_local_update(filename)))
        
    except:
        log("Error updating " + filename)
    else:
        log("Update complete")
    finally:
        log("Exiting")




