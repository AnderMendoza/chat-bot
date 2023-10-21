# Importamos las librerías necesarias
import json
from difflib import get_close_matches

# Definimos las funciones necesarias para el chatbot

# Cargamos los datos de un archivo JSON y los devolvemos como un diccionario
def load_data(file_path: str) -> dict:
    with open(file_path, "r") as file:
        data: dict = json.load(file)
    return data


# Guardamos los datos proporcionados en formato JSON en la ruta de archivo especificada
def save_data(file_path: str, data: dict):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)


# Buscamos la mejor coincidencia entre una pregunta y una lista de preguntas
def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None


# Obtenemos la respuesta asociada a una pregunta en un conjunto de datos
def get_answer_for_question(question: str, data: dict) -> str | None:
    for q in data["question"]:
        if q["question"] == question:
            return q["answer"]


# Definimos la función principal del chatbot
def chat_bot():
    # cargar la base de conocimiento
    # Cargamos la base de conocimiento
    data: dict = load_data("data.json")

    # mientras funcione...
    # Mientras funcione...
    while True:
        # ingrese una pregunta
        # Ingresamos una pregunta
        user_input: str = input("Tu: ")

        # si ingresa "quit" entonces cierra el programa
        # Si ingresamos "quit" entonces cierra el programa
        if user_input.lower() == "quit":
            print(f"Bot: ¡Adiós!")
            break

        # buscar si existe alguna pregunta relacionada
        # Buscamos si existe alguna pregunta relacionada
        best_match: str | None = find_best_match(
            user_input, [q["question"] for q in data["question"]]
        )

        # si existe: enseñar la pregunta y respuesta
        # Si existe: enseñar la pregunta y respuesta
        if best_match:
            answer: str = get_answer_for_question(best_match, data)
            print(f"Bot: {answer}")

        # si no existe: responder NO LO SÉ
        # Si no existe se puede proporcionar una respuesta para que el bot guarde la respuesta y pregunta en la base de conocimiento
        else:
            print("Bot: No sé la respuesta. ¿Puede enseñármela?")
            new_answer: str = input('Ingrese la respuesta o "skip" para saltearla: ')

            if new_answer.lower() != "skip":
                data["question"].append({"question": user_input, "answer": new_answer})
                save_data("data.json", data)
                print("Bot: ¡Gracias! ¡He aprendido algo nuevo!")


chat_bot()
