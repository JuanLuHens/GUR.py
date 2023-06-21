from ldap3 import Server, Connection, AUTO_BIND_NO_TLS, SUBTREE
import ipaddress
from concurrent.futures import ThreadPoolExecutor
import time
from dns import resolver
import argparse
import os

def get_args():
    parser = argparse.ArgumentParser(
        description = 'The "Get Unique Ranges" (GUR.py) application is a tool designed to retrieve the unique ranges of networks where workstations and servers of a domain are located\nBy @z3r082')
    parser.add_argument('-u', '--user', dest='user', type=str, required=True,help='Domain user without the domain.')
    parser.add_argument('-p', '--password', dest='password', type=str, required=True,help='Domain user\'s password.')
    parser.add_argument('-d', '--domain', dest='domain', type=str, required=True,help='Domain. Example "contoso.com".')
    parser.add_argument('-dc', dest='dc', type=str, required=True,help='Domain Controller IP.')
    parser.add_argument('-ns', dest='ns', type=str, required=True,help='DNS-Nameserver IP.')
    parser.add_argument('-t', dest='hilos',action="store_true", required=False, default=10, help="Threads. Default 10")
    parser.add_argument('-v', dest='verbose',action="store_true", required=False, help="verbose")
    return parser.parse_args()


def obtener_rango(ip):
    rango = str(ipaddress.ip_network(ip + '/24', strict=False))
    return rango

def obtener_conn(servidor,user,password,domain):
    username=f'{user}@{domain}'
    server = Server(servidor, port=389, get_info=SUBTREE)
    conn = Connection(server, user=username, password=password, auto_bind=AUTO_BIND_NO_TLS)
    return conn

def obtener_equipos(conn,domain):
    dc0 = domain.split('.')[0]
    dc1 = domain.split('.')[1]
    base = f'dc={dc0},dc={dc1}'
    conn.search(
    search_base=base,
    search_filter='(objectClass=computer)',
    attributes=['cn','dNSHostName']
    )
    for entry in conn.entries:
        try:
            print("Nombre: {}".format(entry.cn))
            if domain in entry.dNSHostName.value:
                with open('hosts.txt', 'a') as f:
                    f.write(f'{entry.dNSHostName}\n')
            else:
                with open('hosts.txt', 'a') as f:
                    f.write(f'{entry.cn}.{domain}\n')
        except:
            with open('hosts.txt', 'a') as f:
                    f.write(f'{entry.cn}.{domain}\n')
        print("===========================================")
    conn.unbind()
    return True

def resolve_host(host,ns):
    try:
        resolver.default_resolver = resolver.Resolver(configure=False)
        resolver.default_resolver.nameservers = [ns]
        response = resolver.query(host)
        ip_address = response[0].address
        rango = obtener_rango(ip_address)
        print(f'{host}: {ip_address} :{rango}\n')
        with open("rangos.txt", "a") as file:
            file.write(f"{rango}\n")
    except Exception as e:
        print(f'No se pudo resolver la dirección IP para {host}: {str(e)}')

if __name__ == '__main__':
    args = get_args()
    conn = obtener_conn(args.dc,args.user,args.password,args.domain)
    if(obtener_equipos(conn,args.domain)):
        with open("hosts.txt") as file:
            hosts = file.read().splitlines()
        with ThreadPoolExecutor(max_workers=args.hilos) as executor:
            futures = []
            for host in hosts:
                futures.append(executor.submit(resolve_host, host,args.ns))
                
            for future in futures:
                future.result()
            while executor._work_queue.qsize() >= executor._max_workers:
                print("Esperando a que finalicen algunos hilos...")
                time.sleep(1)
        with open('rangos.txt', 'r') as f:
            rangos = f.readlines()
        rangos = list(set(rangos))
        rangos.sort()
        with open('rangosunicos.txt', 'w') as f:
            f.writelines(rangos)
        os.system('clear')
        os.remove('hosts.txt')
        os.remove('rangos.txt')
        print('\033[94m'+'Rangos unicos:')
        for x in rangos:
            print(x)
        print("Esta informacion queda almacenada en el fichero rangosunicos.txt")