import random
import re
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI 

class WordleSolver:
    def __init__(self, game_instance, api_key):
        """
        Initialize the WordleSolver with a WordleClone game instance and an API key for LangChain.
        """
        self.game = game_instance
        self.api_key = api_key
        self.llm = OpenAI(openai_api_key=self.api_key)

    def parse_response(self, response):
        pattern = '[A-Z]{5}'
        match = re.search(pattern, response)
        if match:
            rslt = match.group().replace('%', '')
            if len(rslt) != 5:
                raise ValueError(f'Invalid response provided: {response}')
            return rslt
        raise ValueError(f'Invalid response provided: {response}')

    def make_initial_guess(self):
        """
        Use LangChain to make a strategic first guess.
        """
        prompt = PromptTemplate(
            input_variables=["word_length"],
            template=(
                "You are playing Wordle. The goal is to guess the secret word, which is {word_length} letters long. "
                "Suggest the best strategic first word to guess, considering the rules of the game and the need to maximize information for the next guesses. "
                "Only return the single word as your response, without any additional text."
                "Return your answer in the following format: 'The best word to guess would be APPLE', where APPLE is your guess."
                "Be sure that your guess is in all upper case letters."
            )
        )
        full_prompt = prompt.format(word_length=self.game.word_length)
        response = self.llm(full_prompt).strip()
        print(f'raw guess: {response}')
        return self.parse_response(response)

    def suggest_next_word(self, feedback, guess):
        """
        Use LangChain to suggest the next word to guess based on the feedback and previous guess.
        """
        prompt = PromptTemplate(
            input_variables=["feedback", "guess", "word_length"],
            template=(
                "You are playing Wordle. The goal is to guess the secret word, which is {word_length} letters long. "
                "You are provided with the following feedback mechanism: \n"
                "- 'G' means the letter is correct and in the right position.\n"
                "- 'Y' means the letter is correct but in the wrong position.\n"
                "- '_' means the letter is not in the word.\n\n"
                "Here is the feedback from the last guess:\n"
                "Guess: {guess}\n"
                "Feedback: {feedback}\n\n"
                "Don't pick a word you've already tried."
                "Incorporate the feedback to make an informed guess."
                "Return your answer in the following format: 'The best word to guess would be APPLE', where APPLE is your guess."
                "Be sure that your guess is in all upper case letters."
            )
        )
        full_prompt = prompt.format(feedback=feedback, guess=guess, word_length=self.game.word_length)
        response = self.llm(full_prompt).strip()
        print(f'raw guess: {response}')
        return self.parse_response(response)

    def solve(self):
        """
        Attempt to solve the WordleClone game by iteratively guessing words and analyzing feedback.
        """
        # Make the initial guess
        # guess = random.choice(self.game.word_list)
        guess = self.make_initial_guess()
        feedback = None

        while len(self.game.attempts) < self.game.max_attempts:
            # Make the guess and retrieve feedback
            feedback = self.game.guess_word(guess)
            print(f"Guess: {guess}")
            self.game.display_attempts()

            # Check for win or game over
            if "Congratulations" in feedback or "Game Over" in feedback:
                print(feedback)
                break

            # debugging
            print('-' * 25)
            print(f'feedback:\n{feedback}')
            print('-' * 25)
            input('press any key to proceed >')

            # Get the next suggested word based on feedback
            guess = self.suggest_next_word(feedback=feedback, guess=guess)

# Example Usage
if __name__ == "__main__":
    from wordle import WordleClone  # Import the WordleClone class defined above
    import os

    openai_api_key = os.getenv('OPENAI_API_KEY')

    # Initialize game and solver
    game = WordleClone()
    solver = WordleSolver(game_instance=game, api_key=openai_api_key)

    # Solve the game
    solver.solve()
