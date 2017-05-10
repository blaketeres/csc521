(ns clojure-quirk.core
  (:gen-class)
  (:require [instaparse.core :as insta])
  (:use [clojure.pprint]))

(defn setValue [symbolTable varname value]
  "Function used to bind a name in scope"
  (if value
    (swap! symbolTable merge
           {(keyword varname) value}))
  [])

(defn checkTable [symbolTable varitem]
  "Function used to look up a name in scope"
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

(defn callByLabel [label & args]
  "Calls a function by its label"
  (apply (ns-resolve 'clojure-quirk.core (symbol (name label))) args))

(defn interpretQuirk [subtree]
  "Begins the parse tree traversal"
  (callByLabel (first subtree) subtree (atom {})))

(defn Program [subtree scope]
  (cond

    ; Program0 (<Statement> <Program>)
    (= (count subtree) 3)
    (do (callByLabel (first (second subtree)) (second subtree) scope)
      (callByLabel (first (third subtree)) (third subtree) scope))

    ; Program1 (<Statement>)
    :default
    (callByLabel (first (second subtree)) (second subtree) scope)))

(defn Statement [subtree scope]

  ; Statement0/1/2 (FunctionDeclaration | Assignment | Print)
  (callByLabel (first (second subtree)) (second subtree) scope))

(defn FunctionDeclaration [subtree scope]

  ; FunctionDeclaration (FUNCTION Name LPAREN FunctionParams LBRACE FunctionBody RBRACE)
  (let [funcName (second (second (third subtree)))
        funcParams (into [] (callByLabel (first (fifth subtree)) (fifth subtree) scope))
        funcBody (seventh subtree)]
        (setValue scope funcName [funcParams funcBody])))

(defn FunctionParams [subtree scope]
  (cond

    ; FunctionParams0 (NameList RPAREN)
    (= :NameList (first (second subtree)))
    (callByLabel (first (second subtree)) (second subtree) scope)

    ; FunctionParams1 (RPAREN)
    :default
    []))

(defn FunctionBody [subtree scope]
  (cond

    ; FunctionBody0 (Program Return)
    (= :Program (first (second subtree)))
    (do (callByLabel (first (second subtree)) (second subtree) scope)
		  (callByLabel (first (third subtree)) (third subtree) scope))

    ; FunctionBody1 (Return)
    :default
    (callByLabel (first (second subtree)) (second subtree) scope)))

(defn Return [subtree scope]

  ; Return (RETURN ParameterList)
  (callByLabel (first (third subtree)) (third subtree) scope))

(defn Assignment [subtree scope]

  ; Assignment1/0 (SingleAssignment | MultipleAssignment)
  (callByLabel (first (second subtree)) (second subtree) scope))

(defn SingleAssignment [subtree scope]

  ; SingleAssignment (VAR Name ASSIGN Expression)
  (let [varName (second (second (third subtree)))
        varValue (callByLabel (first (fifth subtree)) (fifth subtree) scope)]
    (setValue scope varName varValue)))

(defn MultipleAssignment [subtree scope]

  ; MultipleAssignment (VAR NameList ASSIGN FunctionCall)
  (let [varNames (into [] (callByLabel (first (third subtree)) (third subtree) scope))
        varValues (into [] (flatten (conj [] (callByLabel (first (fifth subtree)) (fifth subtree) scope))))
        errorMessage1 (str "Too many variables for assignment.")]
    (if (> (count varNames) (count varValues))
      (throw (Exception. errorMessage1)))
    (loop [i 0]
      (when (< i (count varNames))
        (setValue scope (str (get varNames i)) (get varValues i))
        (recur (inc i))))))

(defn Print [subtree scope]

  ; Print (PRINT Expression)
  (println (callByLabel (first (third subtree)) (third subtree) scope)))

(defn NameList [subtree scope]
  (cond

    ; NameList0 (Name COMMA NameList)
    (= (count subtree) 4)
    (into [] (concat (callByLabel (first (second subtree)) (second subtree) scope)
                     (callByLabel (first (fourth subtree)) (fourth subtree) scope)))

    ; NameList1 (Name)
    :default
    (callByLabel (first (second subtree)) (second subtree) scope)))

(defn ParameterList [subtree scope]
  (cond

    ; ParameterList0 (Parameter COMMA ParameterList)
    (= (count subtree) 4)
    (into [] (list (callByLabel (first (second subtree)) (second subtree) scope)
                   (callByLabel (first (fourth subtree)) (fourth subtree) scope)))

    ; ParameterList1 (Parameter)
    :default
    (callByLabel (first (second subtree)) (second subtree) scope)))

(defn Parameter [subtree scope]

  ; Parameter0/1 (Expression/Name)
  (= :Expression 1)
  (callByLabel (first (second subtree)) (second subtree) scope))

(defn Expression [subtree scope]
  (cond

    ; Expression0/1 (Term ADD Expression/Term SUB Expression)
    (= (count subtree) 4)
    (let [term (callByLabel (first (second subtree)) (second subtree) scope)
          expression (callByLabel (first (fourth subtree)) (fourth subtree) scope)]
      (cond

        (= :ADD (first (third subtree)))
        (+ term expression)

        (= :SUB (first (third subtree)))
        (- term expression)))

    ; Expression2 (Term)
    :default
    (let [expression (callByLabel (first (second subtree)) (second subtree) scope)
          errorMessage (str "Expression " expression " does not result to a value.")]
      (if-not (instance? Number expression)
        (throw (Exception. errorMessage))
        expression))))

(defn Term [subtree scope]
  (cond

    ; Term0/1 (Factor MULT Term/Factor DIV Term)
    (= (count subtree) 4)
    (let [factor (callByLabel (first (second subtree)) (second subtree) scope)
          term (callByLabel (first (fourth subtree)) (fourth subtree) scope)]
      (cond

        (= :MULT (first (third subtree)))
        (* factor term)

        (= :DIV (first (third subtree)))
        (double (/ factor term))))

    ; Term2 (Factor)
    :default
    (callByLabel (first (second subtree)) (second subtree) scope)))

(defn Factor [subtree scope]
  ;(pprint subtree)
  (cond

    (= :SubExpression (first (second subtree)))
    (cond

      ; Factor0 (SubExpression EXP Factor)
      (= (count subtree) 4)
      (let [subExpression (callByLabel (first (second subtree)) (second subtree) scope)
            factor (callByLabel (first (fourth subtree)) (fourth subtree) scope)]
        (Math/pow subExpression factor))

      ; Factor1 (SubExpression)
      :default
      (callByLabel (first (second subtree)) (second subtree) scope))

    ; Factor2 (FunctionCall)
    (= :FunctionCall (first (second subtree)))
    (callByLabel (first (second subtree)) (second subtree) scope)

    :default
    (cond

      ; Factor3 (Value EXP Factor)
      (= (count subtree) 4)
      (let [value (callByLabel (first (second subtree)) (second subtree) scope)
            factor (callByLabel (first (fourth subtree)) (fourth subtree) scope)]
        (Math/pow value factor))

      ; Factor4 (Value)
      :default
      (callByLabel (first (second subtree)) (second subtree) scope))))

(defn FunctionCall [subtree scope]
  (cond

    ; FunctionCall0 (Name LPAREN FunctionCallParams COLON Numb)
    (= (count subtree) 6)
    (let [funcScope scope
          funcName (second (second (second subtree)))
          funcCallParams (into [] (flatten (conj [] (callByLabel (first (fourth subtree)) (fourth subtree) scope))))
          numParamsRequired (count (first (checkTable scope funcName)))
          funcBody (checkTable scope funcName)
          funcParamVars (first funcBody)
          funcReturnIndex (int (callByLabel (first (sixth subtree)) (sixth subtree) scope))
          errorMessage1 (str "Call to function " funcName " has wrong number of arguments")
          errorMessage2 (str "Call to function " funcName " tries to return index out of range")]
      (if (not= (count funcCallParams) (count funcParamVars))
        (throw (Exception. errorMessage1)))
      (loop [i 0]
        (when (< i numParamsRequired)
          (setValue funcScope (str (get funcParamVars i)) (get funcCallParams i))
          (recur (inc i))))
      (setValue funcScope funcName (checkTable scope funcName))
      (if (nil? (get (into [] (flatten (callByLabel (first(second (get @funcScope (keyword funcName)))) (second (get @funcScope (keyword funcName))) funcScope))) funcReturnIndex))
        (throw (Exception. errorMessage2)))
      (get (into [] (flatten (callByLabel (first(second (get @funcScope (keyword funcName)))) (second (get @funcScope (keyword funcName))) funcScope))) funcReturnIndex))

    ; FunctionCall1 (Name LPAREN FunctionCallParams)
    :default
    (let [funcScope scope
          funcName (second (second (second subtree)))
          funcCallParams (into [] (flatten (conj [] (callByLabel (first (fourth subtree)) (fourth subtree) scope))))
          numParamsRequired (count (first (checkTable scope funcName)))
          funcBody (checkTable scope funcName)
          funcParamVars (first funcBody)
          errorMessage (str "Call to function " funcName " has wrong number of arguments")]
      (if (not= (count funcCallParams) (count funcParamVars))
        (throw (Exception. errorMessage)))
      (loop [i 0]
        (when (< i numParamsRequired)
          (setValue funcScope (str (get funcParamVars i)) (get funcCallParams i))
          (recur (inc i))))
      (setValue funcScope funcName (checkTable scope funcName))
      (callByLabel (first (second (get @funcScope (keyword funcName)))) (second (get @funcScope (keyword funcName))) funcScope))))

(defn FunctionCallParams [subtree scope]
  (cond

    ; FunctionCallParams0 (ParameterList RPAREN)
    (= :ParameterList (first (second subtree)))
    (callByLabel (first (second subtree)) (second subtree) scope)

    ; FunctionCallParams0 (RPAREN)
    :default
    []))

(defn SubExpression [subtree scope]

  ; SubExpression0 (LPAREN Expression RPAREN)
  (callByLabel (first (third subtree)) (third subtree) scope))

(defn Value [subtree scope]

  ; Value0/1 (Name/Number)
  (callByLabel (first (second subtree)) (second subtree) scope))

(defn Name [subtree scope]
  (cond

    ; Name0 (IDENT)
    (= :IDENT (first (second subtree)))
    (checkTable scope (second (second subtree)))

    :default
    (cond

      ; Name1 (SUB IDENT)
      (= :SUB (first (second subtree)))
      (- (double (checkTable scope (second (third subtree)))))

      ; Name2 (ADD IDENT)
      (= :ADD (first (second subtree)))
      (double (checkTable scope (second (third subtree)))))))

(defn Numb [subtree scope]
  (cond

    ; Number0 (NUMBER)
    (= :NUMBER (first (second subtree)))
    (double (read-string (second (second subtree))))

    :default
    (cond

      ; Number1 (SUB NUMBER)
      (= :SUB (first (second subtree)))
      (- (double (read-string (second (third subtree)))))

      ; Number2 (ADD NUMBER)
      (= :ADD (first (second subtree)))
      (double (read-string (second (third subtree)))))))

(defn -main [& args]
  (def quirk (insta/parser (clojure.java.io/resource "quirkGrammar.ebnf") :auto-whitespace :standard))
  (def quirkParseTree (quirk (slurp *in*)))

  (if (.equals "-pt" (first *command-line-args*))
    (def SHOW_PARSE_TREE true))
  (if (= true SHOW_PARSE_TREE)
    (pprint quirkParseTree)
    (interpretQuirk quirkParseTree)))
