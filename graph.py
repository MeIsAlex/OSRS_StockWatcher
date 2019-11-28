import pygame
green = (0, 255, 0)
red = (255, 0, 0)
black = (0, 0, 0)
gray = (128,128,128)

# the graph class stores everything we need to calculate and draw the graph
class Graph:
    def __init__(self, maxVal, values, screen, name):
        self.start_x = 190
        self.name = name
        self.screen = screen
        self.start_y = 450
        self.val_y = values
        self.cords_y = []
        self.node_val = []
        self.lines = []
        self.max_values = maxVal  # use itemdate to find max values
        self.increment = 0
        self.max_y = 0
        self.min_y = 0

    # finds the max and min value of all the items
    # we need this to dynamically change values on y-axis
    def find_min_max(self):
        if len(self.val_y) > 0:
            self.max_y = max(max(x) for x in self.val_y)
            self.min_y = min(min(x) for x in self.val_y)

    # calculate the values on the dots of the y-axis
    def cal_node(self):
        diff = self.max_y - self.min_y
        temp = diff / (self.max_values - 1)
        for y in range(self.max_values):
            value = self.min_y + (y * temp)
            self.node_val.append(round(value))
        self.node_val

    # draw the x and y axis
    def plot_axis(self):
        pygame.draw.line(self.screen, black, (self.start_x, self.start_y), (self.start_x, (self.start_y - 420)), 3)
        pygame.draw.line(self.screen, black, (self.start_x, self.start_y), ((self.start_x + 420), self.start_y), 3)

    # draw the dots on x and y axis and places values on y-axis
    # values x-axis coming soon
    def plot_points(self):
        if len(self.val_y) > 0:
            myfont = pygame.font.SysFont('Comic Sans MS', 10)
            increment = int(420 / self.max_values)
            val = self.max_values
            for y in range(self.max_values):
                val -= 1
                cord_x = self.start_x + (y * increment)
                pygame.draw.circle(self.screen, black, (cord_x, self.start_y), 3)
                textsurface = myfont.render(str(val), False, black)
                self.screen.blit(textsurface, (cord_x-3, self.start_y))
            for y in range(self.max_values):
                cord_y = self.start_y - (y * increment) - increment
                textsurface = myfont.render(str(self.node_val[y]), False, black)
                textwidth = textsurface.get_width()
                self.screen.blit(textsurface, (self.start_x - textwidth - 3, cord_y-10))
                pygame.draw.circle(self.screen, black, (self.start_x, cord_y), 3)
                pygame.draw.line(self.screen, gray, (self.start_x, cord_y), ((self.start_x + 420), cord_y), 1)

    # make line classes
    def make_line(self):
        i = 0
        for x in self.val_y:
            self.lines.append(Line(self.start_x, self.start_y, i, x, self.max_y, self.min_y, self.max_values, self.screen, self.name[i]))
            i += 1

    # calls function for each item
    def draw_line(self):
        if len(self.lines) > 0:
            for i in range(len(self.lines)):
                self.lines[i].cal_val_y()
                self.lines[i].draw_cords()
        self.lines = []


# class containing everything to calculate and draw 1 item
# call multiple times to draw more lines
class Line:
    def __init__(self, startx, starty, num, x, max_y, min_y, max_val, screen, name):
        self.startx = startx
        self.starty = starty
        self.num = num
        self.name = name
        self.val_y = x
        self.cords_y = []
        self.max_y = max_y
        self.min_y = min_y
        self.max_values = max_val
        self.screen =screen

    # calculate the coordinates of the values
    def cal_val_y(self):
        incr = 420 / self.max_values
        if len(self.val_y) > 0:
            diff = self.max_y - self.min_y
            temp = diff / (self.max_values - 1)
            for y in range(self.max_values):
                value = (incr * (self.val_y[y] - self.min_y) / temp)
                self.cords_y.append(int(self.starty - value - incr))

    # draw the coordinates as a line graph
    def draw_cords(self):
        incr = int(420 / self.max_values)
        myfont = pygame.font.SysFont('Comic Sans MS', 10)
        textsurface = myfont.render(self.name, False, black)
        textwidth = textsurface.get_width()
        textheight = textsurface.get_height()
        if len(self.val_y) > 0:
            for y in range(self.max_values - 1):
                cord_x1 = self.startx + (y * incr)
                cord_x2 = self.startx + ((y + 1) * incr)
                if self.cords_y[y] < self.cords_y[y + 1]:
                    pygame.draw.line(self.screen, red, (cord_x1, self.cords_y[y]), (cord_x2, self.cords_y[y + 1]), 2)
                else:
                    pygame.draw.line(self.screen, green, (cord_x1, self.cords_y[y]), (cord_x2, self.cords_y[y + 1]), 2)
        self.screen.blit(textsurface, (self.startx + ((len(self.val_y)-1) * 30)-textwidth, self.cords_y[self.max_values-1]-textheight-3))
