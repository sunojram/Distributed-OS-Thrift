import sys, glob
sys.path.append('../gen-py')

from SpellService import SpellService
from SpellService.ttypes import *

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

# parsing arguments 
host=sys.argv[1]
port=sys.argv[2]
words=[]
words=sys.argv[3:]

spell_request=SpellRequest()
spell_request.to_check=words

try:

  # Make socket
  transport = TSocket.TSocket(host,port)

  # Buffering is critical. Raw sockets are very slow
  transport = TTransport.TBufferedTransport(transport)

  # Wrap in a protocol
  protocol = TBinaryProtocol.TBinaryProtocol(transport)

  # Create a client to use the protocol encoder
  client = SpellService.Client(protocol)

  # Connect!
  transport.open()
  spell_response=client.spellcheck(spell_request)
  #print spell_response

  if hasattr(spell_response,'is_correct'):
      output=[]

   # converting bool to int
      for i in spell_response.is_correct:
          output.append(str(int(i)))

      print " ".join(output)

  # Close!
  transport.close()

except Thrift.TException, tx:
  print '%s' % (tx.message)
