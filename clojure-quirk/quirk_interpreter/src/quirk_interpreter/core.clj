(ns example.core
  (:require [instaparse.core :as insta]))

(def quirk
  (insta/parser
    (clojure.java.io/resource "quirkGrammar.ebnf") :auto-whitespace :standard))