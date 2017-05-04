# clojure-quirk

## How To Run

If using leiningen, you can download the entire project folder and run the program without any compilation.

On the command line, change to the project's directory. Make sure that the quirk file you would like to pipe in is either in the same directory, or its path is fully specified.

You can run the program with:

`lein run < testQuirkFile.q`

If you would like to run the compiled file, you can compile/run the program with two commands:

```
lein uberjar
java -jar target/clojure-quirk-0.1.0-SNAPSHOT-standalone.jar < testFile.q
```

Running the compiled file works a bit more quickly, but either will yield the same results.

My interpreter supports dynmaic rebinding of variables and functions, as well as nested function declarations. The atom {} structure and access methods used were inspired by the interpreter found in the link below:

https://github.com/javazquez/arnoldclj_interpreter/blob/master/src/arnoldclj_s/interpreter.clj

I modified its structure to work locally upon whatever scope is specified, rather than on a global table. This allows scope to be limited to the confines of a function's braces.

My interpreter declares a valid and invalid way to use multiple assignments on function calls. Use this function as an example:
```
function myFunc() {
  return 4, 3, 5
}
```
### Valid
```
var a = myFunc()
var a, b = myFunc()
var a, b, c = myFunc()
var a = myFunc():2
var b = myFunc():0
```
### Invalid

```
var a, b, c, d = myFunc()   // Assignment out of range of function return values
var a, b, c = myFunc():1    // Multiple assignments to one variable
```


