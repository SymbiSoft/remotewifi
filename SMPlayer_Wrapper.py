'''
Target application file
Define a commom interface to RemoteWifi

SendTarget(command,arg)

'''
import subprocess
import os

TARGET_PROCESS_NAME = "smplayer.exe"
TARGET_PROCESS_PATH = "I:\Arquivos de programas\SMPlayer"

def SendTarget(command,arg=" "):
    if   command == 'open':
        cmline = os.path.join(TARGET_PROCESS_PATH,TARGET_PROCESS_NAME)
        p = subprocess.Popen(cmline + " " + arg)        
    elif command == 'play':
        cmline = os.path.join(TARGET_PROCESS_PATH,TARGET_PROCESS_NAME)
        p = subprocess.Popen(cmline + " -send-action play")
    elif command == 'pause':
        cmline = os.path.join(TARGET_PROCESS_PATH,TARGET_PROCESS_NAME)
        p = subprocess.Popen(cmline + " -send-action pause")
    elif command == 'stop':
        cmline = os.path.join(TARGET_PROCESS_PATH,TARGET_PROCESS_NAME)
        p = subprocess.Popen(cmline + " -send-action stop")
    elif command == 'fullscreen':
        cmline = os.path.join(TARGET_PROCESS_PATH,TARGET_PROCESS_NAME)
        p = subprocess.Popen(cmline + " -send-action fullscreen")        
        
