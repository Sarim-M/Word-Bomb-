import enchant
import random
import pygame
from bomb import Bomb
from start import Start
import time

pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Arial', 20)
my_starter_font = pygame.font.SysFont('Bebas Nueue', 60)
pygame.display.set_caption("Word Bomb")

b = Bomb(230,50)
s = Start(0,220)


score = 0
size = (800, 600)
screen = pygame.display.set_mode(size)
start_time = time.time()

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
picked_word_display = my_starter_font.render("LOADING PREFIX/SUFFIX...", True, (255,255,255))
guessed_word_display = my_starter_font.render("ENTER WORD HERE", True, (255,255,255))
guessing_message = my_font.render("Write a word that you haven't already used and includes:", True, (255,255,255))
time_message = my_font.render("Loading...", True, (255,255,255))
score_message = my_font.render("Score: 0", True, (255,255,255))
hearts_message = my_font.render("Hearts = 3", True, (255,255,255))

#variables
chosen_words = []
hearts = 3

#program switches
run = True
GameStart = False
GuessedYet = False
usage = 0





while run:
  for event in pygame.event.get():

    if event.type == pygame.QUIT:  # If user clicked close
        run = False
    if event.type == pygame.MOUSEBUTTONUP and not GameStart:
        pos = pygame.mouse.get_pos()
        if s.rect.collidepoint(pos):
             GameStart = True
             text_box = pygame.Rect(270, 530, 200, 40)
             text_box_color = (0, 0, 0)
             text_box_active = True
             file_name = "a"
             file_name_message = my_font.render(file_name, True, (0, 0, 0))
    if event.type == pygame.KEYUP and text_box_active:
        if event.key == 8:
            file_name = file_name[0:len(file_name) - 1]
            file_name_message = my_font.render(file_name, True, (0, 0, 0))
        else:
            if event.key == 9:
                text_box_active = False
            else:
                file_name += event.unicode
                file_name_message = my_font.render(file_name, True, (0, 0, 0))
    if event.type == pygame.MOUSEBUTTONUP:
        # activate the text box
        if text_box.collidepoint(event.pos):
            text_box_color = (0, 0, 255)
            text_box_active = True
        # de-activate the text box
        else:
            text_box_color = (0, 0, 0)
            text_box_active = False


  if GameStart:
   x = 0
   guessed_word_checker = []
   word = []
   correct_letters = 0
   current_time = (int(11 - (time.time() - start_time)))
   if current_time >= 0:
     current_time = str(current_time)
     time_message = my_font.render(current_time, True, (255,255,255))
   KeyPressed = False


   if not GuessedYet:
     picked_word = pick_word()
     picked_word_display = my_starter_font.render(picked_word, True, (255,255,255))
     GuessedYet = True
     for letters in picked_word:
         word.append(letters)
         print(word)




   file_name = file_name.upper()
   keys = pygame.key.get_pressed()
   for event in pygame.event.get():
       if event.type == pygame.KEYUP:
           if event.key == pygame.K_TAB:
            GuessedYet = True
            KeyPressed = True
            print(file_name)
            legible_word = word_check(file_name)
            if legible_word == True:
            silly = True
            for letters in file_name:
             guessed_word_checker.append(letters)
             print(guessed_word_checker)
            for i in guessed_word_checker:
              guessed_word_checker_list_length = len(guessed_word_checker)
              print(guessed_word_checker_list_length)
              try:
               if i == word[x] and x <= guessed_word_checker_list_length:
                correct_letters = correct_letters + 1
                print("Correct letters first check: " + str(correct_letters))
               if correct_letters != len(word):
                 x = x + 1
              except IndexError as e:
               print("Loading....")
              except Exception as e:
               print("An error has occurred:", e)
            print("Correct letters" + str(correct_letters))
            print("Len(word): " + str(len(word)))
            if correct_letters >= (len(word)) and int(current_time) >= 0:
             chosen_words.append(file_name)
             score = score + 10
             score_message = my_font.render("Score: " + str(score), True, (255,255,255))
             print(score)
             print("Correct!")
             start_time = time.time()
             GuessedYet = False
      else:
       print("Thats not right!")
       print("teehee")
       print(correct_letters)
       hearts = hearts - 1
       hearts_message = my_font.render("Hearts: " + str(hearts), True, (255,255,255))
       GuessedYet = False
      print(silly)




    else:
      if not silly:
         print("That's not right! ")
         print("hoohaa")
         hearts = hearts - 1
         hearts_message = my_font.render("Hearts: " + str(hearts), True, (255, 255, 255))
         GuessedYet = False
    print(silly)
    silly = False
  screen.fill((245, 14, 14))
  if not GameStart:
      screen.blit(start_message, (160, 160))
      screen.blit(s.image, s.rect)
  if GameStart:
      screen.blit(picked_word_display, (350, 60))
      screen.blit(guessing_message,(200,30))
      screen.blit(b.image, b.rect)
      pygame.draw.rect(screen, text_box_color, text_box, 3)
      screen.blit(file_name_message, (100,50))
      screen.blit(time_message, (100,60))
      screen.blit(score_message, (100,70))
      screen.blit(hearts_message, (100,90))
  pygame.display.update()







