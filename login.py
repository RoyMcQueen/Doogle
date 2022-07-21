import pandas as pd 
from dog_code import *

USER_PATH = 'data/users.csv'
DOG_PATH = 'data/dogs.csv'
USER_DF = pd.read_csv(USER_PATH)
DOG_DF = pd.read_csv(DOG_PATH)

def register_user(user_name, user_email, user_pass, user_df):
    
    """Register function for the user """

    user_id = len(user_df) + 101 ## first user start in 1001 --> we always add one to this value when new register occur
    
    user_df.loc[-1] = [user_name, user_email, user_pass, user_id] # adding a row based on inputs 
    user_df.index = user_df.index + 1  # shifting index
    user_df = user_df.sort_index()  # sorting by index

    user_df.to_csv(USER_PATH, index=False) # overwrite the user
    return user_id 

def register_dog(dog_name,dog_bd,dog_sex,dog_breed,dog_weight,dog_allergies,dog_food, user_id, dog_df):
    
    """Register function for the dog """

    dog_id =  len(dog_df) + 101
    dog_df.loc[-1] = [dog_name,dog_bd,dog_sex,dog_breed,dog_weight,dog_allergies,dog_food, user_id, dog_id] # adding a row based on inputs 
    dog_df.index = dog_df.index + 1  # shifting index
    dog_df = dog_df.sort_index()  # sorting by index

    dog_df.to_csv(DOG_PATH, index=False) # overwrite the user 


### Menu one for register and Login  ### 

def menu():
    
    response = input(  
    """
    What do you want to do?
    
    1 - Register 
    2 - Login
    3 - Close
    
    """)

    if response == '1':

        ### user inputs for registation ###

        user_name = input('Enter your full name')
        user_email = input('Enter your email')
        password = input('Enter pasword')

        user_id = register_user(user_name=user_name, user_email=user_email, user_pass=password, user_df=USER_DF)

        print("\n Now it's time to register your dog in the app \n")


        dog_name = input('Enter the name of your dog.')
        dog_bd = input('Enter the month and year in which your dog was born in this format: Mon - Year')
        dog_sex = input('Is your dog male or female.')
        dog_breed = input('Enter the breed of your dog.')
        dog_weight = input('Enter the weight of your dog in kg.')
        dog_allergies = input('What is your dog allergic to?')
        dog_food = input('What food is your dog currently eating?')
        user_id = user_id

        register_dog(dog_name=dog_name,dog_bd=dog_bd,dog_sex=dog_sex,dog_breed=dog_breed,dog_weight=dog_weight,
                            dog_allergies=dog_allergies,dog_food=dog_food, user_id = user_id, dog_df = DOG_DF)
        
        return (1, None)
    
    elif response == '2':

        tries = 1
        while tries:

            user_email = input('Enter your email')
            password = input('Enter pasword')

            data = USER_DF[(USER_DF['Email'] == user_email) & (USER_DF['Password'] == password)]
            logged = len(data)

            if logged == 1:
                print('\n\n    You loged in succesfully!!     \n\n')
                user_id = data['User_ID'].values[0]

                return (2, user_id)
            
            else:
                res = input('Wrong Password, Do you want to try again? ')
                if res == 'yes':
                    continue
                else:
                    return (1, None)
                


    elif response == '3':
        
        return (0, None)


### Menu two for OPTIONS   ### 


def menu2(user_id, dog_df):

    profile = input(  
    """
    What do you want to do?
    
    1 - Dog Info 
    2 - Find nearby places for your pet
    3 - Choose the right food for your pet
    4 - Log Out

    """) 

    if profile == '1':
        print(dog_df[dog_df['user_id'] == user_id])
        return 1

    elif profile == '2':
        searching()
        return 1
    elif profile == '3':
        food()
        return 1
    elif profile == '4':
        return 0