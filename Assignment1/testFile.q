&&&&

function SquareDistance(x1, y1, x2, y2) {
  return x1 ^ x2 + y1 ^ y2
}

function areaOfSquare(x) {
  return x ^ 2
}

function areaOfRectangle(x, y) {
  return x * y
}

function multipleReturn(a, b, c) {
  var d = a + b + c
  return a, b, c, d
}


var a = 5
var b = -2.1234
var c=   9
var d = 1.5

var e
=
8

var distance1 = SquareDistance(2, 3, 5, 6)

var distance2= SquareDistance(a, 2, b, 5)

var squareArea1 =areaOfSquare(7)

var squareArea2=areaOfSquare(d)

var rectangleArea1     =     areaOfRectangle(2   ,    10)

var       rectangleArea2=areaOfRectangle(e,6)

var aa, bb, cc, dd = multipleReturn(1, 2, 3)

     var   multipleReturnNoIndex =      multipleReturn(3, 4, 5)

var indexedReturn = multipleReturn(5, 6, 9):3


print distance1
print distance2
print squareArea1
print squareArea2
print rectangleArea1
print rectangleArea2
print aa
print bb
print cc
print dd
print multipleReturnNoIndex
print indexedReturn
