import pandas as pd
from pymongo import MongoClient

# Load the CSV
df = pd.read_csv('vgsales.csv')

# Rename columns for consistency
df.rename(columns={
    'Name': 'name',
    'Platform': 'platform',
    'Year_of_Release': 'year_of_release',
    'Genre': 'genre',
    'Publisher': 'publisher',
    'NA_Sales': 'na',
    'EU_Sales': 'eu',
    'JP_Sales': 'jp',
    'Other_Sales': 'other',
    'Global_Sales': 'global',
    'Critic_Score': 'critic_score',
    'Critic_Count': 'critic_count',
    'User_Score': 'user_score',
    'User_Count': 'user_count',
    'Developer': 'developer',
    'Rating': 'esrb_rating' 
}, inplace=True)

# Convert numeric fields
df['critic_score'] = pd.to_numeric(df['critic_score'], errors='coerce')
df['critic_count'] = pd.to_numeric(df['critic_count'], errors='coerce')
df['user_score'] = pd.to_numeric(df['user_score'], errors='coerce')
df['user_count'] = pd.to_numeric(df['user_count'], errors='coerce')

# Create nested 'sales' field
df['sales'] = df.apply(lambda row: {
    'na': row['na'],
    'eu': row['eu'],
    'jp': row['jp'],
    'other': row['other'],
    'global': row['global']
}, axis=1)

# Create nested 'ratings' field
df['ratings'] = df.apply(lambda row: {
    'critic_score': row['critic_score'],
    'critic_count': row['critic_count'],
    'user_score': row['user_score'],
    'user_count': row['user_count'],
    'esrb_rating': row['esrb_rating']
}, axis=1)

# Drop the now-flattened columns
df.drop(columns=['na', 'eu', 'jp', 'other', 'global', 'critic_score', 'critic_count', 'user_score', 'user_count', 'esrb_rating'], inplace=True)

# Convert DataFrame to list of documents
data = df.to_dict(orient='records')

# Connect to MongoDB
client = MongoClient('172.31.91.223', 27017)
db = client['video_game_db']
collection = db['games']

# Clear existing collection and insert
collection.delete_many({})
collection.insert_many(data)

print("vgsales data successfully inserted.")