import os
import string
import random
import rarfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from threading import Lock

archive_path = r"C:\Users\hp\Desktop\j\LOLI TIME.exe"
chars = string.ascii_uppercase + string.digits
pwd_length = 6

temp_dir = r"C:\Users\hp\Desktop\j\temp_extract"
os.makedirs(temp_dir, exist_ok=True)

# 线程安全的密码集合
used_passwords = set()
password_lock = Lock()

def generate_unique_password(length):
    while True:
        password = "".join(random.choices(chars, k=length))
        with password_lock:
            if password not in used_passwords:
                used_passwords.add(password)
                return password

def try_extract(password):
    try:
        # 清空临时目录中的文件
        for file in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        
        with rarfile.RarFile(archive_path) as rf:
            rf.extractall(temp_dir, pwd=password.encode())  # 注意：某些版本的 rarfile 需要 bytes 类型的密码
        print(f"Password is correct: {password}")
        return password
    except Exception as e:
        # print(f"Error occurred with password {password}: {e}")  # 可选：打印错误信息以进行调试
        return None

def main():
    max_workers = 6  # 根据CPU核心调整线程数
    attempts = 36**4  # 总尝试次数
    found_password = None

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(try_extract, generate_unique_password(pwd_length)) for _ in range(attempts)]
        for future in tqdm(as_completed(futures), total=attempts, desc="Trying password..."):
            result = future.result()
            if result:
                found_password = result
                break
        
        if found_password:
            print(f"The password is: {found_password}")
        else:
            print("Password not found.")

        # 清理临时目录
        for file in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)

if __name__ == "__main__":
    main()