import turtle

t = turtle.Turtle()
t.speed(1)

t.penup()
t.goto(-20, 20)  
t.pendown()
t.pencolor("purple")
for _ in range(4):
    t.forward(40)
    t.right(90)

turtle.done()