# Author: Aldric

# From the zxcvbn paper, the following are some ideas for evaluating passwords strength

# token logitech l0giT3CH ain’t parliamentarian 1232323q
# reversed DrowssaP
# sequence 123 2468 jklm ywusq
# repeat zzz ababab l0giT3CHl0giT3CH
# keyboard qwertyuio qAzxcde3 diueoa
# date 7/8/1947 8.7.47 781947 4778 7-21-2011 72111 11.7.21
# bruteforce x$JQhMzt

# classes
# l   = letters
# ld  = letters and digits
# lds = letters, digits and symbols

# length: 8, 12 and 20

# sources
# https://manytools.org/network/password-generator/
# https://passwordgeneratorapp.com/multiple-password-generator/
# 

# first we need a dictionary with frequency.
import wordfreq
import regex
from datetime import datetime
from itertools import islice
import collections
from nltk.corpus import words

def main():
  TODAY = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
  WORDS = set(words.words())

  inp = input("Enter filename: ")
  ## token ##
  with open(inp, "r+") as f:
    lines = f.readlines()
  lines = [line.rstrip().lower() for line in lines]
  # check for words in the string

  # sliding window algorithm
  def sliding_window(iterable, n):
    # sliding_window('ABCDEFG', 4) -> ABCD BCDE CDEF DEFG
    it = iter(iterable)
    window = collections.deque(islice(it, n), maxlen=n)
    if len(window) == n:
      yield tuple(window)
    for x in it:
      window.append(x)
      yield tuple(window)

  # get all the windows above len 3 (ignore words with len 2 and below)
  def get_all_windows(s):
    all_windows = []
    n = len(s)
    while n > 2:
      all_windows += ["".join(x) for x in sliding_window(s, n)]
      n = n - 1
    return all_windows

  # get word frequency and assign score
  def check_token(pw):
    freq = 0.0
    window = get_all_windows(pw)
    # print(window) # debug
    for s in window:
      if s in WORDS: # make sure the match is only on english words
        freq = freq + wordfreq.zipf_frequency(s, 'en') # if no match, returns 0
      # print(s, freq) # debug
    return freq

  ## sequence ##

  ## repeat ##
  # check for any character repeated 3 times or more
  def check_repeat(line):
    repeat3 = regex.compile(r"(.)\1{2,}")
    result = repeat3.search(line)
    if result == None:
      print("no match")
      return False # no match
    else:
      print(result)
      # r.span() => (7, 10)
      # r.group() => 'ttt'
      # print(m.captures())
      return True

  ## date ##

  ## bruteforce ## 

  # run strength checker
  with open("logs.txt", "a+") as f:
    f.write("===" + TODAY + ", " + inp + "===")
    for line in lines:
      print(line)
      check_repeat(line)
      print(check_token(line))

if __name__ == "__main__":
  main()
