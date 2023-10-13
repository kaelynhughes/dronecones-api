# Dronecones API

## To start the server:

`flask --app api run --debug`

## To start running the database:

`flask --app api init-db`


## User flask shell:

`flask --app api shell`

### would print all drones
```
import os
import sqlite3

# Get the path to the database file in the "instance" folder
db_path = os.path.join(app.instance_path, 'api.sqlite')

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Execute an SQL query
cursor.execute('SELECT display_name, drone_size, owner_id FROM drone')

# Fetch the results
results = cursor.fetchall()

# Display the data
for row in results:
    display_name, drone_size, owner_id = row
    print(display_name, drone_size, owner_id)

# Close the database connection
conn.close()
```