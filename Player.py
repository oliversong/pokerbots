import socket
import sys

"""
Simple example pokerbot, written in python. This is an example of a bare bones,
dumb pokerbot - it only sets up the socket necessary to connect with the engine
and then always returns the same action. It is meant as an example of how a
pokerbot should communicate with the engine.
"""

if __name__ == "__main__":
    # port number specified by the engine to connect to.
    port = int(sys.argv[1])
    # connect the socket to the engine
    s = socket.create_connection(('localhost', int(sys.argv[1])))
    # Get a file-object for reading packets from the socket.
    # Using this ensures that you get exactly one packet per read.
    f_in = s.makefile()
    while 1:
        # block until the engine sends us a packet
        data = f_in.readline()
        # if we receive a null return, then the connection is dead
        if not data:
            print "Gameover, engine disconnected"
            break
        # Here is where you should implement code to parse the packets from
        # the engine and act on it.
        print data
        # When appropriate, reply to the engine with a legal action.
        # The engine will ignore all spurious packets you send.
        # The engine will also check/fold for you if you return an
        # illegal action.
        # When sending responses, you need to have a newline character (\n) or
        # carriage return (\r), or else your bot will hang!
        s.send("CHECK\n")
    # if we get here, the server disconnected us, so clean up the socket
    s.close()
