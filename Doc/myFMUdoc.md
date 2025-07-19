 MyFMU short doc
 -
myFMU code is written by V Chevrier 
Ensem/université de Lorraine/ LORIA

contact : vincent DOT chevrier AT loria DOT fr


It is based on from fmpy library

Inspired by JAVAFmi library

Does not incude FMI 3.0

Version 0.2
-

new:
- methods to get parameters, input and output
- variable/parameters can be of more types 
# Libraries used


- ctypes
- PyQt5.QtWidgets
- fmpy
- shutil
# Methods 
##  constructor
parameter String the path to the fmu file

## Information about FMU


- **info**
prints variables from model description with causality and initial values if any

- **gui**
some graphical informations (use of gui function of fmpy)

    Note!
    
        many possibilities with gui, see docs
        possible to execute 32 bit in 64 bit env 
    BUT:some troubles with this possibility, may be has to be commented 
- **cosimInfo, getOutputList, getInputList, getParameterList** guess !
## Cosimulating
- **init**
*note: don't confuse with constructor*

extract fmu, and do useful steps to make fmu simulable
        
    - Parameters
  
        - start_time : initial time as double.
        - varvalues : a list of couple VarNAme (string) and its value
- **set**
assign values to parameters or inputs 
- parameters:
    - var (variable name(s))
      - val value(s) of variables

        - different syntax can be used
    
          - set(['a','b','c'],(1,2,3))
                    both are lists
          - set('a',1)
                    both are simple values
          - set(['a','b','c'],{ 'a':1, 'aprime':2, etc.})
                    a list and a dictionnary
          - set('a'- ,{ 'a':1, 'aprime':2, etc.})
                     a variable  and a dictionnary

 
- **get**

  - parameters :
      - varname (a list of name or a single value - String-)
      - a dictionary (if any)
  - syntax 
    - get('so')
    - get(['xo', 'io', 'bo', 'so'],res) where res is a non empty dictionnary
    - get('so',res)
  - return
     - variables values (a single one or the list of values according to the varname position parameter list)
     - SIDE EFFECT with dictionary: if a dictionnary is provided variable entries are modified
    
 - **terminate** 
   clean files, ..
   
-  **doStep**(time, step_size):
   basic call to fmpy dostep
   
   need to be improved but enough til now
   