import os
import subprocess


def execute_scripts_in_folder(folder_path):
    '''
    This function executes all the scripts.
    :param folder_path: folder path of scripts to be executed.
    '''
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.py'):
            script_path = os.path.join(folder_path, file_name)
            subprocess.run(['python', script_path])  # executing the script using subprocess


def main():
    queries_folder = 'framester-queries'  # update this to your actual folder path
    execute_scripts_in_folder(queries_folder)


if __name__ == "__main__":
    main()
