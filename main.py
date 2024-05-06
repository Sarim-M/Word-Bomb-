import enchant
import random
import pygame
from bomb import Bomb
from start import Start

pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Arial', 20)
my_starter_font = pygame.font.SysFont('Bebas Nueue', 40)
pygame.display.set_caption("Word Bomb")
b = Bomb
s = Start

size = (800, 600)
screen = pygame.display.set_mode(size)

def pick_word():
  words = []
  f = open("letters", "r")
  for w in f:
    words.append(w.rstrip())
  r = random.randint(0, len(words) - 1)
  f.close()
  random_word = words[r]
  return random_word.upper()

def word_check(word):
  word_checker = enchant.Dict("en_US")
  word_legibility = word_checker.check(word)
  if word_legibility == True:
    for i in chosen_words:
      if i == word:
        return False
  return True


#messages to be blitten
start_message = my_starter_font.render("Welcome to Word Bomb!", True, (255,255,255))

#variables
chosen_words = []
hearts = 3

#program switches
run = True
GameStart = True


while run and GameStart:
  x = 0
  guessed_word_checker = []
  word = []
  correct_letters = 0
  picked_word = pick_word()
  print("Write a word that you haven't already used and includes:")
  print(picked_word)
  for letters in picked_word:
    word.append(letters)
  guessed_word = input("Enter your word here: ")
  guessed_word = guessed_word.upper()
  legible_word = word_check(guessed_word)
  if legible_word == True:
    for letters in guessed_word:
      guessed_word_checker.append(letters)
    for i in guessed_word_checker:
      guessed_word_checker_list_length = len(guessed_word_checker)
    try:
      if i == word[x] and x <= guessed_word_checker_list_length:
        correct_letters = correct_letters + 1
      if correct_letters != len(word):
       x = x + 1
    except IndexError as e:
     print("Loading....")
    except Exception as e:
     print("An error has occurred:", e)
    if correct_letters >= len(word):
      chosen_words.append(guessed_word)
      score = score + 10
      print(score)
      print("Correct!")
    else:
     print("Thats not right!")
     hearts = hearts - 1


  else:
   print("That's not right! ")
   hearts = hearts - 1




#BLIT

