import random

class WordleClone:
	def __init__(self):
		"""Initialize the WordleClone game with a list of five-letter words."""
		self.word_list = self.get_words()
		self.target_word = random.choice(self.word_list)
		self.max_attempts = 6
		self.attempts = []
		
	def get_words(self):
		word_file = 'words.txt'
		with open(word_file, 'r') as f:
			words = f.readlines()
		return [_.strip().upper() for _ in words]

	def guess_word(self, guess):
		"""Make a guess and return feedback on the guess."""
		if len(guess) != len(self.target_word):
			return f"Word must be {len(self.target_word)} letters long."

		guess = guess.upper()
		feedback = []

		for i, char in enumerate(guess):
			if char == self.target_word[i]:
				feedback.append("G")  # Correct letter in the correct position
			elif char in self.target_word:
				feedback.append("Y")  # Correct letter in the wrong position
			else:
				feedback.append("_")  # Incorrect letter

		self.attempts.append((guess, feedback))

		if guess == self.target_word:
			return "Congratulations! You've guessed the word!"
		elif len(self.attempts) >= self.max_attempts:
			return f"Game Over! The word was {self.target_word}."
		else:
			return feedback

	def display_attempts(self):
		"""Display all previous attempts and their feedback."""
		for guess, feedback in self.attempts:
			print(f"{guess} -> {''.join(feedback)}")

	def reset_game(self):
		"""Reset the game with a new target word."""
		self.target_word = random.choice(self.word_list)
		self.attempts = []

# Example usage:
if __name__ == "__main__":
	game = WordleClone()

	print("Welcome to WordleClone!")
	while len(game.attempts) < game.max_attempts:
		user_guess = input("Enter your guess: ")
		feedback = game.guess_word(user_guess)
		game.display_attempts()
		if "Congratulations" in feedback or "Game Over" in feedback:
			print(feedback)
			break
			# reset_input = input("Play again? (y/n) >")
			# if reset_input.lower() == 'y':
			# 	game.reset_game()
			# else:
			# 	break
			
