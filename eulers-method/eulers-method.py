import math

deltaX = 0.000001
x = 0
y = 0

print("\n\n")
print("Starting at (" + str(x) + ", " + str(y) + ")")
print("with approximations at steps of " + str(deltaX))

endX = 2

def m(y, x):
	return math.sin(y) + x

def newY(oldY):
	return m(oldY, x) * deltaX + oldY

while x < endX:
	y = newY(y)
	x += deltaX
	pass

print("yields (" + str(x) + ", " + str(y) + ")")
