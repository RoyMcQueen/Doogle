import googlemaps ## installed the googlemaps library which is used as a wrapper to connect to the API
import pandas as pd
import time
import geopy.distance
from IPython.display import display
import geocoder

pd.set_option('display.max_rows', None)


## add the user entry logic (check website justfoodfordogs)

## add the products and the logic

## add color to the text

## add linespaces to the text


# Google Maps API



api_key = 'AIzaSyDhqY1U1q5WVGMord6QXlw8ZcgwaamvRbQ' # Gmaps API key

map_client = googlemaps.Client(api_key) ## connecting to the API

food_table = pd.read_excel('datasets/AggregatedTable.xlsx')

def beginning():

    start = input("""How can we help? Pick one of these options:\n\n[1]Find nearby places for your pet.\n\n[2]Choose the right food for your pet.""")

    while start not in(['1','2']):

                print('You need to enter 1 or 2, please try again')

                start = input("""How can we help? Pick one of these options:\n\n[1]Find nearby places for your pet.\n[2]Choose the right food for your pet.""")
    if start == '1':
        searching()
    elif start == '2':
        food()
### Food code missing

def searching():

    first = input('Do you want to use your current location? Y or N ') ## deciding if we use our own location or another address

    while first.lower() not in(['y','n']):

            print('You need to enter Y or N, please try again')

            first = input('Do you want to use your current location? Y or N ') 
            

    if first.lower() == 'Y'.lower():

        g = geocoder.ip('me')

        my_address_coordinates = tuple(g.latlng)
    
    elif first.lower() == 'N'.lower():    

        my_address = input("Please input the address you want ") ## write the address you are at, or the address where want to check nearby places

        address_response = map_client.geocode(my_address) ## fetches the address from the API using the words inserted above

        my_address_coordinates = tuple(address_response[0]['geometry']['location'].values()) ## gets the tuple of the coordinates 
                                                                                        ## from address_response 
        

    
        
    my_radius = '' ## asks the user for the radius in which to search, in kilometres


    while type(my_radius) == str: 

        if my_radius.isdigit():
        
            my_radius = int(my_radius)*1000

        elif my_radius.split('.')[0].isdigit() and my_radius.count('.') == 1:
            
            my_radius = float(my_radius)*1000

        else:
            
            my_radius = input("Please enter a radius of search in kms ")


    ## consider an if-else statement here to just allow these options; how to do that?
    my_search = input("""Search nearby you: do you want to search for:\n\n[1]veterinary hospitals\n[2]pet shops\n[3]dog parks """)

    search_dict = {'1':'veterinary hospitals','2':'pet shops','3':'dog parks'}


    ## TO DO: change to dictionary!!

    while my_search not in('1','2','3'):

        print('You need to choose one of the options, please try again')

        my_search = input("""Search nearby you: do you want to search for:\n\n[1]veterinary hospitals\n[2]pet shops\n[3]dog parks""")


    response = map_client.places_nearby(location = my_address_coordinates, 
                                        keyword = search_dict[my_search], radius = my_radius) # calls the GMaps API to return the places
                                                                                            # nearby the address the user input, with the user 
                                                                                            # input radius, and the keywords we want to search for



    ## Deciding which dataframe to show // consider putting this in a function


    if my_search == '1': ## if what we input for my_search is that, then prepare the dataframe. same logic all the way down

        try:

            vet_hospital_df = pd.DataFrame(response['results'])

            vet_hospital_df.drop(['geometry','icon','icon_background_color', 
                                'icon_mask_base_uri','photos','place_id','plus_code','reference',
                                'scope','types','business_status'],axis = 1, inplace=True)

            vet_hospital_df.rename(columns = {'name':'Hospital_Name', 'rating':'User_Rating','user_ratings_total':
                                            'User_Rating_Total','vicinity':'Address',
                                            'opening_hours':'Open Now'}, inplace = True)

            vet_hospital_df = vet_hospital_df[['Hospital_Name','User_Rating','User_Rating_Total','Address','Open Now']]

            vet_hospital_df.loc[vet_hospital_df['Open Now'] == {'open_now': True}, 'Open Now'] = 'Open Now'
            vet_hospital_df.loc[vet_hospital_df['Open Now'] == {'open_now': False}, 'Open Now'] = 'Closed'
            vet_hospital_df.loc[vet_hospital_df['Open Now'] == {}, 'Open Now'] = 'Undisclosed'
            vet_hospital_df['Open Now'].fillna('Undisclosed',inplace=True) ## falta replicar isto para os outros

            vet_hospital_df.sort_values(by=['User_Rating_Total','User_Rating'], ascending=False, inplace=True)

            print(vet_hospital_df.head(10)) ## need to get new names for open now values, maybe reorder them

        except:
            print("There are no veterinary hospitals within this radius. Try increasing the radius") ## call to the API might not retrieve anything

        ## once any of these dataframes are displayed, we need to find a way to ask if the user wants to research again.

    elif my_search == '2':


        try:


            pet_shop_df = pd.DataFrame(response['results'])

            pet_shop_df.drop(['geometry','icon','icon_background_color', 
                                'icon_mask_base_uri','photos','place_id','plus_code','reference',
                                'scope','types','business_status'],axis = 1, inplace=True)

            pet_shop_df.rename(columns = {'name':'Pet_Shop', 'rating':'User_Rating','user_ratings_total':'User_Rating_Total',
                                        'vicinity':'Address','opening_hours':'Open Now'}, inplace = True)


            pet_shop_df.sort_values(by=['User_Rating_Total','User_Rating'], ascending=False,inplace=True)

            pet_shop_df = pet_shop_df[['Pet_Shop','User_Rating','User_Rating_Total','Address','Open Now']]

            pet_shop_df.loc[pet_shop_df['Open Now'] == {'open_now': True}, 'Open Now'] = 'Open Now'
            pet_shop_df.loc[pet_shop_df['Open Now'] == {'open_now': False}, 'Open Now'] = 'Closed'
            pet_shop_df.loc[pet_shop_df['Open Now'] == {}, 'Open Now'] = 'Undisclosed'
            pet_shop_df['Open Now'].fillna('Undisclosed',inplace=True) 

            print(pet_shop_df.head(10)) ## need to get new names for open now values, maybe reorder them

        except:
            print("There are no pet shops within this radius. Try increasing the radius") ## call to the API might not retrieve anything

    elif my_search == '3':

        try:

            dog_park_df = pd.DataFrame(response['results'])

        


            dog_park_df.drop(['geometry','icon','icon_background_color', 
                                'icon_mask_base_uri','photos','place_id','plus_code','reference',
                                'scope','types','business_status'],axis = 1, inplace=True)


            dog_park_df.rename(columns = {'name':'Dog_Park', 'rating':'User_Rating','user_ratings_total':'User_Rating_Total',
                                        'vicinity':'Address','opening_hours':'Open Now'}, inplace = True)


            dog_park_df.sort_values(by=['User_Rating_Total','User_Rating'], ascending=False,inplace=True)

            dog_park_df = dog_park_df[['Dog_Park','User_Rating','User_Rating_Total','Address','Open Now']]

            dog_park_df.loc[dog_park_df['Open Now'] == {'open_now': True}, 'Open Now'] = 'Open Now'
            dog_park_df.loc[dog_park_df['Open Now'] == {'open_now': False}, 'Open Now'] = 'Closed'
            dog_park_df.loc[dog_park_df['Open Now'] == {}, 'Open Now'] = 'Undisclosed'
            dog_park_df['Open Now'].fillna('Undisclosed',inplace=True)
        

            print(dog_park_df.head(10)) ## need to get new names for open now values, maybe reorder them

        except:
            print("There are no dog parks within this radius. Try increasing the radius") ## call to the API might not retrieve anything



def search_again():

    question = input('Do you want to search anything else? Y or N ')

    while question.lower() not in('y','n'):

        question = input('Do you want to search anything else ? Y or N')

    if question.lower() == 'Y'.lower():
        beginning()

    else:
        print('thanks')



def food():
    age_prompt = input("""Select one of the ages for your puppy\n\n[1]Puppy\n[2]Adult\n[3]Senior""")

    while age_prompt not in(['1','2','3']):

        print('You need to enter 1,2,or 3 please try again')

        age_prompt = input("""Select one of the ages for your puppy\n\n[1]Puppy\n[2]Adult\n[3]Senior""")

    age_dict = {'1':'Puppy','2':'Adult','3':'Senior'}

    brand_prompt = input('Would you like to select a specific brand, or see all the options? Y or N')

    while brand_prompt.lower() not in(['y','n']):

        print('You need to enter Y or N, please try again')

        brand_prompt = input('Would you like to select a specific brand? Y or N')

    if brand_prompt.lower() == 'Y'.lower():

        brand_choice = input("""Please select one of the following brands:\n\n[1]Royal Canin\n[2]Hills\n[3]Advance\n[4]Taste Of The Wild\n[5]Wolf Of Wilderness\n[6]Pedigree\n[7]Yarrah """)

        while brand_choice not in(['1','2','3','4','5','6','7']):

            print('You need to enter one of the options, please try again')

            brand_prompt = input("""Please select one of our selected brands:\n\n[1]Royal Canin\n[2]Hills\n[3]Advance\n[4]Taste Of The Wild\n[5]Wolf Of Wilderness\n[6]Pedigree\n[7]Yarrah """)

        food_dict = {'1':'RoyalCanin','2':'Hill','3':'Advance','4':'Wild','5':'Wolf','6':'Pedigree','7':'Yarrah'}
     
       
        print(food_table[(food_table['DogAge'] == age_dict[age_prompt]) & (food_table['Brand'] == food_dict[brand_choice])][['ProductName','Price']])

    else:

        display(food_table[(food_table['DogAge'] == age_dict[age_prompt])][['ProductName','Price']])



beginning()


search_again()

        