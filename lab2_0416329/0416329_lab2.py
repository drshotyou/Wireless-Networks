#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.node import RemoteController
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI

class MyTopo( Topo ):
    "Single switch connected to n hosts."
    def build( self ):
        s1 = self.addSwitch( 's1' )
        s2 = self.addSwitch( 's2' )
        s3 = self.addSwitch( 's3' )
        s4 = self.addSwitch( 's4' )

        h1 = self.addHost( 'h1' )
        h2 = self.addHost( 'h2' )

        self.addLink( h1, s1, bw=10, delay='5ms', loss=0,
                            max_queue_size=1000, use_htb=True )
        self.addLink( s1, s2, bw=1, delay='5ms', loss=50,
                            max_queue_size=1000, use_htb=True )  
        self.addLink( s1, s3, bw=2, delay='5ms', loss=10,
                            max_queue_size=1000, use_htb=True )
        self.addLink( s2, s4, bw=1, delay='5ms', loss=0,
                            max_queue_size=1000, use_htb=True )
        self.addLink( s3, s4, bw=2, delay='5ms', loss=0,
                            max_queue_size=1000, use_htb=True )                                          
        self.addLink( s4, h2, bw=10, delay='5ms', loss=0,
                            max_queue_size=1000, use_htb=True )

def perfTest():
    "Create network and run simple performance test"
    topo = MyTopo()
    net = Mininet(topo = topo, link = TCLink, controller = None)
    net.addController('c0', controller = RemoteController, ip = '127.0.0.1', port = 6633)

    net.start()
    
    print "*** Dumping host connections"
    dumpNodeConnections(net.hosts)
    
    h1 = net.get('h1')
    h2 = net.get('h2')
    h1.setMAC("0:0:0:0:0:1")
    h2.setMAC("0:0:0:0:0:2")

    
    print "*** Testing bandwidth between h1 and h2"
    h2.cmd('iperf -s -u -i 5 > results &')
    print h1.cmd('iperf -c 10.0.0.2 -u -b 10m -t 40 -i 5')

    h2.cmd('kill %iperf')
    
    print "*** Output the iperf results"
    file = open('results')
    line_num = 1
    for line in file.readlines():
        print "%d: %s" %(line_num, line.strip())
        line_num += 1

    #CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    perfTest()