from login import *

play = True
while play == True:

    run, user = menu()

    if run == 1:
        continue
    
    
    elif run == 2:
        keep_play = True
        while keep_play:
            
            call = menu2(user, DOG_DF)### 2
            if call == 1:
                continue
            else:
                keep_play = False

    else:
        play = False