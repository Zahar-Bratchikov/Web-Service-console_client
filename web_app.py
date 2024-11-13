import os
from datetime import datetime
from fastapi import APIRouter, HTTPException, Query
from model import CreateNoteResponse, NoteTextResponse, NoteInfoResponse, NoteListResponse

api_router = APIRouter()

NOTES_DIR = "notes"
TOKENS_FILE = "tokens.txt"

# Ensure notes directory exists
os.makedirs(NOTES_DIR, exist_ok=True)

# Проверка токена
def load_tokens():
    if not os.path.exists(TOKENS_FILE):
        return set()
    with open(TOKENS_FILE, "r") as file:
        return set(line.strip() for line in file)

def check_token(token: str):
    tokens = load_tokens()
    if token not in tokens:
        raise HTTPException(status_code=403, detail="Invalid token")

# Создать новую заметку
@api_router.post("/note", response_model=CreateNoteResponse)
def create_note(text: str = Query(...), token: str = Query(...)):
    check_token(token)
    note_id = len(os.listdir(NOTES_DIR)) + 1
    note_file = os.path.join(NOTES_DIR, f"{note_id}.txt")
    with open(note_file, "w") as file:
        file.write(f"text={text}\n")
        file.write(f"created_at={datetime.now().isoformat()}\n")
        file.write(f"updated_at={datetime.now().isoformat()}\n")
    return CreateNoteResponse(id=note_id)

# Получить текст заметки
@api_router.get("/note/{id}", response_model=NoteTextResponse)
def get_note_text(id: int, token: str = Query(...)):
    check_token(token)
    note_file = os.path.join(NOTES_DIR, f"{id}.txt")
    if not os.path.exists(note_file):
        raise HTTPException(status_code=404, detail="Note not found")
    with open(note_file, "r") as file:
        data = file.read().splitlines()
    text = [line.split("=")[1] for line in data if line.startswith("text=")][0]
    return NoteTextResponse(id=id, text=text)

# Получить информацию о времени создания и изменения заметки
@api_router.get("/note/{id}/info", response_model=NoteInfoResponse)
def get_note_info(id: int, token: str = Query(...)):
    check_token(token)
    note_file = os.path.join(NOTES_DIR, f"{id}.txt")
    if not os.path.exists(note_file):
        raise HTTPException(status_code=404, detail="Note not found")
    with open(note_file, "r") as file:
        data = file.read().splitlines()
    created_at = [line.split("=")[1] for line in data if line.startswith("created_at=")][0]
    updated_at = [line.split("=")[1] for line in data if line.startswith("updated_at=")][0]
    return NoteInfoResponse(created_at=created_at, updated_at=updated_at)

# Обновить текст заметки
@api_router.patch("/note/{id}", response_model=NoteTextResponse)
def update_note_text(id: int, new_text: str = Query(...), token: str = Query(...)):
    check_token(token)
    note_file = os.path.join(NOTES_DIR, f"{id}.txt")
    if not os.path.exists(note_file):
        raise HTTPException(status_code=404, detail="Note not found")
    with open(note_file, "r+") as file:
        data = file.read().splitlines()
        updated_data = []
        for line in data:
            if line.startswith("text="):
                updated_data.append(f"text={new_text}")
            else:
                updated_data.append(line)
        updated_data.append(f"updated_at={datetime.now().isoformat()}")
        file.seek(0)
        file.write("\n".join(updated_data))
        file.truncate()
    return NoteTextResponse(id=id, text=new_text)

# Удалить заметку
@api_router.delete("/note/{id}")
def delete_note(id: int, token: str = Query(...)):
    check_token(token)
    note_file = os.path.join(NOTES_DIR, f"{id}.txt")
    if not os.path.exists(note_file):
        raise HTTPException(status_code=404, detail="Note not found")
    os.remove(note_file)
    return {"detail": "Note deleted"}

# Получить список id заметок
@api_router.get("/notes", response_model=NoteListResponse)
def list_notes(token: str = Query(...)):
    check_token(token)
    note_ids = [int(filename.split(".")[0]) for filename in os.listdir(NOTES_DIR) if filename.endswith(".txt")]
    return NoteListResponse(notes={i: note_id for i, note_id in enumerate(note_ids)})
