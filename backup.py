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


def google_auth():
    print("[*] Authenticating")
    gauth = GoogleAuth()

    gauth.LoadCredentialsFile("mycreds.txt")
    if gauth.credentials is None:
        print("[*] Credentials Files is None")
        gauth.LocalWebserverAuth() 
    elif gauth.access_token_expired:
        print("[*] Refresh Token")
        gauth.Refresh()
    else:
        print("[*] Authorize")
        gauth.Authorize()
    gauth.SaveCredentialsFile("mycreds.txt")
    drive = GoogleDrive(gauth) 
    return gauth, drive


def upload_backup(drive, path, file_name):
    f = drive.CreateFile({'title': file_name}) 
    f.SetContentFile(os.path.join(path, file_name)) 
    f.Upload() 
    f = None



def download_backup_from_ggdrive(drive):
    # Get All file in root folder
    f = drive.ListFile({'q': "'root' in parents  and trashed=false"}).GetList()
    for file1 in f:
      print('title: %s, id: %s' % (file1['title'], file1['id']))
      # For each file backup and download to local machine and store it in folder you specify


def controller():
    a,b = get_user_input()
    print(a)
    print(b)
    path = r"/Users/zeroska/Works/GDSC/AutoBackUpGoogleDrive/ImportantFolderTest/"
    now = datetime.now()
    file_name = "backup " + now.strftime(r"%d/%m/%Y %H:%M:%S").replace('/', '-')

    if  not create_zip(path, file_name):
        sys.exit(0)
    auth, drive = google_auth()
    # TODO: Create option to choose between upload and download 


    download_backup_from_ggdrive(drive)
    #upload_backup(drive, r"/Users/zeroska/Works/GDSC/AutoBackUpGoogleDrive/archive", file_name+'.zip')

def get_user_input():
    path = sys.argv[1] 
    archive_store_location = sys.argv[2]
    if os.path.exists(path) and os.path.exist(archive_store_location):
        return path, archive_store_location 


if __name__=="__main__":

    print("[*] backing up")
    controller()




