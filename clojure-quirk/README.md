# clojure-quirk

## How To Run

If using leiningen, you can download the entire project folder and run the program without any compilation.

On the command line, change to the project's directory. Make sure that the quirk file you would like to pipe in is either in the same directory, or its path is fully specified.

You can run the program with:

`lein run < testQuirkFile.q`

If you would like to run the compiled file, you can run the program with:

`java -jar target/clojure-quirk-0.1.0-SNAPSHOT-standalone.jar < testFile.q`

Running the compiled file works a bit more quickly, but either will yield the same results.
