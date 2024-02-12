import pandas as pd
from sqlalchemy import create_engine
# Replace 'your_csv_file.csv' with the actual file name and 'your_table_name' with the desired table name in the database
csv_file = 'database/categories.csv'
table_name = 'categories'
# Create a DataFrame from the CSV file
df = pd.read_csv(csv_file)
# Replace 'your_username', 'your_password', 'your_host', and 'your_database' with your actual PostgreSQL credentials
engine = create_engine('postgresql://vegaventures2:.UZFYj##Qf,.@127.0.0.200:5432/vegaventures2_mydb')
# Load the DataFrame into the PostgreSQL database
df.to_sql(table_name, engine, index=False)