import sys
from os import system

if len(sys.argv)==1:
    mode="linux"
else:
    mode = sys.argv[1]

system("cat ./src/codegen/out.asm")
system("nasm -felf32 ./src/codegen/out.asm")
ld = "ld" if mode == "linux" else "ld.gold"
qemui386="" if mode == "linux" else "qemu-i386 "

system(ld+" -m elf_i386 ./src/codegen/out.o")
print(system(qemui386+"./src/codegen/a.out")>>8)
