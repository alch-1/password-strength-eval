# Author: Aldric
# this script aims to generate strong (hard to guess) passwords

import secrets 
# from python's website:
# The secrets module is used for generating cryptographically strong random numbers suitable for managing data such as passwords, account authentication, security tokens, and related secrets.
# In particular, secrets should be used in preference to the default pseudo-random number generator in the random module, which is designed for modelling and simulation, not security or cryptography. 
import string 
import random

def generatePassLetters(length=8):
  lowercase = string.ascii_lowercase
  uppercase = string.ascii_uppercase

  remainder = length % 2 # ensure that we account for remainders
  size = length // 2

  lwr = ''.join(secrets.choice(lowercase) for _ in range(size))
  upr = ''.join(secrets.choice(uppercase) for _ in range(size + remainder)) # add remainder
  password_unshuffled = lwr + upr

  randbytes = secrets.token_bytes(16) # random bytes from secrets
  # print(randbytes)

  # we want to shuffle but secrets doesn't have that function
  # so we initialise random with a random seed
  random.seed(randbytes) # ensure randomness, if not random follows system time, which is deterministic
  password = ''.join(random.sample(password_unshuffled ,len(password_unshuffled)))

  return password

def generatePassLettersDigits(length=8):
  lowercase = string.ascii_lowercase
  uppercase = string.ascii_uppercase
  numbers = string.digits

  remainder = length % 3 # ensure that we account for remainders
  size = length // 3

  lwr = ''.join(secrets.choice(lowercase) for _ in range(size))
  upr = ''.join(secrets.choice(uppercase) for _ in range(size))
  nbr = ''.join(secrets.choice(numbers) for _ in range(size + remainder))

  password_unshuffled = lwr + upr + nbr
  
  randbytes = secrets.token_bytes(16) # random bytes from secrets
  # print(randbytes)

  # we want to shuffle but secrets doesn't have that function
  # so we initialise random with a random seed
  random.seed(randbytes) # ensure randomness, if not random follows system time, which is deterministic
  password = ''.join(random.sample(password_unshuffled ,len(password_unshuffled)))

  return password


def generatePassAll(length=8):
  lowercase = string.ascii_lowercase
  uppercase = string.ascii_uppercase
  numbers = string.digits
  symbols = string.punctuation

  remainder = length % 4 # ensure that we account for remainders
  # evenly distribute the 4 different pools
  size = length // 4

  lwr = ''.join(secrets.choice(lowercase) for _ in range(size))
  upr = ''.join(secrets.choice(uppercase) for _ in range(size))
  nbr = ''.join(secrets.choice(numbers) for _ in range(size))
  sym = ''.join(secrets.choice(symbols) for _ in range(size + remainder)) # add remainder, if any
  password_unshuffled = lwr + upr + nbr + sym

  randbytes = secrets.token_bytes(16) # random bytes from secrets
  # print(randbytes)

  # we want to shuffle but secrets doesn't have that function
  # so we initialise random with a random seed
  random.seed(randbytes) # ensure randomness, if not random follows system time, which is deterministic
  password = ''.join(random.sample(password_unshuffled ,len(password_unshuffled)))

  return password


# testing
# print(generatePassLetters(9))
# print(generatePassLettersDigits(8))
# print(generatePassAll(7))

# write to file

# 8
with open("python-8-l.txt", "w+") as f:
  for i in range(100):
    f.write(generatePassLetters(8) + "\n")

with open("python-8-ld.txt", "w+") as f:
  for i in range(100):
    f.write(generatePassLettersDigits(8) + "\n")

with open("python-8-lds.txt", "w+") as f:
  for i in range(100):
    f.write(generatePassAll(8) + "\n")

# 12
with open("python-12-l.txt", "w+") as f:
  for i in range(100):
    f.write(generatePassLetters(12) + "\n")

with open("python-12-ld.txt", "w+") as f:
  for i in range(100):
    f.write(generatePassLettersDigits(12) + "\n")

with open("python-12-lds.txt", "w+") as f:
  for i in range(100):
    f.write(generatePassAll(12) + "\n")

# 20
with open("python-20-l.txt", "w+") as f:
  for i in range(100):
    f.write(generatePassLetters(20) + "\n")

with open("python-20-ld.txt", "w+") as f:
  for i in range(100):
    f.write(generatePassLettersDigits(20) + "\n")

with open("python-20-lds.txt", "w+") as f:
  for i in range(100):
    f.write(generatePassAll(20) + "\n")