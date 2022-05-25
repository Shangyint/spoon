Syntax guided synthesis

syn: spec × G × I -> prog
The synthesis algorithm tries to find the program in grammar G such that
all the inputs in I satisfies the spec.

Our task:
syn: ?? × G × good configs × bad configs -> constraint
We don't have a "spec". Instead, we want to synthesis some constraints
such that for all good configs files, the constraint is true, and
for all bad configs, the constraint is false.
