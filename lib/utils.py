# importing required libraries
import pymysql
import typing
import numpy as np
import pandas as pd

def read_data_from_db(config, table_name : str = "Burger_sales_data"):
    """
    Function to read data from given database (hosted on postgres)

    Input:
    config: config.yml file
    table_name: name of the table where data is stored (default parameter: "Burger_sales_data")

    Output:
    df: Dataframe containing all the data fetched from given table
    """
    # creating connection to the DB using pymysql library and required access keys
    connection = pymysql.connect(
        host=config['db']['host'],
        user=config['db']['user'],
        password=config['db']['password'],
        database=config['db']['database']
    )

    # creating cursor object to execute SQL query
    # SQL query: f"SELECT * FROM {table_name}": select everything from table_name(Burger_sales_data)
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")

    # query the description and fetching all the data
    query_results_description = cursor.description
    query_results = cursor.fetchall()

    # closing the connection with DB
    connection.close()
    
    # getting column names from description
    colnames = [d[0] for d in query_results_description]

    # creating dataframe from the fetched data and columns
    df = pd.DataFrame(query_results, columns=colnames)
    
    return df

def preprocess_data(df : pd.DataFrame) -> pd.DataFrame:
    """
    Function to preprocess the data. 
    converting Date column as pandas datetime and converting Region to string
    Also getting all the date and region combination in data

    Input:
    df: dataframe to preprocess

    Output:
    df: processed dataframe
    """
    # converting Date column to pandas datetime
    df['Date']= pd.to_datetime(df['Date'], dayfirst=True)

    # converting Region to string
    df['Region'] = df['Region'].astype(str)

    # dropping duplicates based on Date and Region
    df = df.drop_duplicates(subset=['Date', 'Region']).sort_values(['Date', 'Region']).reset_index(drop=True)
    
    # taking unique values from Date and Region column
    dates = df[['Date']].drop_duplicates().sort_values('Date')
    regions = df[['Region']].drop_duplicates().sort_values('Region')

    # creating all the combinations of Date and Region in the dataset
    df = pd.merge(dates.assign(k=1), regions.assign(k=1), on='k').drop(columns='k').merge(df, on=['Date', 'Region'], how='left')
        
    return df

def get_windowed_data(
    df: pd.DataFrame,
    features : typing.List[str],
    target : str,
    lag : int = 1,
    window_size : int = 14,
    
) -> pd.DataFrame:
    """
    Function to window the data

    Input:
    df: pandas dataframe
    features: list of feature columns
    target: target column
    lag: lag to create data
    window_size: window size to create data
    
    Output:
    res: window dataframe
    """
    
    # getting unique dates and region from dataframe
    dates = df[['Date']].drop_duplicates().sort_values('Date')
    regions = df[['Region']].drop_duplicates().sort_values('Region')

    out = list()

    for target_date in dates['Date']:

        # filtering data for target date
        A = df[df['Date'] == target_date][['Region', target]]
        df_target = A.rename(columns={target: 'Target'})
        dfi = df.copy()

        # adding new column delta_days as the difference between target_date and date in each row
        dfi['delta_days'] = (target_date - df['Date']).dt.days

        # selecting rows based on window and lag
        dfi = dfi[(dfi['delta_days'] >= lag) & (dfi['delta_days'] < lag + window_size)][['Date', 'Region'] + features]
        
        # loop to check for missing values
        # in this case, we have not done any operation to fill the missing values
        if dfi.shape[0] < window_size * len(regions):
            continue

        # creating a list of values based on lag and window size for each target date
        x = dfi.sort_values('Date').groupby('Region').agg(lambda x: list(x)).merge(df_target, on='Region').assign(TargetDate=target_date)
        out.append(x)

    # concatenating all the data    
    res = pd.concat(out, axis=0)

    # dropping rows where Target(sales) is missing
    res = res[~res['Target'].isna()]
        
    return res
