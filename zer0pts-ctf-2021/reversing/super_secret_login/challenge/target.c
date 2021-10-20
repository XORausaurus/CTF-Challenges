#undef _UNICODE
#undef UNICODE
#include <windows.h>
#include <winternl.h>

BYTE patched[] = {0x90, 0xe8,0x87,0xd3,0x08,0x00};
// 0x8d387

int main()
{
    HANDLE hFile = CreateFile(
        "SolveMe-Temp.exe", GENERIC_READ,
        0, NULL, OPEN_EXISTING,
        FILE_ATTRIBUTE_NORMAL, NULL
    );

    DWORD ret;
    DWORD tempSize = GetFileSize(hFile, NULL);
    BYTE* buf = (BYTE*) HeapAlloc(
        GetProcessHeap(), HEAP_ZERO_MEMORY, tempSize
    );

    ReadFile(hFile, buf, tempSize, &ret, NULL);
    CloseHandle(hFile);

    DWORD offset = 0x87931;
    for (int i = 0; i < 6; i++)
    {
        buf[offset+i] = patched[i];
    }

    // patch import - point the GetWindowTextW to somewhere else
    // so that Ldr doesn't patch our call
    buf[0x117374] = 0x4c;
    buf[0x117375] = 0x3e;

    hFile = CreateFile(
        "SuperSecretLogin.exe", GENERIC_WRITE,
        0, NULL, CREATE_ALWAYS,
        FILE_ATTRIBUTE_NORMAL, NULL
    );

    WriteFile(hFile, buf, tempSize, &ret, NULL);
    CloseHandle(hFile);

    WriteFile(
        GetStdHandle(-11),
        "[+] Patched to 'SuperSecretLogin.exe'!\n",
        36, &ret, NULL
    );
}