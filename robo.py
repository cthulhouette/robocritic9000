import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pygame
from gtts import gTTS
import random
import tempfile
import os
import threading
import sys

# Initialize pygame mixer for audio playback
pygame.mixer.init()

# Helper function to get the correct resource path (works for both source and bundled exe)
def get_resource_path(relative_path):
    """ Get the resource path for bundled files (e.g. sounds). """
    if getattr(sys, 'frozen', False):
        # If running as a bundled executable
        return os.path.join(sys._MEIPASS, 'sounds', relative_path)
    else:
        # If running as a script
        return os.path.join(os.path.abspath("sounds"), relative_path)

# Load multiple sound effects from the "sounds" folder
sound_effects = [
    get_resource_path("bruh-sound-effect_WstdzdM.wav"),
    get_resource_path("ceeday-huh-sound-effect.wav"),
    get_resource_path("chinese-doit_qjQ0ubS.wav"),
    get_resource_path("vine-boom.wav"),
    get_resource_path("what-the-hell-meme-sound-effect.wav")
]

def play_random_sound():
    """Play a random sound effect."""
    try:
        sound_file = random.choice(sound_effects)
        pygame.mixer.music.load(sound_file)  # Load the sound file
        pygame.mixer.music.play()  # Play the sound
        while pygame.mixer.music.get_busy():  # Wait for the sound to finish
            pygame.time.Clock().tick(10)
    except Exception as e:
        print(f"Error while playing sound: {e}")

# Predefined sarcastic critique templates in Bengali and English
critique_templates = {
    "english": [
        "Oh wow, another 'groundbreaking' project. Groundbreakingly boring, perhaps?",
        "Your presentation has more buzzwords than actual substance. Impressive in its own way.",
        "This is so 'revolutionary' that I fell asleep trying to understand how.",
        "Your project is like a group assignment—one person's work, everyone else's name on it."
    ],
    "bangla": [
        "তোমার প্রজেক্টের ডিটেলস শোনার বদলে চালডালের ফোন কল ধরা ভালো",
        "বলা হয়ে থাকে যে, তোমার প্রজেক্ট দেখা লাগবে ভেবে আরও তিরিশ বছর আগেই কার্ট কোবেইন মাথায় শটগান ঠেকিয়ে ট্রিগার টানেন।",
        "তোমার কাজ দেখে মনে হচ্ছে যে তুমি ধনেপাতাকে উইড বলে চালিয়ে দাও। ধনেপাতা বিশ টাকা, উইড চারশো বিশ টাকা। পুরা দুই হাজার পার্সেন্ট লাভ।",
        "আই গেস এই প্রজেক্ট এক্সপেরিয়েন্স করার অকাত আমার নাই। জাস্ট শাট আপ।",
        "ভাই আপ্নে কি ছেলে ভার্সাস মেয়ে গ্রুপে এখনো অ্যাক্টিভ?",
        "স্যরি, বেকারদের কথার দাম নাই",
        "স্যরি বন্ধু, মিউজিক টেস্ট দেখে প্রজেক্টের নাম্বার দেওয়া হয় না।",
        "এই প্রজেক্ট আর ফ্রি ফায়ার একদম এক কাতারে পড়ে।",
        "ভাই মনে হয় খালি বাদশাহ আর ট্র্যাভিস স্কটের নাম্বার ওয়ান ফ্যান।"
    ]
}

def evaluate_project(description):
    """Evaluate the project based on the complexity and detail of the description."""
    innovativeness = 0
    feasibility = 0
    relevance = 0

    if "line following robot" in description.lower():
        innovativeness = 8
        feasibility = 8
        relevance = 8
    elif "autonomous vehicle" in description.lower():
        innovativeness = 9
        feasibility = 7
        relevance = 9
    elif "smart home system" in description.lower():
        innovativeness = 8
        feasibility = 7
        relevance = 8
    elif "machine learning-based chatbot" in description.lower():
        innovativeness = 8
        feasibility = 7
        relevance = 8
    else:
        innovativeness = 4
        feasibility = 4
        relevance = 4

    if len(description.split()) > 100:
        innovativeness += 1
        feasibility += 1
        relevance += 1

    innovativeness = min(max(4, innovativeness), 9)
    feasibility = min(max(4, feasibility), 9)
    relevance = min(max(4, relevance), 9)

    overall_score = (innovativeness + feasibility + relevance) / 3
    return innovativeness, feasibility, relevance, overall_score

def generate_critique(language):
    """Generate a random critique based on the selected language."""
    return random.choice(critique_templates[language])

def speak(text, language='en'):
    """Convert text to speech and play it using pygame."""
    try:
        tts = gTTS(text=text, lang=language)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
            tts.save(temp_file.name)
            temp_file_path = temp_file.name

        pygame.mixer.music.load(temp_file_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        os.remove(temp_file_path)
    except Exception as e:
        print(f"Error in text-to-speech: {str(e)}")

def speak_critique(language):
    """Generate and speak a critique in the selected language."""
    play_random_sound()
    critique = generate_critique(language)
    critique_label.config(text=critique)
    speak(critique, 'bn' if language == 'bangla' else 'en')
    play_random_sound()
    return critique

def on_submit():
    """Handles the button click event to process the input."""
    project_description = entry.get()
    if project_description.strip() == '':
        messagebox.showwarning("Warning", "Please enter a project description.")
        return

    innovativeness, feasibility, relevance, overall_score = evaluate_project(project_description)
    language = "bangla" if language_var.get() == "Bangla" else "english"

    # Show the evaluation results in the table format
    table.delete(*table.get_children())  # Clear previous entries in the table
    table.insert("", "end", values=("Innovativeness", innovativeness))
    table.insert("", "end", values=("Feasibility", feasibility))
    table.insert("", "end", values=("Relevance", relevance))
    table.insert("", "end", values=("Overall Score", round(overall_score, 2)))

    # Start the critique speech in a separate thread
    threading.Thread(target=speak_critique, args=(language,)).start()

def stop_speech():
    """Stop the speech playback."""
    pygame.mixer.music.stop()

def skip_critique():
    """Skip the current critique."""
    critique_label.config(text="Critique skipped.")
    stop_speech()

def start_process(event=None):
    """Start the process (submit the project description)."""
    on_submit()

def stop_process(event=None):
    """Stop the speech."""
    stop_speech()

# Initialize the GUI window
root = tk.Tk()
root.title("RoboCritic9000")

root.geometry("700x700")
root.configure(bg="#f5f5f5")

# Apply a modern style to ttk widgets
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12), padding=10)
style.configure("TLabel", font=("Helvetica", 14))
style.configure("Treeview", font=("Helvetica", 12), rowheight=30, padding=5)
style.configure("Treeview.Heading", font=("Helvetica", 14, "bold"))

# Frame for the input section
input_frame = tk.Frame(root, bg="#f5f5f5")
input_frame.pack(pady=20, padx=20)

# Add input field and button
entry_label = tk.Label(input_frame, text="Enter your project description:", bg="#f5f5f5")
entry_label.pack(pady=10)

entry = tk.Entry(input_frame, width=50, font=("Helvetica", 12), bd=2, relief="solid")
entry.pack(pady=10)

language_var = tk.StringVar(value="English")
language_label = tk.Label(input_frame, text="Select language:", bg="#f5f5f5")
language_label.pack(pady=5)

language_menu = ttk.Combobox(input_frame, textvariable=language_var, values=["English", "Bangla"], state="readonly", width=20)
language_menu.pack(pady=5)

submit_button = ttk.Button(input_frame, text="Submit Project", command=start_process)
submit_button.pack(pady=20)

# Table for the evaluation results
table_frame = tk.Frame(root, bg="#f5f5f5")
table_frame.pack(pady=20, padx=20)

table = ttk.Treeview(table_frame, columns=("Criteria", "Score"), show="headings", height=6)
table.heading("Criteria", text="Criteria")
table.heading("Score", text="Score")
table.pack()

# Label to display the critique
critique_frame = tk.Frame(root, bg="#f5f5f5")
critique_frame.pack(pady=20)

critique_label = tk.Label(critique_frame, text="", wraplength=600, font=("Helvetica", 12), bg="#f5f5f5", justify="left")
critique_label.pack(pady=10)

# Buttons for controlling the speech playback
control_frame = tk.Frame(root, bg="#f5f5f5")
control_frame.pack(pady=20)

skip_button = ttk.Button(control_frame, text="Skip Critique", command=skip_critique)
skip_button.pack(side="left", padx=10)

stop_button = ttk.Button(control_frame, text="Stop Speech", command=stop_process)
stop_button.pack(side="right", padx=10)

# Run the application
root.mainloop()
