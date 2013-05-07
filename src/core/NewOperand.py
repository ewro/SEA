"""
   Copyright (c) 2013 neuromancer
   All rights reserved.
   
   Redistribution and use in source and binary forms, with or without
   modification, are permitted provided that the following conditions
   are met:
   1. Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
   2. Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
   3. The name of the author may not be used to endorse or promote products
      derived from this software without specific prior written permission.

   THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
   IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
   OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
   IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
   INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
   NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
   DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
   THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
   (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
   THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from Location import *
import sys, copy
  
size_in_bits = {
    "BYTE"  : 8,
    "WORD"  : 16,
    "DWORD" : 32,
    "QWORD" : 64,
    "1"     : 1,
    "8"     : 8,
    "16"    : 16,
    "32"    : 32,
    "64"    : 64,
}

class Operand:

  def __init__(self, name, size):
    self.type = None
    self.name = str(name)
    self.mem_source = None
    self.mem_offset = None
    self.value      = None
    
    self.resize(size)
  
  def resize(self, new_size):
  
    self.size_in_bits = size_in_bits.get(str(new_size), 0)
    
    if (self.size_in_bits % 8 == 0):
      self.size_in_bytes = self.size_in_bits / 8
    else:
      self.size_in_bytes = () # bottom

    self.size = self.size_in_bits
      
  def getLocations(self):
    sys.exit("ERROR: getLocations not implemented!")
  
  def setValue(self, value):
    sys.exit("ERROR: setValue not implemented!")
  
  def getValue(self):
    sys.exit("ERROR: getValue not implemented!")
  
  def isVar(self):
    sys.exit("ERROR: isVar not implemented!")
    
  def isMem(self):
    sys.exit("ERROR: isMem not implemented!")
  
  def __str__(self):
    return self.name

  def __cmp__(self, op):
    return cmp(self.name,op.name)
  
  def __hash__(self):
    return hash(self.name)
    
  def copy(self):
    return copy.copy(self)
    
  
  #def __contains__(self, obj):
    #print "x", str(obj)
    #return isinstance(obj,self.__class__)

class ImmOp(Operand):
  def getLocations(self):
    
    r = []
    fmt = "%0."+str(2*self.size_in_bytes)+"x"
    
    if ("0x" in self.name):
      hx = fmt % int(self.name,16)
    else:
      hx = fmt % int(self.name,10)

    hx = hx[::-1]
    
    for i in range(0,2*self.size_in_bytes,2):
      r.append(ImmLoc("0x"+hx[i:i+2],i/2))
      
    r.reverse() 
    return r

  def getValue(self):
    if ("0x" in self.name):
      return int(self.name,16)
    else:
      return int(self.name,10)
      
  def isVar(self):
    return False
    
  def isMem(self):
    return False
      
  def __str__(self):
    fmt = "0x%0."+str(2*self.size_in_bytes)+"x"
    #print fmt
    if ("0x" in self.name):   
      return "imm:"+(fmt % (int(self.name,16)))
    else:
      return "imm:"+(fmt % (int(self.name,10)))
      

class AddrOp(Operand): # same as immediate
  def __str__(self):
    fmt = "0x%0."+str(2*self.size_in_bytes)+"x"
    #print fmt
    if ("0x" in self.name):   
      return "imm:"+(fmt % (int(self.name,16)))
    else:
      return "imm:"+(fmt % (int(self.name,10)))
      
  def isVar(self):
    return False
    
  def isMem(self):
    return False

#class AddrOp(Operand): # same as immediate
#  def getLocations(self):
#    
#    r = []
#    fmt = "%016x"#
    
#    if ("0x" in self.name):
#      hx = (fmt % int(self.name,16))
#    else:
#      hx = (fmt % int(self.name),10)

#    hx = hx[::-1]
    
#    for i in range(0,self.size,2):
#      r.append(Location.Addr("0x"+hx[i:i+2],i/2))
#    
#    r.reverse()
#    return r
#
#  def getValue(self):
#    if ("0x" in self.name):
#      return int(self.name,16)
#    else:
#      return int(self.name,10)

class pAddrOp(Operand):
  def __str__(self):
    fmt = "0x%0."+str(2*self.size_in_bytes)+"x)"
    #print fmt
    if ("0x" in self.name):   
      return "*(imm:"+(fmt % (int(self.name,16)))
    else:
      return "*(imm:"+(fmt % (int(self.name,10)))
      
  def isVar(self):
    return True
    
  def isMem(self):
    return True
  

class RegOp(Operand):

  def isVar(self):
    return True
    
  def isMem(self):
    return False
    
  def getLocations(self):
    
    r = []
    
    for i in range(0,self.size_in_bytes):
      r.append(RegLoc(self.name,i))
       
    return r

  def __str__(self):
    #return "reg:"+self.name
    return str(self.name)
    
  def setValue(self, value):
    self.value = value
    
  def getValue(self):
    assert(self.value <> None)
    return self.value

class pRegOp(Operand):

  def isVar(self):
    return True
    
  def isMem(self):
    return True

  def __str__(self):
    return "*(reg:"+self.name+")"

class NoOp(Operand):
  def __init__(self, name = None, size = None):
    self.name = ""
    self.size = 0
    
  def isVar(self):
    return False
    
  def isMem(self):
    sys.exit("Oh no!")

# taken from http://code.activestate.com/recipes/384122/
# definition of an Infix operator class
# this recipe also works in jython
# calling sequence for the infix is either:
#  x |op| y
# or:
# x <<op>> y

class Infix:
    def __init__(self, function):
        self.function = function
    def __ror__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))
    def __or__(self, other):
        return self.function(other)
    def __rlshift__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))
    def __rshift__(self, other):
        return self.function(other)
    def __call__(self, value1, value2):
        return self.function(value1, value2)

iss=Infix(isinstance)

#match = lambda obj, cons: obj.__class.
#isOp = 

