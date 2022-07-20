import googlemaps ## installed the googlemaps library which is used as a wrapper to connect to the API
import pandas as pd
import time
import geopy.distance
from IPython.display import display
import geocoder





# Google Maps API



api_key = 'AIzaSyDhqY1U1q5WVGMord6QXlw8ZcgwaamvRbQ' # Gmaps API key

map_client = googlemaps.Client(api_key) ## connecting to the API



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


    while type(my_radius) == str: ## WRONG

        if my_radius.isdigit():
        
            my_radius = int(my_radius) *1000

        elif my_radius.split('.')[0].isdigit() and my_radius.count('.') == 1:
            
            my_radius = float(my_radius)

        else:
            
            my_radius = input("Please enter a radius in kms ")


    ## consider an if-else statement here to just allow these options; how to do that?
    my_search = input("""Search nearby you: do you want to search for:\n\nveterinary hospitals\npet shops\ndog parks """)

    while my_search not in('veterinary hospitals','pet shops','dog parks'):

        print('You need to choose one of the options, please try again')

        my_search = input("""Search nearby you: do you want to search for:\n\nveterinary hospitals\npet shops\ndog parks""")


    response = map_client.places_nearby(location = my_address_coordinates, 
                                        keyword = my_search, radius = my_radius) # calls the GMaps API to return the places
                                                                                            # nearby the address the user input, with the user 
                                                                                            # input radius, and the keywords we want to search for



    ## Deciding which dataframe to show // consider putting this in a function


    if my_search == 'veterinary hospitals': ## if what we input for my_search is that, then prepare the dataframe. same logic all the way down

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
        vet_hospital_df['Open Now'].fillna('Undisclosed',inplace=True) ## falta replicar isto para os outros

        vet_hospital_df.sort_values(by=['User_Rating_Total','User_Rating'], ascending=False, inplace=True)

        print(vet_hospital_df.head(10)) ## need to get new names for open now values, maybe reorder them

        ## once any of these dataframes are displayed, we need to find a way to ask if the user wants to research again.

    elif my_search == 'pet shops':

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
        pet_shop_df['Open Now'].fillna('Undisclosed',inplace=True) 

        display(pet_shop_df.head(10)) ## need to get new names for open now values, maybe reorder them

    elif my_search == 'dog parks':

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
        dog_park_df['Open Now'].fillna('Undisclosed',inplace=True) 
        

        display(dog_park_df.head(10)) ## need to get new names for open now values, maybe reorder them

    search_again()

def search_again():

    question = input('Do you want to search anything else? Y or N')

    while question.lower() not in('y','n'):

        question = input('Do you want to search anything else? Y or N')

    if question.lower() == 'Y'.lower():
        searching()

    else:
        print('thanks')

searching()

