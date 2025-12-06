import os
import logging
import shutil
import subprocess
import pyautogui

logging.basicConfig(filename='funcs.log',level=logging.INFO,
                    format='%(asctime)s %(name)s - %(levelname)s - %(message)s')


QUEUE_LEN = 1
MAX_PACKET = 1024
MAX_LEN = 6
IP = '0.0.0.0'
PORT = 3035
NOT_EXIST_DIR = 'directory Not found'
NOT_EXIST_FILE = 'file not found'
SUCCESS = 'success'
DELETED = 'file deleted'
COPIED = 'file copied'
EXECUTED = 'app executed'
EXITED = 'client exited'
FAILURE = 'failed in the way'
PATH_FAILURE = 'source file not found'
DESTINATION_COPY = 'destination not found'
NOT_EXIST_EXECUTE = 'app path not found'
PICTURE = 'picture'
NOT_COMMAND = 'not a command'

def di_r(dir_path):
    logging.info('path = ' + dir_path)
    try:
        contents = os.listdir(dir_path)
        return SUCCESS, ", ".join(contents)
    except FileNotFoundError:
        logging.error('Directory not exist')
        return FAILURE, NOT_EXIST_DIR
    except NotADirectoryError:
        logging.error('Got a file path')
        return FAILURE, NOT_EXIST_DIR


def delete(delete_path):
    logging.info('file_path = ' + delete_path)
    try:
        file_path = delete_path.strip('"')
        os.remove(file_path)
        return SUCCESS,DELETED
    except FileNotFoundError:
        logging.error('File not exist')
        return FAILURE,NOT_EXIST_FILE


def copy(from_path, to_path):
    logging.info('from_path = ' + from_path)
    logging.info('to_path = ' + to_path)
    try:
        from_path = from_path.strip('"')
        to_path = to_path.strip('"')
        shutil.copy2(from_path, to_path)
        return SUCCESS,COPIED
    except FileNotFoundError:
        if not os.path.exists(from_path):
            logging.error('Source path not found')
            return FAILURE,PATH_FAILURE
        if not os.path.exists(to_path):
            logging.error('Destination not found')
            return FAILURE,DESTINATION_COPY
        return FAILURE,FAILURE


def execute(execute_path):
    try:
        execute_path = execute_path.strip('"')
        subprocess.call(execute_path)
        return SUCCESS,EXECUTED
    except FileNotFoundError:
        logging.error('Execute path not exist')
        return FAILURE,NOT_EXIST_EXECUTE


def take_screenshot():
    picture = pyautogui.screenshot()
    picture.save('screen.jpg')
    return 'screen.jpg'


def send_screenshot():
    path = take_screenshot()
    with open(path, 'rb') as f:
        img_bytes = f.read()
    return SUCCESS, img_bytes


def length_str(msg):
    return str(len(msg)).zfill(6)


if __name__ == "__main__":

    # asserts for di_r
    cont_status, cont = di_r(r'C:\Users\USER\PycharmProjects')
    # assert ('PythonProject' in cont)   # you can uncomment and adapt if you want

    returned = di_r('nope')
    # di_r now returns (status, message)
    assert returned == (FAILURE, NOT_EXIST_DIR)

    # assert for copy
    copy_status, copy_msg = copy(r"C:\Users\USER\Downloads\cyphen1.py",r"C:\Users\USER\PycharmProjects\PythonProject")
    assert copy_status == SUCCESS

    # asserts for take_screenshot
    image = pyautogui.screenshot()
    image.save(r'screen.jpg')
    data = open("screen.jpg", "rb").read()
    # take_screenshot now returns the file path string
    assert take_screenshot() == 'screen.jpg'

    # asserts for send screenshot
    send_status, send_data = send_screenshot()
    assert send_status == SUCCESS

    # assert for execute
    exec_status, exec_msg = execute(r"C:\\ffakeee\ ")
    assert exec_status == FAILURE and exec_msg == NOT_EXIST_EXECUTE

    # asserts for delete
    del_status1, del_msg1 = delete(r"C:\Users\USER\Downloads\cyphen1.py")
    assert del_status1 == SUCCESS

    del_status2, del_msg2 = delete(" fake ")
    assert del_status2 == FAILURE



    print('asserts passed')
