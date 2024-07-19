from tkinter import Tk, Label, Button, Entry, Toplevel, END
import random as rng


class Hangman:
    """
    Represents an instance of the Hangman game.
    """
    def __init__(self) -> None:
        """
        Initializes a Hangman object, sets up ui elements and attributes.
        """
        self.root: Tk = Tk()
        self.root.geometry("300x250+500+200")
        self.root.resizable(False, False)
        self.root.title("Hangman")

        self.FONT: str = "Courier New"
        self.bg_color: str = "#ddd"

        self.root.config(background=self.bg_color)

        self.attempts: int = 6
        self.attempts_text: Label = Label(self.root, font=(self.FONT, 13),
                                          text=f"Attempts Left: {self.attempts}",
                                          background=self.bg_color)
        self.attempts_text.place(relx=0.5, rely=0.15, anchor="center")

        self.word_text: Label = Label(self.root, font=(self.FONT, 20),
                                      background=self.bg_color)
        self.word_text.place(relx=0.5, rely=0.32, anchor="center")

        self.guess_text: Label = Label(self.root, text="Guessed letters: ", 
                                       font=(self.FONT, 10), 
                                       background=self.bg_color)
        self.guess_text.place(relx=0.5, rely=0.55, anchor="center")

        self.entry_label: Label = Label(self.root, text="Guess a Letter: ",
                                        font=(self.FONT, 10),
                                        background=self.bg_color)
        self.entry_label.place(relx=0.4, rely=0.75, anchor="center")

        def validate(P):
            if len(P) == 0:
                return True
            elif len(P) == 1 and P.isalpha() and \
            P.upper() not in self.attempt_letters:
                return True
            else:
                return False
            
        vcmd = (self.root.register(validate), '%P')

        self.letter_entry: Entry = Entry(self.root, font=(self.FONT, 10),
                                         width=5, justify="center",
                                         validate="all",
                                         validatecommand=vcmd)
        self.letter_entry.place(relx=0.7, rely=0.75, anchor="center")
        
        self.submit_button: Button = Button(self.root, font=(self.FONT, 8),
                                            text="Submit", command=self.submit)
        self.submit_button.place(relx=0.5, rely=0.9, anchor="center")


        self.correct_word: str = self.set_correct_word()
        self.current_guess: list[str] = ['_'] * len(self.correct_word)
        self.update_word_text()
        self.attempt_letters: list[str] = []
        self.update_guess_text()

        self.exit_mode: str = "Q"

        self.root.mainloop()


    def set_correct_word(self) -> str:
        """
        Selects and a random word from the text file and sets it as the
        correct answer.

        :return: the word to be guessed.
        """
        with open("hangman_words.txt", "r") as file:
            words: list[str] = file.readlines()
            correct_word: str = rng.choice(words).strip()
        
        return correct_word
    
    def update_word_text(self) -> None:
        """
        Update the ui for the word.
        """
        new_text: str = ' '.join(self.current_guess)
        self.word_text.config(text=new_text)


    def update_guess_text(self) -> None:
        """
        Update the ui for the guessed letters.
        """
        new_text: str = ""
        for idx, char in enumerate(self.attempt_letters, 1):
            if idx % 15 == 0:
                new_text += f"{char}," + "\n"
            else:
                new_text += f"{char},"

        self.guess_text.config(text=f"Guessed Letters:\n{new_text.strip(',')}")


    def submit(self) -> None:
        """
        Submit the letter currently entered in the text entry as a guess
        and evaluate it.
        """
        guess: str = self.letter_entry.get().lower()
        correct: str = self.correct_word

        if guess in correct:
            for idx in range(len(correct)):
                if correct[idx] == guess:
                    self.current_guess[idx] = guess.upper()
            self.update_word_text()
        else:
            if guess.upper() not in self.attempt_letters:
                self.attempt_letters.append(guess.upper())
                self.update_guess_text()

                self.attempts -= 1
                self.attempts_text.config(text=f"Attempts Left: {self.attempts}")

        self.letter_entry.delete(0, END)

        # check whether the game has ended
        win: bool = self.check_for_win()
        if win:
            self.end_state(True)
            self.root.destroy()
        else:
            if self.attempts == 0:
                self.end_state(False)
                self.root.destroy()


    def check_for_win(self) -> bool:
        """
        Check whether the game has been won.
        
        :return: True -> won, False -> not won
        """
        correct: str = self.correct_word
        current: str = ''.join(self.current_guess).lower()
        return correct == current  
    
    def end_state(self, won: bool) -> None:
        """
        Launch a pop-up window informing the player of either a win on loss,
        as well as provide options to start a new game or exit the application.

        :param won: whether the game was won or not.
        """
        end_screen: Toplevel = Toplevel()
        end_screen.geometry("200x100+550+270")
        end_screen.resizable(False, False)
        title: str = "WIN!" if won else "LOSE!"
        end_screen.title(title)
        end_screen.grab_set()

        status_text: Label = Label(end_screen, text=f"YOU {title}",
                                   font=(self.FONT, 15))
        status_text.place(relx=0.5, rely=0.35, anchor="center")

        def new_game():
            self.exit_mode = "G"
            end_screen.destroy()

        new_button: Button = Button(end_screen, text="New Game",
                                    font=(self.FONT, 8),
                                    command=new_game)
        new_button.place(relx=0.3, rely=0.7, anchor="center")

        def quit_game():
            end_screen.destroy()

        quit_button: Button = Button(end_screen, text="Quit",
                                     font=(self.FONT, 8),
                                     command=quit_game)
        quit_button.place(relx=0.7, rely=0.7, anchor="center")

        self.root.wait_window(end_screen)
        

if __name__ == "__main__":
    game: Hangman = Hangman()
    while game.exit_mode == "G":
        game = Hangman()