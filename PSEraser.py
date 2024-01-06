import os
import getpass
import psutil
import difflib
import platform

current_username = getpass.getuser()

BANNER = """
 ______ _    _______
(_____ \ |  (_______)
 _____) ) \\  _____    ____ ____  ___  ____  ____
|  ____/ \\ \\|  ___)  / ___) _  |/___)/ _  )/ ___)
| |  _____) ) |_____| |  ( ( | |___ ( (/ /| |
|_| (______/|_______)_|   \\_||_(___/ \\____)_|
___________________________________________
by \033[92m"Lazzy503"\033[0m
Github Profile \033[92m@lazzy503-umer\033[0m
"""

# Colorful characters for "A Proper Process Eraser TOOL"
tool_string = "\033[95mA \033[91mP\033[93mr\033[96mo\033[92mp\033[94me\033[91mr \033[93mP\033[95mr\033[91mo\033[92mc\033[96me\033[93ms\033[91ms \033[92mE\033[93mr\033[91ma\033[93ms\033[96me\033[91mr \033[92mT\033[95mo\033[94mo\033[91ml\033[0m"

BANNER += tool_string

BANNER += """
___________________________________________
"""

def clear_screen():
    system = platform.system()
    if system == "Windows":
        os.system('cls')
    else:
        os.system('clear')
    
    print("\033[94m" + BANNER + "\033[0m")  # Print the banner after clearing

def search_executables_in_directories(directories, extensions):
    executables = []
    for directory in directories:
        for root, _, files in os.walk(directory):
            for filename in files:
                if filename.endswith(tuple(extensions)):
                    executables.append(os.path.join(root, filename))
    return executables

def save_executed_program(program_path):
    try:
        file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "trained.txt")
        with open(file_path, "a") as file:
            file.write(program_path + "\n")
    except Exception as e:
        print("\033[91mError saving program path:", e, "\033[0m")

def get_closest_process_name(user_input):
    running_process_names = [process.info['name'] for process in psutil.process_iter(attrs=['name'])]
    closest_match = difflib.get_close_matches(user_input.lower(), [name.lower() for name in running_process_names], n=1)
    return closest_match[0] if closest_match else None

def close_process_by_name(process_name):
    system = platform.system()
    try:
        if system == "Windows":
            os.system(f"taskkill /F /IM {process_name}")
        elif system == "Linux" or system == "Darwin":
            os.system(f"pkill -f {process_name}")
        print(f"\033[91mClosed process: {process_name}\033[0m")
    except Exception as e:
        print(f"\033[91mError closing process: {e}\033[0m")

def main():
    print("\033[94m" + BANNER + "\033[0m")
    
    program_files_dirs = [r"C:\Program Files", r"C:\Program Files (x86)", r"C:\Users"]
    executable_extensions = (".exe",)
    program_files_executables = search_executables_in_directories(program_files_dirs, executable_extensions)

    while True:
        user_command = input("\033[92mEnter a command: \033[0m")

        if user_command.lower() == "exit":
            break

        if user_command.lower() in ['cls', 'clear']:
            clear_screen()

        if user_command.startswith("open "):
            program_name = user_command[5:].strip()

            matched_paths = []
            try:
                with open("trained.txt", "r") as file:
                    for line in file:
                        if program_name.lower() in line.lower():
                            matched_paths.append(line.strip())
            except Exception as e:
                print("\033[91mError reading from trained data file:", e, "\033[0m")

            if matched_paths:
                try:
                    os.startfile(matched_paths[0])
                    print("\033[94mProgram opened based on trained data.\033[0m")
                except Exception as e:
                    print(f"\033[91mError opening program: {e}\033[0m")
            else:
                matching_paths = [path for path in program_files_executables if program_name.lower() in path.lower()]

                if matching_paths:
                    print("\033[93mMatching Programs:\033[0m")
                    for i, path in enumerate(matching_paths, start=1):
                        print(f"{i}. {path}")

                    selection = input("\033[92mEnter the number of the program to open (or 'q' to quit): \033[0m")

                    if selection.lower() == 'q':
                        continue

                    try:
                        program_index = int(selection)
                        if 1 <= program_index <= len(matching_paths):
                            selected_path = matching_paths[program_index - 1]
                            try:
                                os.startfile(selected_path)
                                save_executed_program(selected_path)
                            except Exception as e:
                                print(f"\033[91mError opening program: {e}\033[0m")
                        else:
                            print("\033[91mInvalid selection.\033[0m")
                    except ValueError:
                        print("\033[91mInvalid input.\033[0m")
                else:
                    print("\033[93mNo matching programs found.\033[0m")

        elif user_command.startswith("close "):
            program_name = user_command[6:].strip()
            closest_process_name = get_closest_process_name(program_name)

            if closest_process_name:
                print(f"\033[94mMatching process name found: {closest_process_name}\033[0m")
                close_process_by_name(closest_process_name)
            else:
                print("\033[93mNo matching process found.\033[0m")
        else:
            print("\033[94mCleaned!\033[0m")

if __name__ == "__main__":
    main()
