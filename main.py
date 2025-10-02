import os
import random
import subprocess
from datetime import datetime
import re
import json

# ================== НАСТРОЙКИ ==================
TARGET_REPO = "/root/github_auto"
SOURCE_FILES_PATH = "/root/github_auto/SourceFiles"
LOG_FILE = os.path.join(TARGET_REPO, "actions_log.json")

REAL_FILE_NAMES = [
    "utils.py",
    "helpers.py",
    "data_processing.py",
    "api_client.py",
    "models.py",
    "services.py",
    "config_loader.py",
    "getby.py",
    "auth.py",
    "database.py",
    "validators.py",
    "session_manager.py",
    "notifications.py",
    "report_generator.py",
    "scheduler.py",
    "cache.py"
]

COMMIT_MESSAGES = [
    "Fix bug in data processing",
    "Add helper functions for API",
    "Refactor user authentication",
    "Improve logging messages",
    "Update README and documentation",
    "Optimize performance in utils",
    "Minor code cleanup",
    "gogo",
    "ready go",
    "Add unit tests for models",
    "Fix edge case in authentication",
    "Update dependencies",
    "Improve error handling",
    "Refactor API client structure",
    "Add caching mechanism",
    "Enhance database queries",
    "Update config settings",
    "Add comments and documentation",
    "Refactor helper functions"
]


# ================== ЛОГИКА С ЛОГОМ ==================
def load_log():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"created_files": 0, "inserted_code": 0, "comments": 0}


def save_log(data):
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def choose_action(log_data):
    # динамическая вероятность
    prob_new_file = 0.15
    total = sum(log_data.values()) or 1
    if log_data["created_files"] / total > 0.2:  # если файлов слишком много
        prob_new_file = 0.05
    if log_data["created_files"] / total < 0.05:  # если слишком мало
        prob_new_file = 0.25

    actions = ["new_file", "insert_code", "comment"]
    weights = [prob_new_file, 0.6, 0.25]  # базовые веса
    return random.choices(actions, weights=weights, k=1)[0]


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


def create_new_file():
    base_name = random.choice(REAL_FILE_NAMES)
    name, ext = os.path.splitext(base_name)
    i = 1
    while True:
        new_file = os.path.join(TARGET_REPO, f"{name}{'' if i==1 else f'_{i}'}{ext}")
        if not os.path.exists(new_file):
            open(new_file, "w", encoding="utf-8").close()
            return new_file
        i += 1


def insert_code(target_file):
    source_files = get_py_files(SOURCE_FILES_PATH)
    if not source_files:
        print("Папка с исходниками пуста!")
        return None
    file_path = random.choice(source_files)
    funcs = extract_random_functions(file_path)
    if not funcs:
        print(f"В файле {file_path} нет функций для вставки")
        return None
    with open(target_file, "a", encoding="utf-8") as f:
        for func_code in funcs:
            f.write("\n" + func_code + "\n")
    return target_file


def add_comment(target_file):
    comment = f"#  {datetime.now()}\n"
    with open(target_file, "a", encoding="utf-8") as f:
        f.write(comment)
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
    log_data = load_log()

    action = choose_action(log_data)
    print("Выбрано действие:", action)

    target_file = None
    if action == "new_file":
        target_file = create_new_file()
        log_data["created_files"] += 1
    elif action == "insert_code":
        py_files = get_py_files(TARGET_REPO)
        if not py_files:
            target_file = create_new_file()
            log_data["created_files"] += 1
        else:
            target_file = random.choice(py_files)
        result = insert_code(target_file)
        if result:
            target_file = result
            log_data["inserted_code"] += 1
    else:  # comment
        py_files = get_py_files(TARGET_REPO)
        if py_files:
            target_file = random.choice(py_files)
            result = add_comment(target_file)
            if result:
                target_file = result
                log_data["comments"] += 1

    git_push(target_file)
    save_log(log_data)


if __name__ == "__main__":
    main()

def main() -> None:
    """
    Get images list and annotations list from input dir.
    Update new images and annotations.
    Save images and annotations in output dir.
    """
    img_paths, annos = get_dataset(LABEL_DIR, IMG_DIR)
    for index in range(NUMBER_IMAGES):
        idxs = random.sample(range(len(annos)), 4)
        new_image, new_annos, path = update_image_and_anno(
            img_paths,
            annos,
            idxs,
            OUTPUT_SIZE,
            SCALE_RANGE,
            filter_scale=FILTER_TINY_SCALE,
        )


def random_chars(number_char: int) -> str:
    """
    Automatic generate random 32 characters.
    Get random string code: '7b7ad245cdff75241935e4dd860f3bad'
    >>> len(random_chars(32))
    32
    """
    assert number_char > 1, "The number of character should greater than 1"
    letter_code = ascii_lowercase + digits
    return "".join(random.choice(letter_code) for _ in range(number_char))

