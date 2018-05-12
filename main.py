from time import sleep
from bot_logic import *
from helper import *

#Create a Reddit instance
r = bot_login()

s = r.submission(id = '8isv7u')
print('Loading more comments...')
# Load more comments
while True:
    try:
        s.comments.replace_more()
        break
    except:
        print('Handling replace_more exception')
        sleep(1)
print('Done!')

print('Looking for conversations...')
convs = find_conv_in_forest(s.comments)
print('Done!')

with open('convs.txt', 'w+') as f:
    f.write(str_convs(convs))
