Python Program By: Cory Sollberger 4/25/16

A program that takes a (Context-Free Grammar) G ->(Alph, Vars, Rules, Start) defined as follows

Alph = { 'a', 'b', 'c' }, Vars = { P, Q, R, S, T, U, V, W, X, Y, Z }, Start = { S } and the Rules are as follows:
S -> aXT | YbT | UbZ | UWc | PQT, P -> aT, Q -> QT | aQ, T -> cT | e, U -> aU | e, X -> aX | R | e,
R -> aRb |e, Y -> Yb | R | e, V -> bVc | e, W -> Wc | V | e, Z -> bZ | V | e

The program generates n number of derivations below a specified derivation length from the above CFG "G".

Following the initial generation of derivations the program will then remove Epsilon (e) transitions from the grammar
which will then produce more derivations using the same defined traits.

Following the pattern above the grammar will be reduced by:

- Eliminating Unit Productions
- Eliminating Useless Variables and Rules
- Converting the grammar to Chomsky Normal Form that has no e-productions, unit productions, or useless variables
  and rules