from tkinter import *
from tkinter import ttk, filedialog, messagebox
import pyttsx3
import speech_recognition as sr
import os

sapi = pyttsx3.init()
rate = sapi.getProperty('rate')
sapi.setProperty('rate', 125)

class TextToSpeech:
    def __init__(self, root):
        self.root = root
        blank_space = "Ahmad Luthfi Amirulloh"
        self.root.title(1 * blank_space )
        self.root.resizable(width=False, height=False)
        self.root.geometry("800x600+0+0")

        MainFrame = Frame(self.root, bd=7, width=780, height=580, relief=RIDGE, bg="cadetblue")
        MainFrame.grid()
        TitleFrames = Frame(MainFrame, bd=7, width=760, height=100, relief=RIDGE)
        TitleFrames.grid(row=0, column=0)
        TitleFrames = Frame(TitleFrames, bd=7, width=760, height=100, relief=RIDGE, bg="cadetblue")
        TitleFrames.grid(row=0, column=0, padx=8)
        TextFrame = Frame(MainFrame, bd=10, width=760, height=400, relief=RIDGE, bg="cadetblue")
        TextFrame.grid(row=1, column=0)
        LeftFrame = Frame(TextFrame, bd=10, width=500, height=400, relief=RIDGE)
        LeftFrame.grid(row=0, column=0)
        ButtonFrame = Frame(TextFrame, bd=10, width=260, height=400, relief=RIDGE)
        ButtonFrame.grid(row=0, column=1)

        self.lblTitle = Label(TitleFrames, font=('arial', 24, 'bold'), text="Pengenalan Ucapan", bd=7, bg="cadetblue")
        self.lblTitle.grid(row=0, column=0, padx=10)

        self.txtEnterText = Text(LeftFrame, height=12, width=40, bg="light yellow", font=('Courier', 14, 'bold'))
        self.txtEnterText.grid(row=0, column=0)

        def TextSapi():
            TextInput = self.txtEnterText.get("1.0", "end-1c")
            sapi.say(TextInput)
            sapi.runAndWait()

        def ChangeVoice():
            TextInput = self.txtEnterText.get("1.0", "end-1c")
            voices = sapi.getProperty('voices')
            for voice in voices:
                sapi.setProperty('voice', voice.id)
                sapi.say(TextInput)
            sapi.runAndWait()

        def LoadAndReadFile():
            file_path = filedialog.askopenfilename(title="Select a text file", filetypes=(("Text files", ".txt"), ("All files", ".*")))
            if file_path:
                try:
                    with open(file_path, 'r') as file:
                        text_content = file.read()
                        self.txtEnterText.delete("1.0", END)
                        self.txtEnterText.insert("1.0", text_content)
                except FileNotFoundError:
                    messagebox.showerror("Error", "File not found.")
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred: {e}")

        def SaveAsWav():
            file_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV files", "*.wav"), ("All files", "*.*")])
            if file_path:
                TextInput = self.txtEnterText.get("1.0", "end-1c")
                sapi.save_to_file(TextInput, file_path)
                sapi.runAndWait()
                messagebox.showinfo("Success", f"File saved as {file_path}")

        def OpenAppWithVoice():
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                messagebox.showinfo("Listening", "Silakan bicara sekarang...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)
            try:
                command = recognizer.recognize_google(audio, language="id-ID")
                self.txtEnterText.delete("1.0", END)
                self.txtEnterText.insert("1.0", command)
                if "buka notepad" in command.lower():
                    os.system("notepad.exe")
                elif "buka kalkulator" in command.lower():
                    os.system("calc.exe")
                else:
                    messagebox.showinfo("Info", "Perintah tidak dikenali.")
            except sr.UnknownValueError:
                messagebox.showerror("Error", "Tidak dapat mengenali suara.")
            except sr.RequestError as e:
                messagebox.showerror("Error", f"Could not request results; {e}")

        Button(ButtonFrame, pady=1, bd=4, font=('arial', 16, 'bold'), padx=10, width=15, height=2, text="Baca Teks", command=TextSapi).grid(row=0, column=0, padx=2)
        Button(ButtonFrame, pady=1, bd=4, font=('arial', 16, 'bold'), padx=10, width=15, height=2, text="Unggah File", command=LoadAndReadFile).grid(row=1, column=0, padx=2)
        Button(ButtonFrame, pady=1, bd=4, font=('arial', 16, 'bold'), padx=10, width=15, height=2, text="Ubah Suara", command=ChangeVoice).grid(row=2, column=0, padx=2)
        Button(ButtonFrame, pady=1, bd=4, font=('arial', 16, 'bold'), padx=10, width=15, height=2, text="Simpan", command=SaveAsWav).grid(row=3, column=0, padx=2)
        Button(ButtonFrame, pady=1, bd=4, font=('arial', 16, 'bold'), padx=10, width=15, height=2, text="Buka Aplikasi", command=OpenAppWithVoice).grid(row=4, column=0, padx=2)

if __name__ == "__main__":
    root = Tk()
    application = TextToSpeech(root)
    root.mainloop()
