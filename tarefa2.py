#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel

class CustomTopo(Topo):
    "Topologia personalizada com 4 switches e 11 hosts."
    def build(self):
        # Criando os switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')

        # Criando os hosts
        hosts = []
        for i in range(1, 12):
            host = self.addHost(f'h{i}', cpu=0.05)
            hosts.append(host)

        # Ligando hosts aos switches
        # s1 -> h1, h2, h3
        self.addLink(hosts[0], s1)
        self.addLink(hosts[1], s1)
        self.addLink(hosts[2], s1)

        # s2 -> h4, h5, h6
        self.addLink(hosts[3], s2)
        self.addLink(hosts[4], s2)
        self.addLink(hosts[5], s2)

        # s3 -> h7, h8
        self.addLink(hosts[6], s3)
        self.addLink(hosts[7], s3)

        # s4 -> h9, h10, h11
        self.addLink(hosts[8], s4)
        self.addLink(hosts[9], s4)
        self.addLink(hosts[10], s4)

        # Ligando switches entre si
        self.addLink(s1, s2)
        self.addLink(s2, s3)
        self.addLink(s3, s4)
        self.addLink(s1, s4)  # criando redundância

def perfTest(net):
    "Testa a largura de banda entre h1 e todos os outros hosts."
    h1 = net.get('h1')
    hosts = [h for h in net.hosts if h.name != 'h1']
    for h in hosts:
        print(f'Testando largura de banda entre h1 e {h.name}')
        net.iperf((h1, h))

if __name__ == '__main__':
    setLogLevel('info')  # Ativa log de info
    topo = CustomTopo()
    net = Mininet(
        topo=topo,
        host=CPULimitedHost,
        link=TCLink
    )
    net.start()
    print("Conexões dos hosts:")
    dumpNodeConnections(net.hosts)
    print("Testando conectividade da rede:")
    net.pingAll()
    perfTest(net)
    net.stop()
