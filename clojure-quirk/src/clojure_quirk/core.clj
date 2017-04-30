(ns clojure-quirk.core
  (:gen-class)
  (:require [instaparse.core :as insta])
  (:use [clojure.pprint]))

(def symbolTable (atom {}))

(defn setValue [varname value]
  (if value
    (swap! symbolTable merge
           {(keyword varname) value})) 
  [])

(defn checkTable [varitem]
  (let [variable (keyword varitem)]
    (if (contains? @symbolTable variable)
      (get @symbolTable variable) 
      varitem)))

; easy access functions
(defn third [aList] (nth aList 2))
(defn fourth [aList] (nth aList 3))
(defn fifth [aList] (nth aList 4))
(defn sixth [aList] (nth aList 5))
(defn seventh [aList] (nth aList 6))
(defn eighth [aList] (nth aList 7))

;this returns a map with local variable bindings when calling a function
(defn varBindLoop [paramList valueList]
  (if (= 1 (count paramList))
    (assoc {} (first paramList) (first valueList))
    (merge (assoc {} (first paramList) (first valueList))
      (varBindLoop
        (rest paramList)
        (rest valueList)))))

; call function by its label
(defn callByLabel [label & args]
  (apply (ns-resolve 'clojure-quirk.core (symbol (name label))) args))

(defn interpretQuirk [subtree]
  (callByLabel (first subtree) subtree {}))

(defn Program [subtree scope]
  (println "PROGRAM")
  (cond
    
		; Program0 (<Statement> <Program>)
		(= (count subtree) 3)
		((callByLabel (first (second subtree)) (second subtree) scope)
		  (callByLabel (first (third subtree)) (third subtree) scope))
  
	  ; Program1 (<Statement>)
	  :default
	  (callByLabel (first (second subtree)) (second subtree) scope)))

(defn Statement [subtree scope]
  (println "STATEMENT")
  
  ; Statement0/1/2
	(callByLabel (first (second subtree)) (second subtree) scope))

(defn FunctionDeclaration [subtree scope]
  (println "FUNCTIONDECLARATION")
  (def funcName (second (second (third subtree))))
  (def funcParams (callByLabel (first (fifth subtree)) (fifth subtree) scope))
  (def funcBody (callByLabel (first (seventh subtree)) (seventh subtree) scope))
  (setValue funcName (list funcParams funcBody)))

(defn FunctionParams [subtree scope]
  (println "FUNCTIONPARAMS")
  (cond
    
    ; FunctionParams0
    (= :NameList (first (second subtree)))
    (second subtree)
    
    ; FunctionParams1
    ; ---------------
    ))

(defn FunctionBody [subtree scope]
  (println "FUNCTIONBODY")
  (cond
    
    ; FunctionBody0
    (= :Program (first (second subtree)))
    ((callByLabel (first (second subtree)) (second subtree) scope)
		  (callByLabel (first (third subtree)) (third subtree) scope))
    
    ; FunctionBody1
    :default
    (callByLabel (first (second subtree)) (second subtree) scope)))

(defn Return [subtree scope]
  (println "RETURN")
  (callByLabel (first (third subtree)) (third subtree) scope))

(defn Assignment [subtree scope]
  (println "ASSIGNMENT")
  (callByLabel (first (second subtree)) (second subtree) scope))

(defn SingleAssignment [subtree scope]
  (println "SINGLEASSIGNMENT")
  (def varName (second (second (third subtree))))
  (def varValue (callByLabel (first (fifth subtree)) (fifth subtree) scope))
  (setValue varName varValue))

(defn MultipleAssignment [subtree scope]
  (println "MULTIPLEASSIGNMENT")
  (pprint subtree))

(defn Print [subtree scope]
  (println "PRINT")
  (def valToPrint (callByLabel (first (third subtree)) (third subtree) scope))
  (println valToPrint))

(defn NameList [subtree scope]
  (println "NameList"))

(defn ParameterList [subtree scope]
  (println "ParameterList"))

(defn Parameter [subtree scope]
  (println "Parameter"))

(defn Expression [subtree scope]
  (println "EXPRESSION"))

(defn Term [subtree scope]
  (println "Term"))

(defn Factor [subtree scope]
  (println "Factor"))

(defn FunctionCall [subtree scope]
  (println "FunctionCall"))

(defn FunctionCallParams [subtree scope]
  (println "FunctionCallParams"))

(defn SubExpression [subtree scope]
  (println "SubExpression"))

(defn Value [subtree scope]
  (println "Value"))

(defn Name [subtree scope]
  (println "Name"))

(defn Num [subtree scope]
  (println "Number"))

(defn -main [& args]
  (def quirk (insta/parser (clojure.java.io/resource "quirkGrammar.ebnf") :auto-whitespace :standard))
  (def quirkParseTree (quirk (slurp *in*)))
   
  (if (.equals "-pt" (first *command-line-args*))
    (def SHOW_PARSE_TREE true))
  (if (= true SHOW_PARSE_TREE)
    (pprint quirkParseTree)
    (interpretQuirk quirkParseTree)))
