# -*- coding: UTF-8 -*-
import dpkt
import socket
import datetime
import matplotlib.pyplot as plt

first = 0
first_ts = 0
first_seq = 0

def printPcap(pcap):
    global first
    global first_ts
    global first_seq
    
    list_thp = []
    list_ts = []

    list_thp2 = []
    list_ts2 = []
    
    prev_seq = 0
    current_sum = 0
    current_run = 0
    prev_seq2 = 0;
    current_sum2 = 0
    current_run2 = 0

    for (ts,buf) in pcap:
        eth = dpkt.ethernet.Ethernet(buf)
        if not isinstance(eth.data, dpkt.ip.IP):
            print 'Non IP Packet type not supported %s' % eth.data.__class__.__name__
            continue

        ip = eth.data
        src = socket.inet_ntoa(ip.src)
        dst = socket.inet_ntoa(ip.dst)

        tcp = ip.data



        if src == "140.113.195.91" and tcp.dport == 49726:
            if first == 0:
                first = 1
                first_ts = ts
                first_seq = tcp.seq

           
	    
            seq=ts-first_ts

            if seq >= prev_seq + 0.25 and current_run != 0:
	    	list_thp.append(((current_sum/current_run)/0.25)/10000)
		list_ts.append(seq)
		
		current_sum = 0
		current_run = 0
		prev_seq=seq
		#print '[+] Src:'+src+' -->Dst:'+dst +  '\tseq: ' + str(tcp.seq-first_seq) + '  \ttime:' + format(ts-first_ts, '.6f') + '\tsize: ' + str(len(buf))
                
            else:
	        current_sum = current_sum + len(buf)
		current_run = current_run + 1
	
	if src == "140.113.195.91" and tcp.dport == 49728:
            if first == 0:
                first = 1
                first_ts = ts
                first_seq = tcp.seq

            
            seq=ts-first_ts

            if seq >= prev_seq2 + 0.25 and current_run2 != 0: 
	    	list_thp2.append(((current_sum2/current_run2)/0.25)/10000)
		list_ts2.append(seq)
		
		current_sum2 = 0
		current_run2 = 0
		prev_seq2=seq
                #print '[+] Src:'+src+' -->Dst:'+dst +  '\tseq: ' + str(tcp.seq-first_seq) + '  \ttime:' + format(ts-first_ts, '.6f') + '\tsize: ' + str(len(buf))
            else:
	        current_sum2 = current_sum2 + len(buf)
		current_run2 = current_run2 + 1


    draw_sqn(list_ts,list_thp)
    draw_sqn(list_ts2,list_thp2)
    plt.show()
def draw_sqn(list_ts,list_sqn):
    plt.plot(list_ts,list_sqn)
    plt.xlabel("Time");
    plt.ylabel("Throughput");
    plt.title("time/datarate graph")
    #plt.show()

def main():
    f = open('lab1_0416329_rx_wget.pcap')
    pcap = dpkt.pcap.Reader(f)
    printPcap(pcap)

if __name__ == '__main__':
    main()

