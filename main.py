import time
import random
import curses
from curses import wrapper

GREEN = 1
RED = 2
WHITE = 3

def start_screen(stdscr):
  stdscr.clear()
  stdscr.addstr("WELCOME TO THE TYPING SPEED TEST!\n")
  stdscr.addstr("Press any key to begin")
  stdscr.refresh()
  stdscr.getkey()

def display_text(stdscr, target_text, current_text, wpm = 0):
  stdscr.addstr(target_text)
  stdscr.addstr(f'\n{"" :{"="}^50}\n')
  stdscr.addstr(f'[WPM: {wpm}]\n')
  for i, c in enumerate(current_text):
    correct_char = target_text[i]
    if c == correct_char:
      stdscr.addstr(c, curses.color_pair(GREEN))
    else:
      stdscr.addstr(c, curses.color_pair(RED))

def load_text():
  with open('paragraphs.txt', "r") as file:
    paras = file.readlines()
    return random.choice(paras)

def typing_test(stdscr):
  # does not wait for user input
  stdscr.nodelay(True)

  target_text = load_text()
  target_text = target_text.strip()
  current_text = []
  wpm = 0
  start_time = time.time()

  while(True):
    time_passed = max(time.time() - start_time, 1)
    # character per min
    wpm = len(current_text) / (time_passed / 60)
    # word per min (average word length is 5)
    wpm = round(wpm / 5)

    try:
      stdscr.clear()
      display_text(stdscr, target_text, current_text, wpm)
      stdscr.refresh()
    except curses.error:
      pass
    
    # finish the test
    if "".join(current_text) == target_text:
      stdscr.nodelay(False)
      break

    # stdscr.nodelay(True) -> getkey throws exception
    try:
      key = stdscr.getkey()
    except:
      continue
    
    # escape key
    try:
      if ord(key) == 27:
        stdscr.nodelay(False)
        break
    except:
      pass

    # remove the last character when backspace is pressed
    if key in ("KEY_BACKSPACE", '\b', '\x7f'):
      if len(current_text) > 0:
        current_text.pop()
    elif key in ("SHF_PADENTER", '\''):
      current_text.append('\'')
    elif len(current_text) < len(target_text) and len(key) == 1:
      current_text.append(key)
    
def main(stdscr):
  curses.init_pair(GREEN, curses.COLOR_GREEN, curses.COLOR_BLACK)
  curses.init_pair(RED, curses.COLOR_RED, curses.COLOR_BLACK)
  curses.init_pair(WHITE, curses.COLOR_WHITE, curses.COLOR_BLACK)

  start_screen(stdscr)
  while True:
    typing_test(stdscr)
    stdscr.addstr("\nYou completed the test! Press any key to continue...")
    stdscr.refresh()
    key = stdscr.getkey()
		
    try:
      if ord(key) == 27:
        break
    except:
      pass

wrapper(main)