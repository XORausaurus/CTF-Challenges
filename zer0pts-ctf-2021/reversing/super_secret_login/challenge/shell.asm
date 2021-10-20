format pe gui 6.0
entry _start

section '.text' code readable executable writeable

; [ebp+8] - dest
; [ebp+12] - src
; [ebp+16] - size
; [ebp+20] - key

pDest = 8
pSrc = 12
pSize = 16
pKey = 20
KEY_LEN = 43

_start:
  push ebp
  mov ebp, esp
  pushad
  xor eax, eax
  sub esp, 256

rc4_sbox_setup:
  mov BYTE [esp+eax], al
  inc eax
  cmp eax, 256
  jne rc4_sbox_setup

  xor esi, esi
  xor ebx, ebx

rc4_key_setup:
  movzx eax, BYTE [esp+esi]
  add ebx, eax  ; j += S[i]
  mov eax, esi
  mov ecx, KEY_LEN
  xor edx, edx
  div ecx
  mov eax, [ebp+pKey]
  movsx ecx, BYTE [eax+edx]
  add ebx, ecx  ; j += key[i%43]
  ; swap S[i], S[j]
  movzx ebx, bl
  mov cl, [esp+esi]
  mov al, [esp+ebx]
  mov [esp+esi], al
  mov [esp+ebx], cl
  add esi, 1
  cmp esi, 256
  jne rc4_key_setup

  xor esi, esi
  xor edx, edx
  xor ecx, ecx
  
rc4_crypt:
  inc edx
  inc esi
  movzx edx, dl
  mov al, BYTE [esp+edx]
  add ecx, eax  ; j += S[i]
  movzx ecx, cl ; j %= 256
  mov bl, BYTE [esp+ecx]
  mov BYTE [esp+ecx], al
  mov BYTE [esp+edx], bl
  add al, bl
  movzx eax, al
  mov edi, [ebp+pSrc]
  mov bl, BYTE [edi+esi-1]
  mov al, BYTE [esp+eax]  ; S[S[i]+S[j]]
  xor ebx, eax
  mov edi, [ebp+pDest]
  call write_byte
  cmp esi, [ebp+pSize]
  jne rc4_crypt
  add esp, 256
  popad
  leave
  retn 16

write_byte:
  ; addr = edi+esi-1
  ; byte = bl
  push eax
  push ebx
  jmp short next
back:
  pop eax
  shr ebx, 4
  mov bl, [eax+ebx]
  mov [edi+esi*2-2], bl
  pop ebx
  and ebx, 0xf
  mov bl, [eax+ebx]
  mov [edi+esi*2-1], bl
  pop eax
  ret

next:
  call back
hexStr db "0123456789abcdef"