import nltk
import random
from nltk.corpus import words
from wordle import WordleClone


class WordleSolver:

	def init_word_list(self):
		nltk.download('words', quiet=True)
		return [word.upper() for word in words.words() if len(word) == 5 and word.isalpha()]

	def get_letter_freq(self, word_list):
		letter_freq = {}
		for word in word_list:
			for letter in word:
				if letter in letter_freq:
					letter_freq[letter] += 1
				else:
					letter_freq[letter] = 1
		return self.sort_letter_freq_dict(letter_freq)

	def get_letter_freq_by_pos(self, word_list):
		pos_freq = [{}, {}, {}, {}, {}]
		for w in word_list:
			for i in range(5):
				if w[i] in pos_freq[i]:
					pos_freq[i][w[i]] += 1
				else:
					pos_freq[i][w[i]] = 1
		return pos_freq

	def sort_letter_freq_dict(self, letter_freq_dict):
		rslt = [(k, v) for k, v in letter_freq_dict.items()]
		return sorted(rslt, key=lambda x: x[1], reverse=True)

	# filter by known letter location
	def filter_by_letter_loc(self, letter, location, word_list):
		return [_ for _ in word_list if _[location] == letter]

	# filter by known letter, deny-list location
	def filter_by_letter_neg_loc(self, letter, neg_loc_list, word_list):
		for loc in neg_loc_list:
			word_list = [_ for _ in word_list if letter in _ and _[loc] != letter]
		return word_list

	def filter_by_unused_letter(self, letter, word_list):
		return [_ for _ in word_list if letter not in _]
	
	def generate_guess_word(self, word_list, allow_repeat):
		word_list = []
		for i in range(5):
			letter_freq = self.get_letter_freq_by_pos(word_list)
			letter_freq_list = self.sort_letter_freq_dict(letter_freq[i])
			if not allow_repeat:
				letter_freq_list = [_ for _ in letter_freq_list if _[0] not in word_list]
			letter_choice = random.choice([_[0] for _ in letter_freq_list][:3]) 
			word_list.append(letter_choice)
			word_list = self.filter_by_letter_loc(letter_choice, i, word_list)
		return ''.join(word_list)

	def get_guess_word(self, word_list, allow_repeat=True):
		for _ in range(5):
			try:
				return self.generate_guess_word(word_list, allow_repeat)
			except Exception as e:
				continue

	def apply_feedback_to_word_list(self, guess, feedback, word_list):
		for i in range(5):
			if feedback[i] == 'G':
				word_list = self.filter_by_letter_loc(guess[i], i, word_list)
			elif feedback[i] == 'Y':
				word_list = self.filter_by_letter_neg_loc(guess[i], [i], word_list)
			else:
				word_list = self.filter_by_unused_letter(guess[i], word_list)
		return word_list

	def play_wordle(self):
		viable_words = self.init_word_list()
		wc = WordleClone()
		attempt = 1
		guess = self.get_guess_word(viable_words, allow_repeat=False)
		while True:
			print(guess)
			feedback = wc.guess_word(guess)
			print(feedback)
			if isinstance(feedback, str) and feedback.startswith('Congratulations!'):
				print('Congratulations!')
				return (True, attempt)
			elif isinstance(feedback, str) and feedback.startswith('Game Over!'):
				print('Game Over!')
				return (False, -1)
			viable_words = self.apply_feedback_to_word_list(guess, feedback, viable_words)
			guess = self.get_guess_word(viable_words)


if __name__ == '__main__':
	solver = WordleSolver()
	solver.play_wordle()
