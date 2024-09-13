import os
import time

import google.generativeai as genai
from rich.console import Console
from rich.table import Table
from rich.spinner import Spinner
from rich.live import Live
from create_prompt import laurence_v25

os.system('clear')

genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
  system_instruction="You are a roleplaying chatbot. You fully embrace the role given to you and before responding you first write out three sentences on which specific parts of the character's profile relates to the current conversation. Then on another line, write your response to the current conversation in quotes.",
)
chat_session = model.start_chat(history=laurence_v25())


# Initialize the console
console = Console()

def typewriter_effect(text, delay=0.01):
    for char in text:
        console.print(char, end='')  # Print each character without new line
        time.sleep(delay)  # Delay between each character to simulate typing

# Function to simulate Laurence's dialogue with a spinner
def add_laurence_dialogue(console, user_input):
    # First, show "Laurence:" with a spinner
    # spinner = Spinner("dots", text="Typing...")
    with console.status("", spinner="dots"):
        response = chat_session.send_message(user_input)
    # After 1 second, replace the spinner with Laurence's actual dialogue
    console.print(f"    Laurence: ", end="", style="bold blue")
    parts = response.text.split('"')
    output = parts[1]
    # reasoning_done = False
    # for chunk in response:
    #     if '"' in chunk.text:
    #         reasoning_done = True
         
    typewriter_effect(output)
    console.print()
    console.print()


# Function to add "You" dialogue
def add_your_dialogue(console):
    user_input = console.input("        [bold green] You: ")  # Get input from the user
    # live.update(f"     You: {user_input}")
    console.print()
    return user_input

print("\n\n\n\n")
console.print(f"[bold blue]    Laurence:[/bold blue] Salut, c'est Laurence. I speak English too! Say 'goodbye' whenever you want to stop chatting.")
console.print()

while True:
# Your response
    user_input = add_your_dialogue(console)  # Takes input from the user

    if "goodbye" in user_input:
        break

# Laurence's second line with a 1-second spinner
    add_laurence_dialogue(console, user_input)


with console.status("", spinner="dots"):
    response = chat_session.send_message("Stop playing the role of Laurence. Instead, what if I would like to make an AI chatbot of myself given this conversation. If you were to make a chatbot that mimics me, give me 3-5 of my personality traits and then ask me 2-3 deeply personal questions. Things that you couldn't find out online but that would help you make a better copy of me. Start your response with 'If I were to make a chatbot of you' and then give your response. After the personal questions, ask if I think this would be enough to copy me. Then on a new line just ask 'what would be missing from the machine?'.")
# After 1 second, replace the spinner with Laurence's actual dialogue
console.print(f"    Laurence: ", end="", style="bold blue")
typewriter_effect(response.text)
console.print()

