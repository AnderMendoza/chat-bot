import json
import tkinter as tk
from difflib import get_close_matches
import numpy as np
from tensorflow.keras.models import load_model

# Variables para almacenar la pregunta actual y los datos
current_question = ""
data = {"question": []}

# Cargamos datos del chatbot
def load_data(file_path: str) -> dict:
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"question": []}
    return data

# Guardamos datos del chatbot
def save_data(file_path: str, data: dict):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)

# Encontramos la mejor coincidencia de preguntas
def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

# Obtenemos la respuesta para una pregunta
def get_answer_for_question(question: str, data: dict) -> str | None:
    for q in data["question"]:
        if q["question"] == question:
            return q["answer"]
        
# Cargamos el modelo de la red neuronal
multiplication_model = load_model("multiplication_model.h5")
        
# Función para multiplicar dos números usando la red neuronal
def multiply_numbers(num1, num2):
    # Normalizar los números para que estén en el rango que la red neuronal ha aprendido
    num1_normalized = num1 / 10.0
    num2_normalized = num2 / 10.0
    # Predecir el resultado de la multiplicación
    result_normalized = multiplication_model.predict(np.array([[num1_normalized, num2_normalized]]))[0][0]
    # Desnormalizar el resultado
    result = result_normalized * 100.0
    return result

# Manejamos la entrada del usuario en el chatbot
def handle_user_input():
    global current_question, data
    user_input = user_input_entry.get()
    user_input_entry.delete(0, tk.END)

    # Verificamos si la entrada contiene palabras prohibidas
    if any(forbidden_word in user_input.lower() for forbidden_word in forbidden_words):
        chat_log.config(state=tk.NORMAL)
        chat_log.insert(tk.END, "Bot: ¡Advertencia! Has utilizado una palabra prohibida.\n")
        chat_log.config(state=tk.DISABLED)
        return  # No procesamos la entrada prohibida
    
    # Multiplicación de números
    if "multiplicar" in user_input.lower():
        # Pedir al usuario que ingrese dos números
        chat_log.config(state=tk.NORMAL)
        chat_log.insert(tk.END, "Bot: Ingresa el primer número: \n")
        user_input_entry.bind('<Return>', handle_input_number)
        return

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

# Función para manejar la entrada de números para la multiplicación
def handle_input_number(event):
    global current_question, data
    number1 = float(user_input_entry.get())
    user_input_entry.delete(0, tk.END)
    chat_log.insert(tk.END, f"Tu: {number1}\n")
    chat_log.insert(tk.END, "Bot: Ingresa el segundo número: \n")
    user_input_entry.bind('<Return>', lambda event, n=number1: handle_multiply(event, n))

# función para manejar la nueva pregunta y respuesta
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

# Función para manejar la multiplicación
def handle_multiply(event, number1):
    global current_question, data
    number2 = float(user_input_entry.get())
    user_input_entry.delete(0, tk.END)
    chat_log.insert(tk.END, f"Tu: {number2}\n")

    # Realizar la multiplicación utilizando la red neuronal
    result = multiply_numbers(number1, number2)

    chat_log.insert(tk.END, f"Bot: El resultado de {number1} * {number2} es aproximadamente {result:.2f}\n")
    chat_log.config(state=tk.DISABLED)

# Lista de palabras prohibidas
forbidden_words = ["tonto", "feo", "malo"]  # Agregamos las palabras que deseamos prohibir

# Cargamos datos del chatbot
data = load_data("data.json")

# Creamos ventana de la interfaz grafica
root = tk.Tk()
root.title("Chatbot")

# Etiquetas, botones y demas elementos de la GUI
intro_label = tk.Label(root, text="Consejo: Usa el boton enviar para insertar las preguntas y el boton enter de tu teclado para guardar las respuestas. Cuando multipliques y te pida los 2 números agrega los numeros con el boton enter de tu teclado", font=("Arial", 16))

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

# Bucle principal de la interfaz grafica
root.mainloop()
