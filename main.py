# need these 2 for api calls and multithreading
# check commented out functions
import requests
import threading
import json

from OSRS_StockWatcher.graph import Graph
from OSRS_StockWatcher.input import InputBox
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
itemDate = []

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
        print("Database OSRS could not be accessed")
        exit()

    # Close connection once done
    mydb.close()


# Get the last 14 days of data from an itemID and store in in the database
def getItemDataApi(itemID):
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
    itemdate = []  # Not used at the moment
    for result in myresult:
        itemDB.append((result['itemID'], result['itemName']))

    # Close connection once done
    mycursor.close()
    mydb.close()


# Convert name to itemID
def convertToID(name):
    # Loop through all items to check if the name corresponds to an ID
    for i in range(len(itemDB)):
        if name == itemDB[i][1]:
            return itemDB[i][0]
    return "-1"  # Return -1 in case the name wasn't found in the DB


# Get actual values from database
def setItemValuesFromDB(itemID):
    # Clear any old values in variables
    itemPrice.clear()
    itemDate.clear()

    # Connect to DB
    mydb = connectDB()
    mycursor = mydb.cursor(dictionary=True)
    # Get 14 latest values from DB for itemID
    mycursor.execute("SELECT * FROM item WHERE ID=" + str(itemID) + " ORDER BY time DESC LIMIT 14")
    myresult = mycursor.fetchall()

    for result in myresult:
        itemPrice.append(result['price'])
        itemDate.append(result['time'])

    # Close connection
    mycursor.close()
    mydb.close()

    # Turn values back in the right order (they are backwards)
    itemPrice.reverse()
    itemDate.reverse()


# ------------------------------------#
# Main program                       #
# ------------------------------------#

# Get all itemData from database
getItemsDB()

# Try to find item name in database, and grab the corresponding ID
try:
    # Possible item names Baby-, Young-, Gourmet-, Earth-, Essence-, Eclectic-, Nature-, Magpie-, Ninja- or Dragon Impling Jar
    itemID = convertToID("Eclectic Impling Jar")  # Change item name to change graph
    getItemDataApi(itemID)  # Update itemprices in database
    setItemValuesFromDB(itemID)  # Get all prices related to the ID from the last 14 days
except:
    print("Problem reading either itemName or itemID")
    setItemValuesFromDB(11260)  # In case of error, show Impling Jar prices

# Feed graph values to draw according to chosen ID
test_y = [itemPrice]

# Pygame initialisation
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 10)
# make_url_graph()
# url_item()
SCREEN = pygame.display.set_mode((640, 480))  # set the height and width of the screen
SCREEN.fill(white)  # make the screen white
graph = Graph(len(itemPrice), test_y,SCREEN)
box = InputBox(100, 25, 10, 10, myfont, SCREEN)
finish = False
while not finish:
    # call all the functions needed to do stuff
    SCREEN.fill(white)
    graph.find_min_max()
    graph.cal_node()
    graph.make_line()
    graph.draw_line()
    graph.plot_axis()
    graph.plot_points()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finish = True
        box.handle_event(event)
        box.remove_searches(event)
    box.show_searches()
    box.draw()
    pygame.display.flip()
