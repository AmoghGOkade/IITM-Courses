import time

class Tree:
    def __init__(self, initval=None):
        self.value = initval
        if self.value != None:
            self.left = Tree()
            self.right = Tree()
            self.height = 1
        else:
            self.left = None
            self.right = None
            self.height = 0
    def __str__(self):
        return(str(self.inorder()))

    def slope(self):
        return self.left.height - self.right.height
    def isempty(self):
        return (self.value == None)
    def isleaf(self):
        temp = (self.value != None) and (self.left.isempty()) and (self.right.isempty())
        return temp
    
    def inorder(self):
        if self.isempty():
            return([])
        else:
            return (self.left.inorder() + [self.value] + self.right.inorder())
    def find(self, v):
        if self.isempty():
            return False
        if self.value == v:
            return True
        if self.value < v:
            return self.right.find(v)
        if self.value > v:
            return self.left.find(v)
    def minval(self):
        if self.left.isempty():
            return self.value
        else:
            return self.left.minval()
    def maxval(self):
        if self.right.isempty():
            return self.value
        else:
            return self.right.maxval()

    #deleteing a value
    def makeempty(self):
        self.value = None
        self.left = None
        self.right = None
        self.height = 0
    def copyleft(self):     #promote the left child as the node
        self.value = self.left.value
        self.right = self.left.right
        self.left = self.left.left
    def copyright(self):
        self.value = self.right.value
        self.left = self.right.left
        self.right = self.right.right
    def delete(self, v):
        if self.isempty():
            print("No node with value", v)
            return
        if v < self.value:
            self.left.delete(v)
            self.rebalance()
            self.height = 1 + max(self.left.height, self.right.height)
        elif v > self.value:
            self.right.delete(v)
            self.rebalance()
            self.height = 1 + max(self.left.height, self.right.height)
        elif v == self.value:
            print("Deleting", self.value)
            if self.isleaf():
                self.makeempty()
            elif self.left.isempty():
                self.copyright()
            elif self.right.isempty():
                self.copyleft()
            else:
                self.value = self.left.maxval()
                self.left.delete(self.left.maxval())

    #balancing functions for AVL tree
    def leftrotate(self):
        newleft = Tree(self.value)
        newleft.left = self.left
        newleft.right = self.right.left

        self.value = self.right.value
        self.right = self.right.right
        self.left = newleft
    def rightrotate(self):
        newright = Tree(self.value)
        newright.left = self.left.right
        newright.right = self.right

        self.value = self.left.value
        self.left = self.left.left
        self.right = newright
    def rebalance(self):
        if self.slope() == 2:     #left is bigger by 2 levels
            if self.left.slope() == -1:
                print("Left and then right rotation needed")
                self.left.leftrotate()
                self.rightrotate()
            else:
                print("Right rotation needed")
                self.rightrotate()
        elif self.slope() == -2:    #right is bigger by 2 levels
            if self.right.slope() == 1:
                print("Right and then left rotation needed")
                self.right.rightrotate()
                self.leftrotate()
            else:
                print("Left rotation needed")
                self.leftrotate()

    #inserting a value
    def insert(self, v):
        if self.isempty():
            print("Inserting", v)
            self.value = v
            self.left = Tree()
            self.right = Tree()
            
            self.height = 1
            return
        if self.value == v:     #no duplicates allowed
            print("Node of value", v, "already exists")
            return
        if v > self.value:
            self.right.insert(v)
            self.rebalance()
        elif v < self.value:
            self.left.insert(v)
            self.rebalance()
        self.height = 1 + max(self.left.height, self.right.height)

    #plotting (visualization)
    def plot(self, sleep = 1):
        if self.isempty() == False:
            import turtle
            t=turtle.Turtle()
            self.plot_rec(t, 0, 0)
            time.sleep(sleep)
            t.clear()

    def plot_rec(self, t, x, y):    #x and y passed here is the coordinate above which circle should be drawn from
        if self.isempty():
            return
        self.t = t
        
        self.plot_node(x, y)
        if self.left.isempty() == False:
            (new_x, new_y) = self.plot_line(-1, x, y)    #line should always be plotted with the called x and y
            self.left.plot_rec(self.t, new_x, new_y)
        if self.right.isempty() == False:
            (new_x, new_y) = self.plot_line(1, x, y)   
            self.right.plot_rec(self.t, new_x, new_y)
        
    def plot_node(self, x, y):      #plots the circle above the passed x,y and prints the value using the turtle
        self.t.pendown()
        self.t.circle(10)
        self.t.penup()
        self.t.goto(x-2, y+3)
        self.t.write(str(self.value))

    def plot_line(self, dire, x, y):    #goes to the start point of the line (left or right depends on dire), draws the line and calculates (returns) the coords above which the circle should be drawn
        self.t.penup()
        self.t.goto(x+dire*10/(2**0.5), y+10-10/(2**0.5))
        self.t.pendown()
        self.t.goto(x+dire*30/(2**0.5), y+10-30/(2**0.5))
        self.t.penup()
        self.t.goto(x+dire*40/(2**0.5), y-40/(2**0.5))
        x += dire*40/(2**0.5)
        y -= 40/(2**0.5)
        return (x, y)   #x and y above which the next circle needs to be drawn
                
root = Tree(10)
l = [20, 30, 40, 50, 25, 50]
for i in l:
    root.insert(i)
    root.plot()
l = [50, 40, 10]
for i in l:
    root.delete(i)
    root.plot(3)
