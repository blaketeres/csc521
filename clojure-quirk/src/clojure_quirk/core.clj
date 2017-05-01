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
  (callByLabel (first subtree) subtree symbolTable))

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
  (let [funcName (second (second (third subtree)))]
    (let [funcParams (callByLabel (first (fifth subtree)) (fifth subtree) scope)]
      (let [funcBody (callByLabel (first (seventh subtree)) (seventh subtree) scope)]
        (assoc scope (varBindLoop funcParams funcBody))
        (println scope)))))
        ;(setValue funcName (list funcParams funcBody))))))

(defn FunctionParams [subtree scope]
  (println "FUNCTIONPARAMS")
  (cond
    
    ; FunctionParams0
    (= :NameList (first (second subtree)))
    (second subtree)
    
    ; FunctionParams1
    ; Do nothing
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
  (let [varName (second (second (third subtree)))]
    (let [varValue (callByLabel (first (fifth subtree)) (fifth subtree) scope)]
      (setValue varName varValue)
      {(keyword varName) (checkTable varName)})))

(defn MultipleAssignment [subtree scope]
  (println "MULTIPLEASSIGNMENT")
  (let [varNames (second (second (third subtree)))]
    (let [varValues (callByLabel (first (fifth subtree)) (fifth subtree) scope)])))
      ;(let [i 0] (take (count varNames)
                       ;(iterate (inc i (setValue (nth varName i) (nth varValues i)))))))))
    ;{(keyword varName) (checkTable varName)}))

(defn Print [subtree scope]
  (println "PRINT")
  (let [valToPrint (callByLabel (first (third subtree)) (third subtree) scope)]
    (println valToPrint)))

(defn NameList [subtree scope]
  (println "NAMELIST")
  (cond
    
    ; NameList0 (Name COMMA NameList)
    (= (count subtree) 4)
    ((let [n1 (callByLabel (first (second subtree)) (second subtree) scope)]
       (let [n2 (callByLabel (first (fourth subtree)) (fourth subtree) scope)]
         (into [] (concat n1 n2)))))
    
    ; NameList1 (Name)
    :default
    (callByLabel (first (second subtree)) (second subtree) scope)))

(defn ParameterList [subtree scope]
  (println "PARAMATERLIST")
  (cond
    
    ; ParameterList0 (Parameter COMMA ParameterList)
    (= (count subtree) 4)
    ((let [p1 (callByLabel (first (second subtree)) (second subtree) scope)]
       (let [p2 (callByLabel (first (fourth subtree)) (fourth subtree) scope)]
         (into [] (concat p1 p2)))))
    
    ; ParameterList1 (Parameter)
    :default
    (callByLabel (first (second subtree)) (second subtree) scope)))

(defn Parameter [subtree scope]
  (println "PARAMETER")
    
  ; Parameter0/1 (Expression/Name)
  (= :Expression 1)
  (callByLabel (first (second subtree)) (second subtree) scope))

(defn Expression [subtree scope]
  (println "EXPRESSION")
  (cond
    
    ; Expression0/1 (Term ADD Expression/Term SUB Expression)
    (= (count subtree) 4)
    ((let [term (callByLabel (first (second subtree)) (second subtree) scope)]
       (let [expression (callByLabel (first (fourth subtree)) (fourth subtree) scope)]
	     (cond
			     (= :ADD (first (third subtree)))
           (+ term expression)
           (= :SUB (first (third subtree)))
           (- term expression)))))
      
    ; Expression2
    :default
    (callByLabel (first (second subtree)) (second subtree) scope)))

(defn Term [subtree scope]
  (println "TERM"))

(defn Factor [subtree scope]
  (println "FACTOR"))

(defn FunctionCall [subtree scope]
  (println "FUNCTIONCALL"))

(defn FunctionCallParams [subtree scope]
  (println "FUNCTIONCALLPARAMS"))

(defn SubExpression [subtree scope]
  (println "SUBEXPRESSION"))

(defn Value [subtree scope]
  (println "VALUE"))

(defn Name [subtree scope]
  (println "NAME"))

(defn Num [subtree scope]
  (println "NUMBER"))

(defn -main [& args]
  (def quirk (insta/parser (clojure.java.io/resource "quirkGrammar.ebnf") :auto-whitespace :standard))
  (def quirkParseTree (quirk (slurp *in*)))
   
  (if (.equals "-pt" (first *command-line-args*))
    (def SHOW_PARSE_TREE true))
  (if (= true SHOW_PARSE_TREE)
    (pprint quirkParseTree)
    (interpretQuirk quirkParseTree)))
