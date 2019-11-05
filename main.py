# need these 2 for api calls and multithreading
# check commented out functions
import requests
import threading
# pygame
import pygame
# Mysql database
import mysql.connector

graph_data = []
item_data = []
# needed for the api calls (item id's) probably not important anymore
item_num = [4151, 4153, 4156]
# some colors to make drawing easier and shorter
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (143, 241, 245)
green = (0, 255, 0)

# To connect to database, make sure database 'osrs' exists
try:
    mydb = mysql.connector.connect(cd
        host="localhost",
        user="root",
        passwd="",
        database="osrs"
    )
except:
    print("Database OSRS could not be accessed")
    exit()

# Get actual values from database
# Currently getting values from ID 11248 (Electic Impling Jar)
mycursor = mydb.cursor(dictionary=True)
mycursor.execute("SELECT * FROM item WHERE ID=11248 ORDER BY time DESC LIMIT 10")

myresult = mycursor.fetchall()
itemprice = []
itemdate = []  # Not used at the moment
for result in myresult:
    itemprice.append(result['price'])
    itemdate.append(result['time'])  # Not used at the moment

# Turn values back in the right order (they are backwards)
itemprice.reverse()

# test values
test_y = [
    itemprice
]


# Fill out graph

# the graph class stores everything we need to calculate and draw the graph
class Graph:
    def __init__(self):
        self.start_x = 190
        self.start_y = 450
        self.val_y = []
        self.cords_y = []
        self.node_val = []
        self.lines = []
        self.max_values = len(itemdate)  # use itemdate to find max values
        self.increment = 0
        self.max_y = 0
        self.min_y = 0

    # finds the max and min value of all the items
    # we need this to dynamically change values on y-axis
    # also copy test_y to local array so we don't have to use globals everywhere
    def find_min_max(self):
        self.val_y = test_y.copy()
        if len(self.val_y) > 0:
            self.max_y = max(max(x) for x in self.val_y)
            self.min_y = min(min(x) for x in self.val_y)

    # calculate the values on the dots of the y-axis
    def cal_node(self):
        diff = self.max_y - self.min_y
        temp = diff / (self.max_values - 1)
        for y in range(self.max_values):
            value = self.min_y + (y * temp)
            self.node_val.append(round(value, 1))
        self.node_val

    # draw the x and y axis
    def plot_axis(self):
        pygame.draw.line(SCREEN, black, (self.start_x, self.start_y), (self.start_x, (self.start_y - 420)), 3)
        pygame.draw.line(SCREEN, black, (self.start_x, self.start_y), ((self.start_x + 420), self.start_y), 3)

    # draw the dots on x and y axis and places values on y-axis
    # values x-axis coming soon
    def plot_points(self):
        increment = int(420 / self.max_values)
        for y in range(self.max_values):
            cord_x = self.start_x + (y * increment)
            pygame.draw.circle(SCREEN, black, (cord_x, self.start_y), 3)
        for y in range(self.max_values):
            cord_y = self.start_y-(y * increment)-increment
            textsurface = myfont.render(str(self.node_val[y]), False, black)
            SCREEN.blit(textsurface, (self.start_x - 40, cord_y - 5))
            pygame.draw.circle(SCREEN, black, (self.start_x, cord_y), 3)

    # make line classes
    def make_line(self):
        i = 0
        for x in self.val_y:
            self.lines.append(Line(i, x, self.max_y, self.min_y, self.max_values))
            i += 1

    # calls function for each item
    def draw_line(self):
        if len(self.lines) > 0:
            for i in range(len(self.lines)):
                self.lines[i].cal_val_y()
                self.lines[i].draw_cords()


# class containing everything to calculate and draw 1 item
# call multiple times to draw more lines
class Line:
    def __init__(self, num, x, max_y, min_y, max_val, name="test"):
        self.num = num
        self.name = name
        self.val_y = x
        self.cords_y = []
        self.max_y = max_y
        self.min_y = min_y
        self.max_values = max_val

    # calculate the coordinates of the values
    def cal_val_y(self):
        incr = 420/self.max_values
        if len(self.val_y) > 0:
            diff = self.max_y - self.min_y
            temp = diff / (self.max_values-1)
            for y in range(self.max_values):
                value = (incr * (self.val_y[y] - self.min_y) / temp)
                self.cords_y.append(int(graph.start_y - value - incr))

    # draw the coordinates as a line graph
    def draw_cords(self):
        incr = int(420 / self.max_values)
        if len(self.val_y) > 0:
            for y in range(self.max_values - 1):
                cord_x1 = graph.start_x + (y * incr)
                cord_x2 = graph.start_x + ((y + 1) * incr)
                if self.cords_y[y] < self.cords_y[y + 1]:
                    pygame.draw.line(SCREEN, red, (cord_x1, self.cords_y[y]), (cord_x2, self.cords_y[y + 1]), 2)
                else:
                    pygame.draw.line(SCREEN, green, (cord_x1, self.cords_y[y]), (cord_x2, self.cords_y[y + 1]), 2)


# thx for skrx for an easy to understand solution
# https://stackoverflow.com/questions/46390231/how-to-create-a-text-input-box-with-pygame
class InputBox:
    def __init__(self, w, h, x, y, text=""):
        self.active = False
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = black
        self.amount = 0
        self.textarea = myfont.render(self.text, False, black)
        self.searches = []

    def draw(self):
        # draw a white rectangle to remove previous blitted value
        pygame.draw.rect(SCREEN, white, self.rect)
        if len(self.text) > 0:
            # blit the new values to the screen
            SCREEN.blit(self.textarea, (self.rect.x + 3, self.rect.y + 3))
        pygame.draw.rect(SCREEN, self.color, self.rect, 2)

    def handle_event(self, ev):
        # check for mousepress in box
        if ev.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(ev.pos):
                self.active = True
                self.color = blue
            else:
                self.active = False
                self.color = black

        # check for keypress
        if event.type == pygame.KEYDOWN:
            if self.active is True:
                if event.key == pygame.K_RETURN:
                    ret_val = self.text
                    self.text = ""
                    self.textarea = font1.render(self.text, False, black)
                    self.searches.append(Search(ret_val, (50 + self.amount * (25 + 5))))
                    self.amount += 1
                elif event.key == pygame.K_BACKSPACE:
                    # remove the last value
                    self.text = self.text[:-1]
                    self.textarea = font1.render(self.text, False, black)
                else:
                    # add the pressed input to the input
                    self.text += event.unicode
                    self.textarea = font1.render(self.text, False, black)

    def show_searches(self):
        for x in range(len(self.searches)):
            self.searches[x].draw()

    def remove_searches(self, ev):
        for x in range(len(self.searches)):
            if self.searches[x].events(ev) is True:
                self.searches.pop(x)

                self.amount -= 1


class Search:
    def __init__(self, text, y):
        self.text = text
        self.rect = pygame.Rect(10, y, 100, 25)
        self.remove = pygame.Rect(85, y, 25, 25)

    def draw(self):
        pygame.draw.rect(SCREEN, black, self.rect, 1)
        textarea = font1.render(self.text, False, black)
        SCREEN.blit(textarea, (self.rect.x + 3, self.rect.y + 3))
        pygame.draw.rect(SCREEN, black, self.remove, 1)
        pygame.draw.line(SCREEN, red, (self.remove.x, self.remove.y), (self.remove.x + 23, self.remove.y + 23), 3)
        pygame.draw.line(SCREEN, red, (self.remove.x, (self.remove.y + 23)), ((self.remove.x + 23), self.remove.y), 3)

    def events(self, ev):
        if ev.type == pygame.MOUSEBUTTONDOWN:
            if self.remove.collidepoint(ev.pos):
                return True


# we use this to make the url for the api
def url_graph():
    base_url = "http://services.runescape.com/m=itemdb_oldschool/api/graph/"
    url = base_url + str(item_num[0]) + ".json"
    # removes the first element in the list
    temp = item_num.pop(0)
    # put the element at the back of the list
    item_num.append(temp)
    get_graph(url)
    # recursive function calls itself every 5 secs
    threading.Timer(5.0, url_graph).start()


def url_item():
    base_url = "http://services.runescape.com/m=itemdb_oldschool/api/catalogue/detail.json?item="
    url = base_url + str(item_num[0])
    # removes the first element in the list
    temp = item_num.pop(0)
    # put the element at the back of the list
    item_num.append(temp)
    get_item(url)
    # recursive function calls itself every 5 secs
    threading.Timer(5.0, url_item).start()


def get_graph(_url):
    # used to get list of timestamps and prices of one item
    response = requests.get(_url)
    data = response.json()['daily']
    for d in data:
        price = data[d]
        graph_data.append([d, price])
    print(graph_data)
    # clear the array to remove the so its ready for the next call
    graph_data.clear()


def get_item(url_i):
    threading.Timer(5.0, get_item).start()
    response = requests.get(url_i)
    data = response.json()['item']
    itemid = data['id']
    name = data['name']
    price = data['current']['price']  # note this is the current price
    price_d = data['today']['price']  # this is the price change of today the actual price would be price - price_d
    item_data.append([itemid, name, price, price_d])
    print(item_data)
    item_data.clear()


pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 10)
font1 = pygame.font.SysFont('Comic Sans MS', 12)
# make_url_graph()
# url_item()
graph = Graph()
SCREEN = pygame.display.set_mode((640, 480))  # set the height and width of the screen
SCREEN.fill(white)  # make the screen white
box = InputBox(100, 25, 10, 10)
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
