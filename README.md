# COMS4111 Project 1 Part 3
- PostgreSQL account: wz2557
- URL of web application: http://

## Description of Implemented parts 
We were able to implement all the functionalities proposed in part 1.
<br>
<br>
As newcomers to a city, we never know nor have connections who can tell us which part of the city is dangerous. As 
international students ourselves, this was certainly a concern for us as well as our families who worry about us every 
day overseas. This is where we came up with the idea of making a database based on crimes in the U.S. In this 
application, we will be able to look for crimes related to specific locations (states) within the U.S. to identify dangerous 
locations that newcomers should avoid. For each location, we will display data such as the crime rate, past crime 
history, and locations of police offices. In addition to these fundamental functionalities, we will extend this app to 
display the details of the crime as well as display the missing and wanted person to branch for help to the public. 
Another aspect we intend to tackle is the current issue of police brutality. Since we will have a record of the police 
departments as well as the police officer’s identification number with their associated charges, we hope to have a 
positive impact on the officers’ actions (such as them having a second thought before doing the wrong) since they will 
be publicly organized and displayed.

## Two web pages with the most interesting database operations
1.The location page is interesting because its output comes from multiple database tables and queries. We use SELECT COUNT(*) and WHERE table.state=user input state to get the number of crimes, police offices, police crimes, homicides, missing people, and fugitives in the selected state. The total number of crimes is equal to the sum of homicides and police crimes. This page is used to give the user an overview of how safe/unsafe the chosen state is.  
2. The police crimes page is also interesting because it allows the user to get detailed information on police crimes in the selected state. It first uses the user input to find police crimes that happened in the selected state. Then it finds the corresponding victim's information by matching case_id in Police_Crimes_Work_At table and Police_crime_victims table. This page displays both police officers' and victims' information, including age, race, sex, etc. 

# Instructions
1. Create virtual environment with
<br>`python3 -m venv crimes_database`

2. Activate virtual environment with
<br>`source crimes_database/bin/activate`

3. Install dependencies with
<br>`pip install -r requirements.txt`

4. Run server with 
<br>`python server.py`

5. Optional: to add dependencies, use pip, then include it in requirements.txt by
<br>`pip freeze > requirements.txt`
