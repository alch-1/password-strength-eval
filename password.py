# Author: Aldric

# sources
# https://manytools.org/network/password-generator/
# https://passwordgeneratorapp.com/multiple-password-generator/
# 

# first we need a dictionary with frequency.
import wordfreq
import math
import regex
from datetime import datetime
from itertools import islice
import collections
from nltk.corpus import words
from collections import Counter
from math import log
import csv


def main():
  TODAY = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
  WORDS = set(words.words())

  ## run strength checker ##
  files_to_check = [
    "manytools-8-l.txt",
    "manytools-8-ld.txt",
    "manytools-8-lds.txt",
    "manytools-12-l.txt",
    "manytools-12-ld.txt",
    "manytools-12-lds.txt",
    "manytools-20-l.txt",
    "manytools-20-ld.txt",
    "manytools-20-lds.txt",

    "pwgen-8-l.txt",
    "pwgen-8-ld.txt",
    "pwgen-8-lds.txt",
    "pwgen-12-l.txt",
    "pwgen-12-ld.txt",
    "pwgen-12-lds.txt",
    "pwgen-20-l.txt",
    "pwgen-20-ld.txt",
    "pwgen-20-lds.txt",

    "python-8-l.txt",
    "python-8-ld.txt",
    "python-8-lds.txt",
    "python-12-l.txt",
    "python-12-ld.txt",
    "python-12-lds.txt",
    "python-20-l.txt",
    "python-20-ld.txt",
    "python-20-lds.txt"
  ]

  
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

  ## repeat ##
  # check for any character repeated 3 times or more
  def check_repeat(line):
    repeat3 = regex.compile(r"(.)\1{2,}")
    result = repeat3.search(line)
    if result == None:
      # print("repeat: no match")
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
      # print("date: no match")
      return False # no match
    else:
      print(result)
      # r.span() => (7, 10)
      # r.group() => 'ttt'
      return result.span()
  

  ## bruteforce ## 
  # check for brute-force-ability
  # calculate entropy of string
  def get_entropy(s) -> float:
    # https://www.pleacher.com/mp/mlessons/algebra/entropy.html
    # https://en.wikipedia.org/wiki/Password_strength#Required_bits_of_entropy
    # check for char set
    lowercase = regex.findall(r"[a-z]+", s) # 26
    uppercase = regex.findall(r"[A-Z]+", s) # 26
    numbers = regex.findall(r"[0-9]+", s) # 10
    symbols = regex.findall(r"[-!$%^&*()_+|~=`{}\\[\]:\";'<>?,.\/@#]+", s) # 32
    
    # print(lowercase, uppercase, numbers, symbols)
    # E = log_2(N ** L)
    n = 0
    if lowercase: 
      n += 26
    if uppercase: 
      n += 26
    if numbers: 
      n += 10
    if symbols: 
      n += 32

    l = len(s)

    entropy = log(n ** l, 2)

    return entropy


  ########
  ## read data
  # inp = input("Enter filename: ")

  for inp in files_to_check:
    sum_score = 0
    count = 0
    with open(inp, "r+") as f:
      lines = f.readlines()
      lines = [line.rstrip() for line in lines]
    
    with open("logs-test.txt", "a+") as f:
      f.write("===" + TODAY + ", " + inp + "===" + "\n")
      to_csv = []
      for line in lines:
        score = 0
        print("---")
        print(line)
        token_result = check_token(line)
        print("token:", token_result)
        # score:
        if token_result < 8:
          score = score + 5
        elif token_result < 10:
          score = score + 4
        elif token_result < 12:
          score = score + 3
        elif token_result < 14:
          score = score + 2
        elif token_result < 16:
          score = score + 1


        repeattuple = check_repeat(line)
        print("repeat: " + str(repeattuple))
        f.write("repeat: " + str(repeattuple) + "\n")

        if repeattuple != False:
          start = repeattuple[0]
          end = repeattuple[1]
          line = line[:start] + line[end + 1:]
        else:
          score = score + 5
        
        datetuple = check_date(line)
        print("date: " + str(datetuple))
        f.write("date: " + str(datetuple) + "\n")
        if datetuple != False:
          start = datetuple[0]
          end = datetuple[1]
          line = line[:start] + line[end + 1:]
        else:
          score = score + 5
        
        entropy = get_entropy(line)
        print('entropy:', entropy)
        f.write('entropy: ' + str(entropy) + "\n")
        if entropy >= 128:
          score += 10
        else:
          to_add = round(entropy/128 * 10)
          score += to_add
        print("final score:", score, "/ 25")
        f.write("final score: " + str(score) +  " / 25\n")
        to_csv.append([line, score])

        sum_score += score
        count += 1

      # calculate total score and average
      average_score = sum_score / count
      with open(inp + '.csv', 'w+', encoding='UTF8', newline='') as f1:
        writer = csv.writer(f1)
        writer.writerow(['password', 'score'])
        writer.writerows(to_csv)
        writer.writerow(['average score', average_score])
if __name__ == "__main__":
  main()
