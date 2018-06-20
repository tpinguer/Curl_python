import re



word = "$thiagoxx.txt"

word = re.sub(r'.txt$', '.json', word)

print(word)



# for (index, string) in enumerate(word):
#     match = re.findall(word, string)
        
#     lenght = len(match) 

#     if lenght == 0:
#         print(index)
#         word[index] = 
