Syntax guided synthesis

syn: spec × G × I -> prog
The synthesis algorithm tries to find the program in grammar G such that
all the inputs in I satisfy the spec.

Our task:
syn: ?? × G × good configs × bad configs -> constraint
We don't have a "spec". Instead, we want to synthesize some constraints
such that for all good config files, the constraint is true, and
for all bad configs, the constraint is false.
