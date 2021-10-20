#undef _UNICODE
#undef UNICODE
#include <windows.h>

// update resource

int main() {

    HMODULE hMod = LoadLibraryEx("SolveMe.exe", NULL, LOAD_LIBRARY_AS_IMAGE_RESOURCE);
    HRSRC hRsrc = FindResource(hMod, "SCRIPT", RT_RCDATA);
    LPVOID pData = LoadResource(hMod, hRsrc);
    DWORD dwSize = SizeofResource(hMod, hRsrc);
    DWORD dwRet;
    HANDLE hFile = CreateFile(
        "script.bin", GENERIC_WRITE, FILE_SHARE_WRITE,
        NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL
    );
    WriteFile(hFile, pData, dwSize, &dwRet, NULL);
    CloseHandle(hFile);

    hFile = CreateFile(
        "shellcode.bin", GENERIC_READ, FILE_SHARE_READ,
        NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL
    );

    DWORD size = GetFileSize(hFile, NULL);
    BYTE* buf = HeapAlloc(GetProcessHeap(), HEAP_ZERO_MEMORY, size);
    ReadFile(hFile, buf, size, &dwRet, NULL);
    while (!buf[--dwRet]);
    dwRet += 3;

    BYTE* buffer = HeapAlloc(GetProcessHeap(), HEAP_ZERO_MEMORY, dwRet+dwSize);
    memcpy(buffer, pData, dwSize);
    memcpy(buffer+dwSize, buf, dwRet);

    CopyFile("SolveMe.exe", "SolveMe-Temp.exe", FALSE);
    HANDLE hUpdate = BeginUpdateResource("SolveMe-Temp.exe", FALSE);
    BOOL ans = UpdateResource(
        hUpdate, RT_RCDATA, "SCRIPT",
        MAKELANGID(LANG_NEUTRAL, SUBLANG_NEUTRAL),
        buffer, dwRet+dwSize
    );
    if (!ans)
    {
        WriteFile(GetStdHandle(-11), "Failed to Update!\n", 18, &dwRet, NULL);
        return 1;
    }
    EndUpdateResource(hUpdate, FALSE);
    WriteFile(GetStdHandle(-11), "[+] Updated Resources!\n", 23, &dwRet, NULL);
}