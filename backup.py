import os 
import shutil
import sys
import time
import schedule
from datetime import datetime

from pydrive.drive import GoogleDrive 
from pydrive.auth import GoogleAuth 

def create_zip(path, file_name):
    try:
        shutil.make_archive(f"archive/{file_name}", 'zip', path)
        return True
    except FileNotFoundError as e:
        print(e)
        return False


# cho nay dung de authen 
def google_auth():
    print("Authening")
    gauth = GoogleAuth() 
    gauth.LoadCredentialsFile("mycreds.txt")
    if gauth.credentials is None:
        print("Credentials is None")
        gauth.LocalWebserverAuth()        
    elif gauth.access_token_expired:
        print("Refresh Token")
        gauth.Refresh()
    else:
        print("Authorize")
        gauth.Authorize()
    gauth.SaveCredentialsFile("mycreds.txt")
    drive = GoogleDrive(gauth) 
    return gauth, drive

# tao file voi ten dc truyen vao
def upload_backup(drive, path, file_name):
    f = drive.CreateFile({'title': file_name}) 
    f.SetContentFile(os.path.join(path, file_name)) 
    f.Upload() 
    f = None



def download_backup_from_ggdrive(drive, path, filename):
    # Get All file in root folder
    f = drive.ListFile({'q': "'root' in parent and trashed=false"}).getList()
    for file1 in f:
      printf('title: %s, id: %s' % (file1['title'], file1['id']))
      # For each file backup and download to local machine and store it in 


def controller():
    path = r"/Users/zeroska/Works/GDSC/AutoBackUpGoogleDrive/ImportantFolderTest/"
    now = datetime.now()
    file_name = "backup " + now.strftime(r"%d/%m/%Y %H:%M:%S").replace('/', '-')

    if  not create_zip(path, file_name):
        sys.exit(0)
    auth, drive = google_auth()
    upload_backup(drive, r"/Users/zeroska/Works/GDSC/AutoBackUpGoogleDrive/archive", file_name+'.zip')

def take_user_input():
    

if __name__=="__main__":
    # schedule.every().day.at("00:00").do(controller)
    # while True:
    #    schedule.run_pending()`
    print("[*] backing up")
    controller()




