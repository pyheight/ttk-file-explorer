"""
This script is used to package the project via pyinstaller,
Allows packaging in different Python environments to support running on different Windows platforms.
"""

import os  
import sys
import re
import time  
import subprocess

from PyInstaller.__main__ import run

version_info = sys.version_info
python_version = f'{version_info[0]}.{version_info[1]}.{version_info[2]}'

source_name = 'ttk file explorer'  
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  
main_script = os.path.join(project_root, 'main.py')  

icon_path = os.path.join(project_root, 'images', 'icon.ico')  
gif_path = os.path.join(project_root, 'images', 'loading.gif')  
splash_path = os.path.join(project_root, 'script', 'images', 'splash.png') 
image_dest_path = './images/' 

build_time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(int(time.time())))
dist_folder = os.path.join(project_root, 'script', 'output', python_version, build_time)  
work_folder = os.path.join(project_root, 'script', 'temp', python_version)  
spec_folder = os.path.join(project_root, 'script')  
version_file = os.path.join(project_root, 'script', 'version.txt')  
spec_file = os.path.join(spec_folder, 'ttk file explorer.spec')
pyinstaller_args_file = os.path.join(dist_folder, 'pyinstaller_args.txt')

# You may need to adjust the path construction logic accordingly.
python_dir = os.path.dirname(sys.executable)
python_scripts_dir = os.path.join(python_dir, 'Scripts')    
pyi_makespec_path = os.path.join(python_scripts_dir, 'pyi-makespec.exe')
tcl_library_path = os.path.join(python_dir, 'tcl', 'tcl8.6')  
tk_library_path = os.path.join(python_dir, 'tcl', 'tk8.6') 

pyinstaller_args = [ 
    # --onefile takes a long time to startup  
    '--onedir',
    '--windowed',  
    '--name={}'.format(source_name),  
    '--paths={}'.format(project_root),  
    '--icon={}'.format(icon_path),  
    '--specpath={}'.format(spec_folder),  
    '--version-file={}'.format(version_file),  
    '--add-data={}:{}'.format(icon_path, image_dest_path),  
    '--add-data={}:{}'.format(gif_path, image_dest_path),  
    '--splash={}'.format(splash_path)
]  

hidden_imports = [  
    'constants',  
    'images',  
    'view',  
    'model',  
    'controller',  
    'controller.tab_manager',     
    '__init__',  
]  

for module in hidden_imports:  
    pyinstaller_args.append('--hidden-import={}'.format(module))  

pyinstaller_args.append(main_script)  

output_args = [
    '--distpath={}'.format(dist_folder),  
    '--workpath={}'.format(work_folder),  
]


def set_environment_variables():
    # This is necessary on some systems, such as Windows 7, where PyInstaller may fail to find the init.tcl file without these variables set.
    # Require end users to manually configure the environment.
    
    if os.path.exists(tcl_library_path):
        print(f'Make sure that you have manually created a new TCL_LIBRARY = {tcl_library_path} in the environment variables of the system before running.')
    if os.path.exists(tk_library_path):
        print(f'Make sure that you have manually created a new TK_LIBRARY = {tk_library_path} in the environment variables of the system before running.')
    

def create_spec(pyi_makespec_path):
    # In a multi-version Python environment, you can't find the correct version by using pyi-makespec directly.

    pyi_makespec_path = pyi_makespec_path if os.path.exists(pyi_makespec_path) else 'pyi-makespec'

    cmd = [pyi_makespec_path] + pyinstaller_args

    print('\nCreating a list of parameters for the .spec file:\n') 
    for arg in cmd:  
        print(arg)  

    result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE)  
    stdout = result.stdout.decode('utf-8')  
    print('\n' + stdout.rstrip('\n'))  


def updated_spec_config(new_text_pos, new_always_on_top):
    with open(spec_file, 'r', encoding='utf-8') as file:  
        content = file.read()  

    splash_init_pattern = r'splash = Splash\('  
    match = re.search(splash_init_pattern, content, re.MULTILINE)  
    if match:  
        end_of_line = content.find(')', match.start())  
        splash_init_line = content[match.start():end_of_line + 1]  
          
        updated_line = re.sub(r'text_pos=.*?,', f'text_pos={new_text_pos},', splash_init_line)  
        updated_line = re.sub(r'always_on_top=.*?,', f'always_on_top={new_always_on_top},', updated_line)  
          
        content = content[:match.start()] + updated_line + content[end_of_line + 1:]  

    with open(spec_file, 'w', encoding='utf-8') as file:  
        file.write(content)  
        
    print('The .spec file has been updated with new Splash configuration:\n') 
    print(content)


def run_with_spec():
    spec_args = [spec_file] + output_args

    print('\nRunning PyInstaller with the .spec file parameters:\n') 
    for arg in spec_args:  
        print(arg)    

    print('\nThe application is being packaged using a .spec file...\n') 
    run(spec_args)

    with open(pyinstaller_args_file, 'w', encoding='utf-8') as file:  
        file.write(str(pyinstaller_args))


def platform_compatibility():
    # The python shared library links to the DLL.
    # You need to use the python version for different Windows platforms. 
    # The last python version for Windows 7 was python 3.8.

    if (version_info[0], version_info[1]) > (3, 8):
        print('The packaged program is not compatible with Windows 7 and should run on Windows 10 and later (or a compatible version of Windows).')
    else:
        print('The packaged program supports Windows 7 and above, including compatible versions that may be earlier.')    


def main():
    set_environment_variables()
    create_spec(pyi_makespec_path)
    updated_spec_config(new_text_pos='(30, 345)', new_always_on_top='False')
    run_with_spec()
    platform_compatibility()


if __name__ == '__main__':
    main()
