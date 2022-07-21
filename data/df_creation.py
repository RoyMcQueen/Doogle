import pandas as pd 


def create_empty_df(col_list, df_name):

    df =pd.DataFrame(columns=col_list)
    df.to_csv(f'data/{df_name}.csv', index=False)

user_cols = ['Name', 'Email', 'Password', 'User_ID']
dog_cols = ['Name','Birthday','Sex', 'Breed','Weight','Allergies','Current Food','user_id', 'dog_id']


create_empty_df(col_list=user_cols, df_name='users')
create_empty_df(col_list=dog_cols, df_name='dogs')