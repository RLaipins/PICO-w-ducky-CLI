import argparse
import requests
from bs4 import BeautifulSoup
import os

url= "http://192.168.4.1:80/"

def get_scripts():
    try:
        resp = requests.get(f"{url}/ducky",timeout=5)
        if resp.status_code == 200:
            
            soup = BeautifulSoup(resp.text, 'html.parser')
            table = soup.find('table')
            print("Available scripts:")
            for enum,script in enumerate(table.findAll('td')[::2],start=1):
                print(f"-----: {enum}.   {script.text}")
        else:
            print(f"Page unreachable, maybe crashed. Status code:{resp.status_code}")
    except requests.exceptions.Timeout:
        print("Connection timed out. Are you connected to the PICO wifi?")
    except Exception as e:
        print(e)

def return_scripts():
    try:
        resp = requests.get(f"{url}/ducky",timeout=5)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            table = soup.find('table')
            scripts=[]
            for script in table.findAll('td')[::2]:
                scripts.append(script.text)
            return scripts
        else:
            print(f"Page unreachable, maybe crashed. Status code:{resp.status_code}")
    except requests.exceptions.Timeout:
        print("Connection timed out. Are you connected to the PICO wifi?")
    except Exception as e:
        print(e)

def get_script_content(script_name):
    scripts = return_scripts()
    if script_name not in scripts:
        print(f"Script: {script_name} wasn't located on ducky. Use 'python .\\cmd_4_web_ducky.py --list' to see available script for edit")
        return
    try:
        resp = requests.get(f"{url}/edit/{script_name}",timeout=5)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            content=soup.find('textarea').text
            print(content)
        else:
            print("This script doesn't exist!")
    except requests.exceptions.Timeout:
        print("Connection timed out. Are you connected to the PICO wifi?")
    except Exception as e:
        print(e)
def run_script(name):
    try:
        resp = requests.get(f"{url}/run/{name}",timeout=5)
        if resp.status_code == 200:
            print(f"Script: {name} was ran")
        else:
            print("Something went south!")
    except requests.exceptions.Timeout:
        print("Connection timed out. Are you connected to the PICO wifi?")
    except Exception as e:
        print(e)

def create_new_script(script_path):
    if not os.path.isfile(script_path):
        print(f"Script: {script_path} wasn't found.")
        return

    with open(script_path, 'r', encoding='utf-8') as file:
        script = file.read()
    
    script_name = f"{script_path.split("\\")[-1].split(".")[0]}.dd"
    
    data={'scriptName':script_name, 'scriptData':script}
    try:
        resp = requests.post(f"{url}/new",data=data,timeout=6)
        if resp.status_code == 200:
            print(f"{script_name} created succesfully!")
    except requests.exceptions.Timeout:
        print("Connection timed out. Are you connected to the PICO wifi?")
    except Exception as e:
        print(e)

def edit_script(name,script_path):
    if not os.path.isfile(script_path):
        print(f"Script: {script_path} wasn't found.")
        return
    
    scripts = return_scripts()
    if name not in scripts:
        print(f"Script: {name} wasn't located on ducky. Use 'python .\\cmd_4_web_ducky.py --list' to see available script for edit")
        return
    
    with open(script_path, 'r', encoding='utf-8') as file:
        script = file.read()
    
    data={'scriptData':script}
    try:
        resp = requests.post(f"{url}/write/{name}",data=data,timeout=10)
        if resp.status_code == 200:
            print(f"{name} was edited successfully!")
    except requests.exceptions.Timeout:
        print("Connection timed out. Edit might have broke webserver :(")
    except Exception as e:
        print(e)

def main():
    parser = argparse.ArgumentParser(description="Pico W ducky CLI")

    parser.add_argument("-l","--list",action="store_true", help="Get list of loaded in scripts")
    parser.add_argument("-r","--run",metavar="script_name", help="Name of the script which you want to run. Get script names from running: python .\\cmd_4_web_ducky.py --list")
    parser.add_argument("-c","--create",metavar="script_path" ,help="Have the file ending as '.dd'. For example: 'example.dd' for it to show up in script list")

    parser.add_argument("-e","--edit",nargs=2,metavar=("script_name","script_path"), help="Enter name of the script you want to edit and local script path for new script content. Example: '.\\cmd_4_web_ducky.py -e payload2.dd 'C:/User/Scripts/edited_script.txt''")
    parser.add_argument("-s","--show",metavar="script_name",help="Enter valid script name to see its contents")
    args = parser.parse_args()

    if args.list:
        get_scripts()
    elif args.run:
        script_name = args.run
        run_script(script_name)
    elif args.create:
        script_path = args.create
        create_new_script(script_path)
    elif args.edit:
        script_name,script_path = args.edit
        edit_script(script_name,script_path)
    elif args.show:
        script_name = args.show
        get_script_content(script_name)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()