# Author: Aldric

# From the zxcvbn paper, the following are some ideas for evaluating password strength

# token logitech l0giT3CH ain’t parliamentarian 1232323q
# reversed DrowssaP
# sequence 123 2468 jklm ywusq
# repeat zzz ababab l0giT3CHl0giT3CH
# keyboard qwertyuio qAzxcde3 diueoa
# date 7/8/1947 8.7.47 781947 4778 7-21-2011 72111 11.7.21
# bruteforce x$JQhMzt

# classes
# letters
# letters and digits
# letters, digits and symbols

# length: 8, 12 and 20

# sources
# https://manytools.org/network/password-generator/
# https://passwordgeneratorapp.com/multiple-password-generator/
# 

# first we need a dictionary with frequency.
import wordfreq

