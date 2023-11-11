from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI


class LinuxRouter(Node):
    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()


class NetworkTopo(Topo):
    def build(self):
        # Adding routers to the topology with different subnets
        r1 = self.addHost('r1', cls=LinuxRouter, ip='10.0.0.1/24')
        r2 = self.addHost('r2', cls=LinuxRouter, ip='10.1.0.1/24')
        r3 = self.addHost('r3', cls=LinuxRouter, ip='10.2.0.1/24')
        # Adding switches between routers and end hosts
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        # Adding links between the switches and the routers
        self.addLink(s1,
                     r1,
                     intfName2='r1-eth1',
                     params2={'ip': '10.0.0.1/24'})

        self.addLink(s2,
                     r2,
                     intfName2='r2-eth1',
                     params2={'ip': '10.1.0.1/24'})
        self.addLink(s3,r3,intfName2='r3-eth1',params2={'ip':'10.2.0.1/24'})
        # Defining the end hosts with ip of the desired subnet of router and default route
        d1 = self.addHost(name='d1',
                          ip='10.0.0.251/24',
                          defaultRoute='via 10.0.0.1')
        d2 = self.addHost(name='d2',
                          ip='10.1.0.252/24',
                          defaultRoute='via 10.1.0.1')
        d3 = self.addHost(name='d3',
                          ip='10.2.0.252/24',
                          defaultRoute='via 10.2.0.1')
        d4 = self.addHost(name='d4',
                          ip='10.0.0.145/24',
                          defaultRoute='via 10.0.0.1')
        d5 = self.addHost(name='d5',
                          ip='10.1.0.145/24',
                          defaultRoute='via 10.1.0.1')
        d6 = self.addHost(name='d6',
                          ip='10.2.0.145/24',
                          defaultRoute='via 10.2.0.1')
        
        self.addLink(s1,d1)
        self.addLink(s2,d2)
        self.addLink(s3,d3)
        self.addLink(s1,d4)
        self.addLink(s2,d5)
        self.addLink(s3,d6)
        # Defining connections between the routers
        self.addLink(r1,
                     r2,
                     intfName1='r1-eth2',
                     intfName2='r2-eth2',
                     params1={'ip': '10.100.0.1/24'},
                     params2={'ip': '10.100.0.2/24'})
        self.addLink(r2,r3,
                     intfName1='r2-eth3',
                     intfName2='r3-eth2',
                     params1={'ip': '10.100.1.1/24'},
                     params2={'ip': '10.100.1.2/24'})
        self.addLink(r1,
                     r3,
                     intfName1='r1-eth3',
                     intfName2='r3-eth3',
                     params1={'ip': '10.100.2.1/24'},
                     params2={'ip': '10.100.2.2/24'})


def run():
    topo = NetworkTopo()
    net = Mininet(topo=topo)

    # Add entries in the routing table of the routers
    info(net['r1'].cmd("ip route add 10.1.0.0/24 via 10.100.0.2 dev r1-eth2"))
    info(net['r1'].cmd("ip route add 10.2.0.0/24 via 10.100.2.2 dev r1-eth3"))
    info(net['r2'].cmd("ip route add 10.0.0.0/24 via 10.100.0.1 dev r2-eth2"))
    info(net['r2'].cmd("ip route add 10.2.0.0/24 via 10.100.1.2 dev r2-eth3"))
    info(net['r3'].cmd("ip route add 10.1.0.0/24 via 10.100.1.1 dev r3-eth2"))
    info(net['r3'].cmd("ip route add 10.0.0.0/24 via 10.100.2.1 dev r3-eth3"))   
    net.start()
    net.pingAll()
    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    run()