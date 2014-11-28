import sys 
sys.path.append('../gen-py')

from SpellService import SpellService
from SpellService.ttypes import *

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

# Spell Service handler Class
class SpellServiceHandler:
  def __init__(self):
    self.log = {}

#Spellcheck class
  
  def spellcheck(self,SpellRequest):
      dictionary={}    # Dictionary for O(1) lookup

# getting the stripped lines as keys to the dictionary
      with open("linuxwords") as f: 
          content=f.readlines()
          #print dictionary
          for line in content:
              stripped_line=line.strip()
              dictionary[stripped_line]= stripped_line
              
          

      spell_response=SpellResponse()
      spell_response.is_correct=[]
  
      if SpellRequest.to_check: 
          words=SpellRequest.to_check 

 # appending values 0 or 1 to the spellresponse
          for word in words: 
              if word in dictionary: 
                  spell_response.is_correct.append(1)
              else:
                  spell_response.is_correct.append(0)

          return spell_response
     
  
handler = SpellServiceHandler()
processor = SpellService.Processor(handler)
transport = TSocket.TServerSocket(port=9090)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

# You could do one of these for a multithreaded server
#server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)
#server = TServer.TThreadPoolServer(processor, transport, tfactory, pfactory)

print 'Starting the server...'
server.serve()
print 'done.'
