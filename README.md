RoboCritic9000

RoboCritic9000 is an interactive project evaluation tool designed to provide automated feedback on technical descriptions. Users input their project descriptions, and the system evaluates them based on key criteria such as innovativeness, feasibility, and relevance. The application generates a score for each criterion and offers a sarcastic critique, delivered in either English or Bangla. With playful sound effects and text-to-speech functionality, RoboCritic9000 adds a humorous twist to project reviews.

<img width="871" height="911" alt="image" src="https://github.com/user-attachments/assets/54bab47a-ee73-48db-aed5-a49e00f866e3" />


Description

1. User Input:

The user enters a project description in the provided text field.
The language is selected via a dropdown menu (English or Bangla).


2. Evaluation Process:

The project description is analyzed to assess three criteria: Innovativeness, Feasibility, and Relevance.
Based on keywords and the length of the description, the system assigns scores for each criterion.
The scores are calculated and an overall score is derived by averaging the three criteria.


3. Sound Effects:

Random sound effects are played before and after generating the critique, adding an element of humor.
Sound files are loaded dynamically from a sounds folder, ensuring portability.


4. Critique Generation:

A sarcastic critique is randomly chosen from predefined templates in English or Bangla.
The critique is displayed on the screen and read out loud using text-to-speech (TTS).


5. Text-to-Speech:

The critique text is converted to speech using the Google Text-to-Speech (gTTS) library.
The speech is played via pygame, and a temporary MP3 file is generated for each critique.


6. GUI Interface:

The user interface is built with Tkinter, providing fields for input, displaying results in a table, and showing the critique.
Buttons allow the user to submit the project description, skip the critique, or stop the speech.


7. Threading:

The critique speech is played in a separate thread, allowing the user to continue interacting with the application without interruption.
