import turtle

t = turtle.Turtle()
t.speed(0)
t.hideturtle()

data = []
result = []
colors = ['red', 'blue', 'green']

def graph():
  #d = input('Enter data: ')
  screen = turtle.Screen()
  d = screen.textinput('Enter data','Enter data:')
  data.append(d)

  g = 0 # G is the sum of the list
  for i in data:
    g = g + int(i)

  increment = 100 / float(g) # Increment is the percentage that 1 represents. If the sum was 10, 1 would represent 10%. If the sum was 25, 1 would represent 4%.

  angles = []

  for i in range(len(data)):
    a = (float(increment) * float(data[i])) # Converting a data value to a percentage
    a *= 3.6 # converting the percentage to an angle
    angles.append(a)
  
  t.clear() # Resetting and drawing the border
  t.up()
  t.home()
  t.goto(100,0)
  t.lt(90)
  t.down()
  t.circle(100)
  
  for i in range(len(angles)):
    t.up()
    t.goto(0,0)
    t.down()
    t.color('black',colors[i%len(colors)])
    t.begin_fill()
    t.rt(angles[0]) # Turns the turtle by the first angle in the list
    t.fd(100) # Drawing the line between segments
    t.lt(90)
    t.circle(100, angles[0])
    t.end_fill()
    t.color('red')
    y = str(round((angles[0] / 3.6),2)) # Reversing the calculations to get a percentage from an angle and rounding to two places
    angles.remove(angles[0]) # Removing the first angle value so that the turtle rotates correctly on the next loop
    t.write(y+'%', font=('Arial', 16, 'normal')) # Writing the percent value on the lines
    t.color('black')