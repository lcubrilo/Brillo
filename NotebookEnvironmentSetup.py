import os
import subprocess

def main():
    try:        
        if 'BINDER_SERVICE_HOST' in os.environ:
            print("Running in Binder")
            
        else:
            print("Assuming local environment...")
            stdout = subprocess.run(['pip', 'install', '-r', 'requirements.txt'], capture_output=True, text=True)
            stdout = stdout.stdout.splitlines()
            
            installed_packages = []; already_satisfied = []

            for line in stdout:
                if "Requirement already satisfied" in line:
                    already_satisfied.append(line.split(' ')[2])
                elif "Successfully installed" in line:
                    installed_packages += line.split("Successfully installed ")[1].split()

            if not installed_packages:
                print("We already had all necessary packages."); return

            with open('requirements.txt', 'r') as f:
                line_count = sum(1 for line in f)
            print(f"Great, we already have the following packages: {', '.join(already_satisfied[:line_count])}")
            print(f"I had to install the following packages: {', '.join(installed_packages)}")

    except Exception as e:
        print(f"The following error happened: {str(e)}")

