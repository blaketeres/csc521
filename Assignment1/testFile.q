function testFunction(a, b, d, g) {
    print a
    print b
    var c = a + b / g
    return c
}
var p = 10
var l = 20
var o = 19
var w = 18
var r = testFunction(p, l, o, w)
print r
