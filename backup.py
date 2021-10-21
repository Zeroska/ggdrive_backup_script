import os 
import shutil
import sys
import time
import schedule
import argparse
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




# This kinda useleses to be honest
def download_backup_from_ggdrive(drive):
    # Get All file in root folder
    f = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    for file1 in f:
      print('title: %s, id: %s' % (file1['title'], file1['id']))
      # For each file backup and download to local machine and store it in folder you specify
      

def controller():
    path, archive_location = get_user_input()

    now = datetime.now()
    # You could change file name here
    file_name = "backup " + now.strftime(r"%d/%m/%Y %H:%M:%S").replace('/', '-')

    if  not create_zip(path, file_name):
        sys.exit(0)
    auth, drive = google_auth()

    # TODO: Create option to choose between upload and download 
    upload_backup(drive,archive_location , file_name+'.zip')
    print("[*] Upload backup successfully - File name: " + file_name +'.zip') 

def get_user_input():
    parser = argparse.ArgumentParser()
    parser.add_argument('Path', metavar='path',type=str,help='path to the file you want to archive')
    parser.add_argument('Archive', metavar='archive', type=str, help='path to archive file you will store')
    args = parser.parse_args()

    input_path = args.Path
    input_path_archive = args.Archive

    if not os.path.isdir(input_path):
        print('the path specified does not exist')
        sys.exit()
    elif not os.path.isdir(input_path_archive):
        print('the archive path specified does not exist')
        sys.exit()
    
    return input_path, input_path_archive


if __name__=="__main__":

    print("Zeroska - GG Backup Script")
    controller()




