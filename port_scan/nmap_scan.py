import nmap


def main():
    ip_list = [line.rstrip() for line in open("ip_list.txt")]
    for ip in ip_list:
        nm_scan(ip)


def nm_scan(ip):
    nm = nmap.PortScanner()
    nm.scan(ip, '0-65535')
    for host in nm.all_hosts():
        print('----------------------------------------------------')
        print('Host : %s (%s)' % (host, nm[host].hostname()), 'State : %s' % nm[host].state())
        for proto in nm[host].all_protocols():
            lport = sorted(nm[host][proto].keys())
            for port in lport:
                print('port : %s\tservice : %s' % (port, nm[host][proto][port]['product']))
if __name__ == '__main__':
    main()
