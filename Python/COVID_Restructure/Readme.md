This script is designed to extract data from the COVID RedCap database, perform the necessary transformations, and load it into our main SQL database. 

Author
Hugo Soriano

Requirements
Before running the script, ensure you have the following Python libraries installed:

pandas
datacompy
sqlalchemy
numpy
pyodbc (for SQL database connection)

Script Overview
1. Logger Initialization
The script begins by setting up a logger to capture debug and informational messages throughout the execution.

2. Extract Function
The extract_table function is responsible for extracting data from a specified SQL table and returning it as a Pandas DataFrame.

3. Load Function
The load_data function loads the transformed data back into the specified SQL table.

4. Data Transformation and Loading
The script performs various transformations on the extracted data, including sorting, grouping, and restructuring the dataset before loading it back into the database. The script processes multiple tables, including:

ImpactContactScheduling_A
ImpactIdd_A
ImpactAnth_A
ImpactBP_A
ImpactSmokedrink_A
ImpactMhxmed_A
ImpactDmhxmed_A
ImpactEkg_A
ImpactFamilyhx_A
ImpactLab_A
CRLDATA_A
ImpactCover_A

Usage
Prepare the Configuration File: Ensure you have a config.py file that contains your SQL connection details. The script expects the following structure:

python
Copy code
sql = {
    'user': 'your_username',
    'server': 'your_server',
    'db': 'your_database',
    'driver': 'your_driver',
    'authentication': 'your_authentication_method'
}

Make sure the following path points to the correct RedCap csv export.

df_covid=pd.read_csv(r'C:\Users\hsoriano\Documents\Python\Data Analyst Portfolio\Python\COVID_Restructure\COHORTCOVID19_DATA_2023-04-21_0933.csv')

