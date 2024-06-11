import enchant
import random
import pygame
import time
from bomb import Bomb
from start import Start
from heart import Heart
from broken_heart import XHeart
from explosion import Explode

#Text
pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Arial', 20)
my_starter_font = pygame.font.SysFont('impact', 60)
my_super_font = pygame.font.SysFont('impact', 250)
pygame.display.set_caption("Word Bomb")


b = Bomb(700,100)
s = Start(550,350)
h_one = Heart(1750,100)
h_two = Heart(1610, 100)
h_three = Heart(1470, 100)
xh_one = XHeart(1750,100)
xh_two = XHeart(1610,100)
xh_three = XHeart(1470,100)
e = Explode(500,200)

#preparations
score = 0
size = (1920, 1040)
screen = pygame.display.set_mode(size)
start_time = time.time()

#functions
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
picked_word_display = my_starter_font.render("EMPTY TEXT BOX TO BEGIN", True, (255,255,255))
guessed_word_display = my_starter_font.render("ENTER WORD HERE", True, (255,255,255))
guessing_message = my_font.render("Write a word that you haven't already used and includes:", True, (255,255,255))
time_message = my_font.render("Loading...", True, (255,255,255))
text_box_warning = my_starter_font.render("EMPTY TEXT BOX TO CONTINUE", True, (255,255,255))
score_message = my_starter_font.render("Words: 0", True, (255,255,255))
hearts_msg = my_font.render("hi", True, (255,255,255))
game_over_message = my_super_font.render("GAME OVER", True, (255,255,255))

#variables
chosen_words = []
hearts = 3
word = []

#program switches
run = True
game_start = False
guessed_yet = False
warning = False
silly = False
game_over = False
usage = 0
current_word = "ora"



#MAIN LOOP
while run:
  for event in pygame.event.get():

    if event.type == pygame.QUIT:  # If user clicked close
      run = False
    if event.type == pygame.MOUSEBUTTONUP and not game_start:
      pos = pygame.mouse.get_pos()
      if s.rect.collidepoint(pos):
        game_start = True
        text_box = pygame.Rect(600, 850, 700, 100)
        text_box_color = (0, 0, 0)
        text_box_active = True
        file_name = "a"
        file_name_message = my_font.render(file_name, True, (0, 0, 0))
    if event.type == pygame.KEYUP and text_box_active and not game_over:
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


  #once game begins
  if game_start:
    x = 0
    guessed_word_checker = []
    correct_letters = 0
    current_time = (int(21 - (time.time() - start_time)))
    if current_time >= 0:
      current_time = str(current_time)
      time_message = my_font.render(current_time, True, (255,255,255))
    key_pressed = False

    if usage == 1:
      usage = 0

    if usage == 0 and not guessed_yet and len(file_name) == 0:
      word = []
      picked_word = pick_word()
      picked_word_display = my_starter_font.render(picked_word, True, (255,255,255))
      guessed_yet = True
      for letters in picked_word:
        word.append(letters)
    if len(file_name) == 0:
      warning = False

    file_name = file_name.upper()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_TAB] and not key_pressed and file_name != current_word:
      x = 0
      current_word = file_name
      warning = False
      guessed_yet = True
      key_pressed = True
      legible_word = word_check(file_name)
      if legible_word == True:
        silly = True
        for letters in file_name:
          guessed_word_checker.append(letters)
        for i in guessed_word_checker:
          guessed_word_checker_list_length = len(guessed_word_checker)
          try:
            if i == word[x] and x <= guessed_word_checker_list_length:
              correct_letters = correct_letters + 1
            else:
              print("WORD AT INDEX " + str(x) + ": " + str(word[x]))
              print("no correct letter deteced: ", str(i) + " " + str(word[x]))
            if correct_letters != len(word):
              x = x + 1
          except IndexError as u:
            print("Loading....")
          except Exception as u:
            print("An error has occurred:", u)
        if correct_letters >= (len(word)) and int(current_time) >= 0:
          chosen_words.append(file_name)
          score = score + 1
          score_message = my_starter_font.render("Words: " + str(score), True, (255,255,255))
          start_time = time.time()
          guessed_yet = False
          warning = True
        else:
          hearts = hearts - 1
          hearts_msg = my_font.render(str(hearts), True, (255,255,255))
          warning = True



      else:
        if not silly:
          hearts = hearts - 1
          hearts_msg =  my_font.render(str(hearts), True, (255,255,255))
          guessed_yet = False
          warning = True
    silly = False
    usage = 1
    if hearts <= 0:
      game_over = True

  #BLIT ZONE
  screen.fill((245, 14, 14))
  if not game_start:
      screen.blit(start_message, (700, 200))
      screen.blit(s.image, s.rect)
  if game_start:
      if not warning:
          screen.blit(picked_word_display, (850, 60))
      screen.blit(guessing_message,(730,30))
      if hearts >= 1 and int(current_time) >= 1:
        screen.blit(b.image, b.rect)
      else:
          screen.blit(e.image, e.rect)
          screen.blit(game_over_message, (400,300))
      pygame.draw.rect(screen, text_box_color, text_box, 3)
      screen.blit(file_name_message, (1000,60))
      screen.blit(time_message, (100,60))
      screen.blit(hearts_msg, (700, 30))
      screen.blit(score_message, (300,900))
      if hearts >= 3 and int(current_time) >= 1:
          screen.blit(h_one.image, h_one.rect)
      else:
          screen.blit(xh_one.image, xh_one.rect)
      if hearts >= 2 and int(current_time) >= 1:
          screen.blit(h_two.image, h_two.rect)
      else:
          screen.blit(xh_two.image, xh_two.rect)
      if hearts >= 1 and int(current_time) >= 1:
         screen.blit(h_three.image, h_three.rect)
      else:
          screen.blit(xh_three.image, xh_three.rect)
      if len(file_name) > 0 and warning:
          screen.blit(text_box_warning, (650,60))


  pygame.display.update()







