import json
import tkinter as tk
from difflib import get_close_matches

# Variables para almacenar la pregunta actual y los datos
current_question = ""
data = {"question": []}

def load_data(file_path: str) -> dict:
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"question": []}
    return data

def save_data(file_path: str, data: dict):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, data: dict) -> str | None:
    for q in data["question"]:
        if q["question"] == question:
            return q["answer"]

def handle_user_input():
    global current_question, data
    user_input = user_input_entry.get()
    user_input_entry.delete(0, tk.END)

# Lista de palabras prohibidas
forbidden_words = ["palabra1", "palabra2", "palabra3"]  # Agrega las palabras que deseas prohibir

def handle_user_input():
    global current_question, data
    user_input = user_input_entry.get()
    user_input_entry.delete(0, tk.END)

    # Verificar si la entrada contiene palabras prohibidas
    if any(forbidden_word in user_input.lower() for forbidden_word in forbidden_words):
        chat_log.config(state=tk.NORMAL)
        chat_log.insert(tk.END, "Bot: ¡Advertencia! Has utilizado una palabra prohibida.\n")
        chat_log.config(state=tk.DISABLED)
        return  # No procesar la entrada prohibida

    if user_input.lower() == "quit":
        root.quit()  # Cerramos la aplicación
    else:
        best_match = find_best_match(user_input, [q["question"] for q in data["question"]])
        chat_log.config(state=tk.NORMAL)
        chat_log.insert(tk.END, f"Tu: {user_input}\n")
        if best_match:
            answer = get_answer_for_question(best_match, data)
            chat_log.insert(tk.END, f"Bot: {answer}\n")
        else:
            chat_log.insert(tk.END, "Bot: No sé la respuesta. ¿Puede enseñármela?\n")
            current_question = user_input
            user_input_entry.config(state=tk.NORMAL)
            user_input_entry.delete(0, tk.END)  # Limpiamos la entrada
            user_input_entry.bind('<Return>', handle_new_answer)
            user_input_entry.focus_set()  # Enfocamos el campo de entrada


def handle_new_answer(event):
    global current_question, data
    new_answer = user_input_entry.get()
    user_input_entry.delete(0, tk.END)

    if new_answer.lower() != "skip" and current_question:
        data["question"].append({"question": current_question, "answer": new_answer})
        current_question = ""  # Limpiamos la variable

        # Mostramos el mensaje de agradecimiento
        chat_log.config(state=tk.NORMAL)
        chat_log.insert(tk.END, "Bot: ¡Gracias! ¡He aprendido algo nuevo!\n")
        chat_log.config(state=tk.DISABLED)
        save_data("data.json", data)  # Guardamos los datos actualizados

data = load_data("data.json")
root = tk.Tk()
root.title("Chatbot")

intro_label = tk.Label(root, text="Consejo: Usa el boton enviar para insertar las preguntas y el boton enter de tu teclado para guardar las respuestas", font=("Arial", 16))

intro_label.pack()

frame = tk.Frame(root)
frame.pack(pady=10)

scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

chat_log = tk.Text(frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
chat_log.pack()

user_input_entry = tk.Entry(root, font=("Arial", 14))
user_input_entry.pack(pady=10)

send_button = tk.Button(root, text="Enviar", command=handle_user_input)
send_button.pack()

chat_log.config(state=tk.DISABLED)

root.mainloop()
