import requests
import json
import time
import datetime

from graph import Graph
from input import InputBox
# pygame
import pygame
# Mysql database
import mysql.connector

# ------------------------------------#
# Global variables                   #
# ------------------------------------#

# Array with all IDs
itemDB = []
# Array to store itemprices and dates,
itemPrice = []
loadedIDs = dict()

# Some colors to make drawing easier and shorter
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (143, 241, 245)
green = (0, 255, 0)


# ------------------------------------#
# Functions                          #
# ------------------------------------#

# Connect to database function
def connectDB():
    # To connect to database, make sure database 'osrs' exists
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="osrs"
        )
        return mydb
    except:
        print("The OSRS database could not be accessed/found")
        print("Press ENTER to close the application")
        input()
        exit()

    # Close connection once done
    mydb.close()


# Get the last 14 days of data from an itemID from the API and store in in the database
def storeItemDataApi(itemID):
    # Connect to database
    mydb = connectDB()
    # API call to get ID data from the last 180 days
    response = requests.get("http://services.runescape.com/m=itemdb_oldschool/api/graph/" + str(itemID) + ".json")

    # convert to readable string
    readApi = json.dumps(response.json(), indent=0)
    readApi = readApi.splitlines()
    itemsApi = []
    timeApi = []
    priceApi = []

    # Only keep the 14 latest days of the item
    for x in range(168, 182):
        itemsApi.append(readApi[x])

    # Filter the JSON data so that we only keep the values we need (the time and price)
    for x in range(len(itemsApi)):
        timeEnd = itemsApi[x].find('"', 2)
        timeApi.append(itemsApi[x][1:timeEnd])
        priceStart = itemsApi[x].find(" ")
        if x == len(itemsApi) - 1:
            priceApi.append(itemsApi[x][priceStart + 1:])
        else:
            priceEnd = itemsApi[x].find(",")
            priceApi.append(itemsApi[x][priceStart + 1:priceEnd])

    # Delete all the data that is older than 14 days
    keepDate = getFourteenDaysAgo()
    sql = "DELETE FROM item WHERE id = %s AND time <= %s"
    values = [itemID, keepDate]
    mycursor = mydb.cursor()
    mycursor.execute(sql, values)
    mydb.commit()

    # Make SQL query to insert all new values
    sql = "INSERT INTO item (time, price, id) VALUES (%s, %s, %s)"
    values = []
    mycursor = mydb.cursor()
    for i in range(len(priceApi)):  # Do this for every value
        values = [timeApi[i], priceApi[i], itemID]
        try:
            mycursor.execute(sql, values)
            mydb.commit()
            # print(mycursor.rowcount, "was inserted.")
        except:  # If it couldn't be added, it probably already existed
            # print("Id: "+ str(itemID) +", time: "+ timeApi[i] + " already exists")
            pass

    # Close connection once done
    mycursor.close()
    mydb.close()


# Get list of item names and IDs
def getItemsDB():
    mydb = connectDB()
    mycursor = mydb.cursor(dictionary=True)
    sql = "SELECT * FROM itemname"
    mycursor.execute(sql)

    myresult = mycursor.fetchall()
    for result in myresult:
        itemDB.append((result['itemID'], str(result['itemName'].lower())))

    # Close connection once done
    mycursor.close()
    mydb.close()


# Convert name to itemID
def convertToID(name):
    # Convert the name to lowercase, since database entries are stored lowercase too
    name = name.lower()
    # Loop through all items to check if the name corresponds to an ID
    for i in range(len(itemDB)):
        if name == itemDB[i][1]:
            return [itemDB[i][0], name]
    return ["-1", 0]  # Return -1 in case the name wasn't found in the DB use zero as a dummy value


# Get actual values from database
def getItemValuesFromDB(itemID):
    # Clear any old values in variable
    itemPrice.clear()

    # Connect to DB
    mydb = connectDB()
    mycursor = mydb.cursor(dictionary=True)
    # Get 14 latest values from DB for itemID
    mycursor.execute("SELECT * FROM item WHERE ID=" + str(itemID) + " ORDER BY time DESC LIMIT 14")
    myresult = mycursor.fetchall()

    for result in myresult:
        itemPrice.append(result['price'])

    # Close connection
    mycursor.close()
    mydb.close()

    # Turn values back in the right order (they are backwards)
    itemPrice.reverse()


# Get the time fourteen days ago in miliseconds starting from 1/1/1970
def getFourteenDaysAgo():
    now = time.time()
    now = now * 1000
    # 14 days in miliseconds = 60 * 60 * 24 * 14 * 1000 = 1209600000 
    return int(round((now - 129600000), 0))


# ------------------------------------#
# Main program                       #
# ------------------------------------#

# Get all itemData from database
getItemsDB()

# Pygame initialisation
pygame.init()
pygame.font.init()
pygame.display.set_caption('OSRS Stockwatcher')
myfont = pygame.font.SysFont('arial', 15)
# make_url_graph()
# url_item()
SCREEN = pygame.display.set_mode((800, 480))  # set the height and width of the screen
SCREEN.fill(white)  # make the screen white
box = InputBox(150, 25, 10, 10, myfont, SCREEN)
test_y = []
names = []
oldsearch = None
finish = False
while not finish:
    # Call all the functions needed to do stuff
    SCREEN.fill(white)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finish = True
        box.handle_event(event)
        box.remove_searches(event)
    box.show_searches()
    search = box.get_searches()
    # Only update graph if something new is searched
    if oldsearch != search:
        names = []
        oldsearch = search
        test_y.clear()
        try:
            index = 0
            for boxtext in search:  # Check all items being searched
                # Check if the text is an item, then convert the name to the itemID
                test = convertToID(boxtext)
                itemID = test[0]
                names.append(test[1])  # get the name if it converts to an id
                if itemID != "-1":  # If -1 returned, item doesn't exist
                    # Check if the item is already loaded recently by checking loadedIDs
                    foundNoID = True
                    for key in loadedIDs:  # If the item was already loaded, use those values instead of doing another database call
                        if itemID == key:
                            test_y.append(loadedIDs[key])
                            foundNoID = False

                    if foundNoID:  # If the ID wasn't loaded yet, get it from the database
                        try: #Try to update prices in the database by calling osrs api for new data
                            storeItemDataApi(itemID)  # Update itemprices in database
                        except: #If not reachable, don't update database and use old data instead
                            pass
                        getItemValuesFromDB(itemID)  # Get all prices related to the ID from the last 14 days
                        loadedIDs[itemID] = itemPrice[:]  # Add the item to the loadedIDs
                        test_y.append(itemPrice)  # Add the prices to the list to draw
                else:
                    box.check_search(index)  # if item does not exist delete it from the searches
                index += 1
        except:
            pass
        
    box.draw()
    graph = Graph(len(itemPrice), test_y, SCREEN, names, 250, 450)
    graph.find_min_max()
    graph.cal_node()
    graph.make_line()
    graph.draw_line()
    graph.plot_axis()
    graph.plot_points()
    pygame.display.flip()
