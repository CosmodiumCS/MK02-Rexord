# MK02-Rexord

## [!!] DISCLAIMER
Though this binary is written in Python, it still has malicious capabilities. Do not run on systems that you do not have permission to use.

## Overview:
Rexord is a proof of concept RAT built off the Discord API. It is the first iteration of the hive mind malware (mk02, mk04, mk07). It was written in Python as a proof of concept after i accidentally discovered botnet capabilities within the Discord API. It is now archived and was never meant to become a serious malware, as I do not believe Python is a sufficient enough language to used for malware. 

## Resources:
- [YouTube Video](https://www.youtube.com/watch?v=xowncNKUziA)
- [YouTube Channel](https://youtube.com/cosmodiumcs)
- [Website](https://cosmodiumcs.com)

## Requirements:
- Python 3.x
- Windows 10 Target
- Discord Server

## Installation:
1. clone repository
```bash
git clone https://github.com/CosmodiumCS/MK02-Rexord
cd MK02-Rexord
```
2. install the requirements
```bash
pip install -r requirements.txt

# install these libraries if on linux
# sudo apt-get install libportaudio2 python3-tk
```
3. add your information to the `.env` file
```
TOKEN=YOUR_TOKEN_HERE
channel_id=CHANNEL_ID_HERE
channel_name=CHANNEL_NAME_HERE
```
4. run the binary
```bash
python3 rexord.py
```

## Features:
**[+] Getting Started:**
 - `hello` - see connected targets
 - `select <target>` - connect to specified target ['all' by default]

**[+] General:**
 - `help` - displays this menu
 - `upload <attachment>` - upload file(s) to target
 - `download <filename>` - download file(s) [list multiple with ","] 
 - `shutdown` - shuts down target
 - `restart` - restarts target
 - `exit` - exits target [can't reconnect]
 - `killswitch` - uninstalls from target
 
**[+] Payloads:**
 - `start keylogger` - starts live keylogger
 - `stop keylogger` - stops live keylogger
 - `webcam` - take picture through target webcam
 - `screenshot` - screenshot target computer
 - `record player <seconds>` - record audio from target 
 - `wifi creds` - gets wifi credentials
 - `web creds` - gets web credentials

**[+] System:**
 - `persist` - executes persistence on target
 - `$<command>` - execute system command on target
 - `private` - get private ip address
 - `public` - get public ip address
 - `os` - show os

## Extraneous:
Again, this was designed as a proof of concept, and not a legitimate malware. However, you can compile this binary using tools like Pyinstaller, Nuitka, and Py2Exe.
