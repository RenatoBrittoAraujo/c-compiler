#  C Compiler

This is a C compiler

I expect to turn C code to:
- A JSON Syntax Tree
- Then to Python source code
- Then to a ubuntu docker container executable (only printf function gets to be implemented from the standard lib)
- Then Create a linker, to try and implement all functions from the standard lib.
- Then Create a pre-processor.

# current open questions

[TODO]:
- Find out if any rules of a procedure are not being validated
- Decide inheritance rules for syntax tree classes (make it 3FN)
- Add string escaping of '"' 
- Add global variable definition
- Add pointers and derefences (every type gets new nested pointer count)
- Add parenthesis expressions
- Add if, else if and else
- Add comparisons
- Add for, while
- Add floats
- Compile the C code to python
- Use a docker container to compile to standard system to ease development of actual C to machine code
- Preprocessor
- Linking
- Another project: compile Python to C (god knows how)

[Dont really care]:
- Type checking (may have some tough problems for educational value, but I can't detect them at the moment)
- Advanced error checking (takes time, barely any value)
- Error handling (to find all error within source code. takes time, no value if can just use a working C compiler already to see all error if I want and also it's just plaing boring dev work)

# Things ive learned

Write an interpreter of BNF and then use a BNF gramatic to accomplish the goal as is being currently done via ifs and elses


# v1

- Read C code and build a syntax tree
- Print the syntax tree json

# v2

- Add support to all possible C code (if, for, while, pointers...)

# v3
