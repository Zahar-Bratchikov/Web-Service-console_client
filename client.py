import requests

BASE_URL = "http://localhost:8080"
TOKEN_FILE = "tokens.txt"

# Загрузка токена из файла
def load_token():
    try:
        with open(TOKEN_FILE, "r") as file:
            return file.readline().strip()
    except FileNotFoundError:
        print("Token file not found.")
        return None

# Создать заметку
def create_note():
    token = load_token()
    if not token:
        return

    text = input("Введите текст заметки: ")
    # Передаем параметр text в строку запроса, а не в теле запроса
    response = requests.post(
        f"{BASE_URL}/note?token={token}&text={text}"  # Параметры передаются в строку запроса
    )

    if response.status_code == 200:
        data = response.json()
        print(f"Заметка создана с ID: {data['id']}")
    else:
        print(f"Ошибка: {response.json()}")

# Прочитать заметку
def read_note():
    token = load_token()
    if not token:
        return

    note_id = input("Введите ID заметки: ")
    response = requests.get(f"{BASE_URL}/note/{note_id}", params={"token": token})

    if response.status_code == 200:
        data = response.json()
        print(f"Текст заметки (ID {data['id']}): {data['text']}")
    else:
        print(f"Ошибка: {response.json()}")

# Обновить заметку
def update_note():
    token = load_token()
    if not token:
        return

    note_id = input("Введите ID заметки: ")
    new_text = input("Введите новый текст заметки: ")
    response = requests.patch(
        f"{BASE_URL}/note/{note_id}?token={token}&new_text={new_text}"  # Параметры передаются в строку запроса
    )

    if response.status_code == 200:
        data = response.json()
        print(f"Текст заметки обновлен (ID {data['id']}): {data['text']}")
    else:
        print(f"Ошибка: {response.json()}")

# Удалить заметку
def delete_note():
    token = load_token()
    if not token:
        return

    note_id = input("Введите ID заметки: ")
    response = requests.delete(f"{BASE_URL}/note/{note_id}", params={"token": token})

    if response.status_code == 200:
        print("Заметка удалена.")
    else:
        print(f"Ошибка: {response.json()}")

# Получить список заметок
def list_notes():
    token = load_token()
    if not token:
        return

    response = requests.get(f"{BASE_URL}/notes", params={"token": token})

    if response.status_code == 200:
        data = response.json()
        print("Список заметок:")
        for idx, note_id in data["notes"].items():
            print(f"{idx}: {note_id}")
    else:
        print(f"Ошибка: {response.json()}")

# Основное меню
def main():
    while True:
        print("\nМеню:")
        print("1. Создать заметку")
        print("2. Прочитать заметку")
        print("3. Обновить заметку")
        print("4. Удалить заметку")
        print("5. Список заметок")
        print("0. Выход")
        choice = input("Выберите действие: ")

        if choice == "1":
            create_note()
        elif choice == "2":
            read_note()
        elif choice == "3":
            update_note()
        elif choice == "4":
            delete_note()
        elif choice == "5":
            list_notes()
        elif choice == "0":
            break
        else:
            print("Некорректный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()
