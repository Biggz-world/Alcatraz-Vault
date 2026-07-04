import os
import subprocess
import sys
import ctypes
from datetime import datetime

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_command(command, description):
    print(f"[\033[94mSTAGE:\033[0m] {description}...")
    try:
        # Using shell=True because some windows commands like 'sfc' are actually batch files
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"[\033[92mSUCCESS\033[0m]: {description}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[\033[91mERROR\033[0m]: {description}\n{e.stderr}")
        return False
    except Exception as e:
        print(f"[\033[91mFAILED\033[0m]: {description}\n{str(e)}")
        return False

def clear_temp_files():
    print(f"[\033[94mSTAGE:\033[0m] Clearing Junk Files...")
    paths = [
        os.environ.get('TEMP'),
        os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'Temp'),
        os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'Prefetch')
    ]
    
    for path in paths:
        if path and os.path.exists(path):
            print(f"  -> Cleaning {path}")
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                try:
                    if os.path.isfile(item_path) or os.path.islink(item_path):
                        os.unlink(item_path)
                    elif os.path.isdir(item_path):
                        import shutil
                        shutil.rmtree(item_path)
                except Exception:
                    pass # Files often in use by the system

def main():
    if not is_admin():
        print("[\033[91mCRITICAL\033[0m] Please run this script as Administrator!")
        input("Press Enter to exit...")
        sys.exit(1)

    print(f"\033[1;33m=== PC Health Maintenance Pipeline ===\033[0m")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Stage 1: System File Checker
    run_command("sfc /scannow", "System File Checker (SFC)")

    # Stage 2: DISM Repair
    run_command("DISM /Online /Cleanup-Image /RestoreHealth", "DISM Image Repair")

    # Stage 3: Network Flush
    run_command("ipconfig /flushdns", "DNS Cache Flush")

    # Stage 4: Disk Junk
    clear_temp_files()

    print(f"\n\033[1;32mPipeline Complete! Your PC is looking healthy.\033[0m")
    input("Press Enter to close...")

if __name__ == "__main__":
    main()
