from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import TCLink
import matplotlib.pyplot as plt
import re,time,argparse
class NetworkTopo(Topo):
    def build(self, **_opts):
        # Adding 2 switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        # Adding hosts
        d1 = self.addHost('d1')
        d2 = self.addHost('d2')
        d3 = self.addHost('d3')
        d4 = self.addHost('d4')
        # Adding links
        self.addLink(s1,d1)
        self.addLink(s1,d2)
        self.addLink(s2,d3)
        self.addLink(s2,d4)
        # print(self.loss)
        self.addLink(s1,s2,**_opts)

def set_server_client(net, congestion_algo,ax=None):
    host=net.get('d4')
    client=net.get('d1')
    print(host.IP())
    remote_ip=f'{host.IP()}'
    test_time=10
    host.cmd(f'iperf -s -Z {congestion_algo} > logs1.txt &')
    host.cmd(f'sudo tcpdump -w host.pcap &')
    client.cmd(f'sudo tcpdump -w client1.pcap &')
    client.cmd(f'iperf -c {remote_ip} -t 10 -i 1 -Z {congestion_algo}> logs2.txt')
    
    host.cmd('killall iperf')
    process_logs(congestion_algo,ax=ax)
def process_logs(congestion_algo,file_name="logs2.txt",ax=None):
    # This function is used to plot the bandwidth curve after reading the iperf logs,
    #  not to be used in this assignment.
    print("processing")
    b_array=[]
    with open(file_name,"r") as f:
        lines=f.readlines()
    pattern=re.compile(r'(\d+(\.\d*)?)\s+([A-Za-z]+/sec)')
    for line in lines:
        match=pattern.search(line)

        if match:
            bandwidth_str,_,unit=match.groups()
            bandwidth=float(bandwidth_str.split()[0])
            if(unit=='Gbits/sec'):
                bandwidth*=1
            if(unit=='Mbits/sec'):
                bandwidth*=1e-3
            if(unit=='Kbits/sec'):
                bandwidth*=1e-6
            b_array.append(bandwidth)
    # print(b_array) 
    if(ax!=None):
        ax.plot(b_array[:-1],marker='o',linestyle='-',label=congestion_algo)

def set_server_multiclient(net,congestion_algo,ax=None):
    host=net.get('d4')
    client1=net.get('d1')
    client2=net.get('d2')
    client3=net.get('d3')
    # print(host.IP())
    remote_ip=f'{host.IP()}'
    test_time=10
    host.cmd(f'iperf -s -Z {congestion_algo} > logs1.txt &')
    host.cmd(f'sudo tcpdump -w host{congestion_algo}.pcap &')
    client1.cmd(f'sudo tcpdump -w client1{congestion_algo}.pcap &')
    client2.cmd(f'sudo tcpdump -w client2{congestion_algo}.pcap &')
    client3.cmd(f'sudo tcpdump -w client3{congestion_algo}.pcap &')
    client1.cmd(f'iperf -c {remote_ip} -t {test_time} -i 1 -Z {congestion_algo} > logs2.txt &')
    client2.cmd(f'iperf -c {remote_ip} -t {test_time} -i 1 -Z {congestion_algo} > logs3.txt &')
    client3.cmd(f'iperf -c {remote_ip} -t {test_time} -i 1 -Z {congestion_algo} > logs4.txt &')
    time.sleep(test_time+5)
    if(ax!=None):
        for i in range(len(ax)):
            process_logs(congestion_algo,file_name=f"logs{2+i}.txt",ax=ax[i])

    host.cmd('killall iperf')

def run(config,congestion,loss,plot_all=False):
    # plotall is used to plot the bandwidth curve not to be used for this assignment.
    topo = NetworkTopo(loss=loss)
    net = Mininet(topo=topo,link=TCLink)
    congestion_al=congestion
    net.start()
    if(config=='b'):
        if(plot_all):
            fig,ax=plt.subplots()
            algos=['reno','bbr','vegas','cubic']
            print("processing")
            for algo in algos:
                set_server_client(net,algo,ax)
                time.sleep(2)
            ax.set_xlabel("Seconds passed")
            ax.set_ylabel("Bandwidth (GBits/sec)")
            ax.set_title("Bandwidth Values")
            ax.legend()
            fig.savefig('client1_bandwidth')
        else:
            print("processing")
            fig,ax=plt.subplots()
            set_server_client(net,congestion_al,ax)
            time.sleep(2)
            ax.set_xlabel("Seconds passed")
            ax.set_ylabel("Bandwidth (GBits/sec)")
            ax.set_title("Bandwidth Values")
            ax.legend()
            fig.savefig('client1_bandwidth')

    if(config=='c'):
        if(plot_all):
            fig1,ax1=plt.subplots()
            fig2,ax2=plt.subplots()
            fig3,ax3=plt.subplots()
            ax1.grid(True)
            ax2.grid(True)
            ax3.grid(True)
            plots=[ax1,ax2,ax3]
            algos=['reno','bbr','vegas','cubic']
            print("processing")
            for algo in algos:
                set_server_multiclient(net,algo,ax=plots)
                time.sleep(2)
            for plot in plots:
                plot.set_xlabel("Seconds passed")
                plot.set_ylabel("Bandwidth (GBits/sec)")
                plot.set_title("Bandwidth Values")
                plot.legend()
            fig1.savefig('Client 1')
            fig2.savefig('Client 2')
            fig3.savefig('Clinet 3')
        else:
            fig1,ax1=plt.subplots()
            fig2,ax2=plt.subplots()
            fig3,ax3=plt.subplots()
            ax1.grid(True)
            ax2.grid(True)
            ax3.grid(True)
            plots=[ax1,ax2,ax3]
            print("processing")
            set_server_multiclient(net,congestion_al,ax=plots)
            time.sleep(2)
            for plot in plots:
                plot.set_xlabel("Seconds passed")
                plot.set_ylabel("Bandwidth (GBits/sec)")
                plot.set_title("Bandwidth Values")
                plot.legend()
            fig1.savefig('Client 1')
            fig2.savefig('Client 2')
            fig3.savefig('Client 3')
    print("processed")
    # CLI(net)
    net.stop()


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--config',type=str)
    parser.add_argument('--congestion',type=str)
    parser.add_argument('--loss',type=int)
    # parser.add_argument('--plotall',type=bool)
    args=parser.parse_args()
    print(args.config,args.congestion,args.loss)
    setLogLevel('info')
    
    run(args.config,args.congestion,args.loss)