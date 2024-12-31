import shutil
import os
import time

no = int(input('copy no: '))

for i in range(1, no+1):
    shutil.copytree('manager', f'agent_{i}', dirs_exist_ok=True)
    print(f'agent_{i} folder is copied from "manager-wt" folder')
    
# Pause the script execution for 5 seconds
sleep_time = 1
print(f'Termination of the terminal will be available in {sleep_time} second/s')
time.sleep(sleep_time)

# Keep the window open until user presses enter
os.system("pause")
