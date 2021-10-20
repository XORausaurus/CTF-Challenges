format pe gui 6.0
entry _start

section '.text' code readable executable writeable

; End of data we will store address of ZwCreateDebugObject
; and ZwQueryObject
; and [debug handle]

END_OF_DATA = 0xC7F74

_start:
    push    ebp
    mov     ebp, esp
    pushad
    mov     eax, dword [fs:0x30]
    mov     ebx, [eax+8]
    
    push    0xdb9cae6a
    push    0x1b708
    call    _resolve

    lea     edi, [ebx+END_OF_DATA]
    push    0
    push    4
    push    edi
    push    0x1e
    push    -1
    call    eax

    mov     eax, [edi]
    or      eax, eax
    jnz     _debugger_present

_no_debugger_present:
    push    0x34ac8e
    push    0x38f88
    call    _resolve
    push    dword [ebp+16]
    push    dword [ebp+12]
    push    dword [ebp+8]
    call    eax
    mov     esi, [ebp+12]
    mov     ecx, 1
    call    _fuck_it
    db  0, 0, 0, 95, 0, 0, 0, 0, 80, 27, 43, 68, 1, 71, 126, 40, 95, 92, 59, 126, 1, 4, 0, 86, 107, 11, 3, 6, 0, 18, 67, 71, 0, 64, 7, 68, 92, 65, 90, 83, 0, 0
_fuck_it:
    pop     edi

_fuck_loop:
    mov     al, [edi+ecx-1]
    xor     [esi+ecx*2-2], al
    add     ecx, 1
    cmp     ecx, [ebp+16]
    jnz     _fuck_loop

_fuck_all:
    popad
    leave
    retn 12

_debugger_present:
    push    dword [ebp+16]
    push    dword [ebp+12]
    push    dword [ebp+8]
    push    0x34ac8e
    push    0x38f88
    call    _resolve
    call    eax
    jmp _fuck_all

_resolve:
    push    ebp
    mov     ebp, esp
    push    ebx
    push    esi
    push    edi
    push    ecx

loc_400031:
    push    dword [fs:30h]
    pop     eax
    mov     eax, [eax+0Ch]  ; LDr
    mov     ecx, [eax+0Ch]  ; InLoadOrderModuleList

loc_40003F:                             ; CODE XREF: ResolveFn+2C↓j
    mov     edx, [ecx]
    mov     eax, [ecx+30h]  ; baseDllName
    push    2
    mov     edi, [ebp+8]
    push    edi
    push    eax
    call    CmpHash
    test    eax, eax
    jz      short loc_400058
    mov     ecx, edx
    jmp     short loc_40003F
; ---------------------------------------------------------------------------

loc_400058:                             ; CODE XREF: ResolveFn+28↑j
    mov     eax, [ecx+18h]
    push    eax             ; Dllbase
    mov     ebx, [eax+3Ch]
    add     eax, ebx
    mov     ebx, [eax+78h]
    pop     eax
    push    eax

loc_400066:                             ; ExportDir
    add     ebx, eax
    mov     ecx, [ebx+1Ch]

loc_40006B:
    mov     edx, [ebx+20h]
    mov     ebx, [ebx+24h]

loc_400071:                             ; ExportAddressTable
    add     ecx, eax

loc_400073:                             ; NamePtrTable
    add     edx, eax
    add     ebx, eax        ; OrdinalTable

loc_400077:                             ; CODE XREF: ResolveFn+68↓j
    mov     esi, [edx]
    pop     eax
    push    eax
    add     esi, eax
    push    1
    push    dword [ebp+12]
    push    esi
    call    CmpHash
    test    eax, eax
    jz      short loc_400094
    add     edx, 4
    add     ebx, 2
    jmp     short loc_400077
; ---------------------------------------------------------------------------

loc_400094:                             ; CODE XREF: ResolveFn+60↑j
    pop     eax
    xor     edx, edx
    mov     dx, [ebx]
    shl     edx, 2
    add     ecx, edx
    add     eax, [ecx]
    pop     ecx
    pop     edi
    pop     esi
    pop     ebx
    mov     esp, ebp
    pop     ebp
    retn    8

CmpHash:
    push    ebp
    mov     ebp, esp
    push    ecx
    push    ebx
    push    edx
    xor     ecx, ecx
    xor     ebx, ebx
    xor     edx, edx
    mov     eax, [ebp+8]

loc_4000BA:                             ; CODE XREF: CmpHash+1F↓j
    mov     dl, [eax]
    or      dl, 60h
    add     ebx, edx
    shl     ebx, 1
    add     eax, [ebp+16]
    mov     cl, [eax]
    test    cl, cl
    loopne  loc_4000BA
    xor     eax, eax
    mov     ecx, [ebp+12]
    cmp     ebx, ecx
    jz      short loc_4000D6
    inc     eax

loc_4000D6:                             ; CODE XREF: CmpHash+28↑j
    pop     edx
    pop     ebx
    pop     ecx
    mov     esp, ebp
    pop     ebp
    retn    0Ch

db  'AU3!EA06'