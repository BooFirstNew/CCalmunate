import os
import random
import subprocess
from datetime import datetime
import re

# ================== НАСТРОЙКИ ==================
TARGET_REPO = "/root/github_auto"           # папка для коммитов
SOURCE_FILES_PATH = "/root/github_auto/SourceFiles"  # папка с исходными файлами

# Реальные названия файлов
REAL_FILE_NAMES = [
    "utils.py",
    "helpers.py",
    "data_processing.py",
    "api_client.py",
    "models.py",
    "services.py",
    "config_loader.py"
    "getby.py"
]

# Реальные сообщения коммитов
COMMIT_MESSAGES = [
    "Fix bug in data processing",
    "Add helper functions for API",
    "Refactor user authentication",
    "Improve logging messages",
    "Update README and documentation",
    "Optimize performance in utils",
    "Minor code cleanup"
    "gogo"
    "ready go"
]

# ================== МЕТОДЫ ==================

def ensure_target_repo():
    os.makedirs(TARGET_REPO, exist_ok=True)

def get_py_files(path):
    if not os.path.exists(path):
        return []
    return [os.path.join(path, f) for f in os.listdir(path) if f.endswith(".py")]

def extract_random_functions(file_path, max_funcs=3):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    functions = re.findall(r"(def .+?:\n(?:[ \t]+.+\n)+)", content)
    if not functions:
        return []
    count = random.randint(1, min(max_funcs, len(functions)))
    return random.sample(functions, count)

def choose_target_file():
    py_files = get_py_files(TARGET_REPO)
    # 15% шанс создать новый файл
    if not py_files or random.random() < 0.15:
        base_name = random.choice(REAL_FILE_NAMES)
        name, ext = os.path.splitext(base_name)
        i = 1
        while True:
            new_file = os.path.join(TARGET_REPO, f"{name}{'' if i==1 else f'_{i}'}{ext}")
            if not os.path.exists(new_file):
                open(new_file, "w", encoding="utf-8").close()
                return new_file
            i += 1
    # иначе случайный существующий файл
    return random.choice(py_files)

def insert_code(target_file):
    source_files = get_py_files(SOURCE_FILES_PATH)
    if not source_files:
        return None
    file_path = random.choice(source_files)
    funcs = extract_random_functions(file_path)
    if not funcs:
        return None
    with open(target_file, "a", encoding="utf-8") as f:
        for func_code in funcs:
            f.write(func_code)
    return target_file

def add_comment(target_file):
    comment = f"#  {datetime.now()}\n"
    with open(target_file, "a", encoding="utf-8") as f:
        f.write(comment)
    return target_file

def minor_update(target_file):
    line = f"\n# Мелкое улучшение {datetime.now()}\n"
    with open(target_file, "a", encoding="utf-8") as f:
        f.write(line)
    return target_file

def git_push(file_changed):
    if not file_changed:
        print("Нет изменений для коммита")
        return
    subprocess.run(["git", "-C", TARGET_REPO, "add", file_changed])
    message = f"{random.choice(COMMIT_MESSAGES)} ({datetime.now()})"
    subprocess.run(["git", "-C", TARGET_REPO, "commit", "-m", message])
    subprocess.run(["git", "-C", TARGET_REPO, "push", "origin", "main"])
    print(f"Коммит сделан: {file_changed} с сообщением: {message}")

# ================== ОСНОВНАЯ ЛОГИКА ==================
def main():
    ensure_target_repo()
    target_file = choose_target_file()
    ACTIONS = [insert_code, add_comment, minor_update]
    actions_to_run = random.sample(ACTIONS, k=random.randint(1, len(ACTIONS)))
    file_changed = None
    for action in actions_to_run:
        result = action(target_file)
        if result:
            file_changed = result
    git_push(file_changed)

if __name__ == "__main__":
    main()
#  2025-10-01 11:05:35.025973
