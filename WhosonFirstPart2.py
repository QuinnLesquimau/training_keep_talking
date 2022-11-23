import random

f = open("data/words.txt", 'r')
data = [line.split(':') for line in f.readlines()]
f.close()
print("Which part do you want to learn/train?")
print("Give two indices a and b, you will learn lines between a and b")
a = int(input())
b = int(input())
data = data[a:b+1]
print("How many words do you want to learn in each line?")
nbr_words = int(input())
while True:
  word, answer = random.choice(data)
  answer = ",".join(answer.split(',')[:nbr_words])
  print(word)
  if answer == input():
    print("Correct!")
  else:
    print("Wrong! The answer is " + answer)