import psycopg2

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(database="vegaventures2_mytest_db", user="vegaventures2_mytest", password="K5lpSM8I+5Qp", host="127.0.0.200", port="5432")
cur = conn.cursor()

# Execute a SELECT query to fetch all data from a specific table
cur.execute("SELECT * FROM users")
# cur.execute("GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO vegaventures")
data = cur.fetchall()

# Print the fetched data
for row in data:
    print(row)

# Close the cursor and the connection
cur.close()
conn.close()