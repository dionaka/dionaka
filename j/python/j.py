import os
import string
import random
import rarfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

archive_path = r"C:\Users\hp\Desktop\j\LOLI TIME.exe"
chars = string.ascii_uppercase + string.digits
pwd_length = 6

temp_dir = r"C:\Users\hp\Desktop\j\temp_extract"
os.makedirs(temp_dir, exist_ok=True)

def generate_random_password(length):
    return "".join(random.choices(chars, k=length))

def try_extract(password):
    try:
        for file in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        
        with rarfile.RarFile(archive_path) as rf:
            rf.extractall(temp_dir, pwd=password)
        print(f"password is correct: {password}")
        return password
    except Exception as e:
        return None

def main():
    #根据cup核心调整线程数
    max_workers = 6
    #总尝试次数
    attempts = 100000
    found_password = None

    with ThreadPoolExecutor(max_workers) as executor:
        futures = [executor.submit(try_extract, generate_random_password(pwd_length)) for _ in range(attempts)]
        for future in tqdm(as_completed(futures), total=attempts, desc="Trying password ..."):
            result = future.result()
            if result:
                found_password = result
                break
        
        if found_password:
            print(f"The password is: {found_password}")
        else:
            print("Password not found.")

        for file in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)

if __name__ == "__main__":
    main()