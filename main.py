import bot_logic as bl
from time import sleep

#Create a Reddit instance
r = bl.bot_login()

s = r.submission(id = '1bs0cs')
# Load more comments
while True:
    try:
        s.comments.replace_more()
        break
    except:
        print('Handling replace_more exception')
        sleep(1)

f = s.comments
conv = bl.find_conv_in_forest(f)
