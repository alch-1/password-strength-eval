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
from re import I
import wordfreq
import math
import regex
from datetime import datetime
from itertools import islice
import collections
from nltk.corpus import words
from collections import Counter
from math import log


def main():
  TODAY = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
  WORDS = set(words.words())
  ## read data
  inp = input("Enter filename: ")
  with open(inp, "r+") as f:
    lines = f.readlines()
  lines = [line.rstrip() for line in lines]

  ## token ##
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
  def get_all_windows(s) -> list:
    all_windows = []
    n = len(s)
    while n > 2:
      all_windows += ["".join(x) for x in sliding_window(s, n)]
      n = n - 1
    return all_windows

  # get word frequency and assign score
  def check_token(pw) -> float:
    pw = pw.lower()
    freq = 0.0
    window = get_all_windows(pw)
    # print(window) # debug
    for s in window:
      if s in WORDS: # make sure the match is only on english words
        freq = freq + wordfreq.zipf_frequency(s, 'en') # if no match, returns 0
      # print(s, freq) # debug
    return freq

  ## sequence ##
  seq = (
    '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', 
    '=', "Q", 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '[', ']', '\\',
    'A', "S", 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';' ,"'",
    'Z', 'X', 'C', 'V', 'B', "N", 'M', ',', '.', '/'
  )

  def check_sequence(line):
    line = line.upper()
    start = math.inf
    end = math.inf
    for i in range(0, len(line) - 1):
      started = False
      current = line[i]
      if current == '/':
        pass
      elif current in seq: 
        if start == math.inf:
          start = i
        # find index
        nxt_index = seq.index(current) + 1
        # check for next
        try:
          nxt_expected = line[nxt_index]
          nxt = line[i + 1]
          if nxt == nxt_expected:
            end = i + 1
        except Exception:
          pass
    # we only want matches with length of 3 chars or more
    if end == math.inf or abs(end - start) <= 2: 
      print("sequence: no match")
      return False
    else:
      return (start, end)

  ## repeat ##
  # check for any character repeated 3 times or more
  def check_repeat(line):
    repeat3 = regex.compile(r"(.)\1{2,}")
    result = repeat3.search(line)
    if result == None:
      print("repeat: no match")
      return False # no match
    else:
      print(result)
      # r.span() => (7, 10)
      # r.group() => 'ttt'
      return result.span()

  ## date ##
  def check_date(line):
    datematch = regex.compile(r"^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]|(?:Jan|Mar|May|Jul|Aug|Oct|Dec)))\1|(?:(?:29|30)(\/|-|\.)(?:0?[1,3-9]|1[0-2]|(?:Jan|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec))\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)(?:0?2|(?:Feb))\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9]|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep))|(?:1[0-2]|(?:Oct|Nov|Dec)))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$")
    result = datematch.search(line)
    if result == None:
      print("date: no match")
      return False # no match
    else:
      print(result)
      # r.span() => (7, 10)
      # r.group() => 'ttt'
      return result.span()
  

  ## bruteforce ## 
  # check for brute-force-ability
  # calculate Shannon entropy of string
  def shannon(s):
    counts = Counter(s) # count elements from the string
    length = len(s)
    freq = [(i / length) for i in counts.values()]
    return -(sum(f * log(f, 2) for f in freq)) * length


  ## run strength checker ##
  with open("logs.txt", "a+") as f:
    # f.write("===" + TODAY + ", " + inp + "===" + "\n")
    for line in lines:
      print("---")
      print(line)
      print("token", check_token(line))
      repeattuple = check_repeat(line)
      sequencetuple = check_sequence(line)

      print("repeat", repeattuple)
      print('sequence', sequencetuple)
      if repeattuple != False:
        start = repeattuple[0]
        end = repeattuple[1]
        line = line[:start] + line[end + 1:]
      
      datetuple = check_date(line)
      if datetuple != False:
        start = datetuple[0]
        end = datetuple[1]
        line = line[:start] + line[end + 1:]
      
      print('entropy', shannon(line))


if __name__ == "__main__":
  main()
