#include <openssl/aes.h>
#include <openssl/evp.h>
#include <openssl/md5.h>
#include <string>
#include <stdlib.h>
#include <string.h>
#include <unordered_map>

void md5(const char *src, int srclen, unsigned char* dest) {
    memset(dest, 0, MD5_DIGEST_LENGTH);

    MD5_CTX md5ctx;
    MD5_Init(&md5ctx);
    MD5_Update(&md5ctx, src, srclen);
    MD5_Final((unsigned char*)dest, &md5ctx);
}

void encrypt(const char* key, const char *data, int datalen, unsigned char* dest) {
    EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();
    memset(dest, 0, datalen);
    int x;

    EVP_CIPHER_CTX_init(ctx);
    EVP_EncryptInit_ex(ctx, EVP_aes_128_ecb(), NULL, (const unsigned char*)key, NULL);
    EVP_EncryptUpdate(ctx, dest, &x, (const unsigned char*)data, datalen);
    EVP_CIPHER_CTX_free(ctx);
}

char fromHexChar(char c) {
    if ('0' <= c && c <= '9') {
        return c - '0';
    }
    if ('a' <= c && c <= 'f') {
        return c - 'a' + 10;
    }
    if ('A' <= c && c <= 'F') {
        return c - 'A' + 10;
    }
    exit(EXIT_FAILURE);
}

char toHexChar(unsigned char c) {
    const static char table[] = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f'};
    return table[c];
}

std::string fromhex(const char* source) {
    std::string s;
    while(*source) {
        char v = fromHexChar(*source) << 4;
        source++;
        v = v | fromHexChar(*source);
        source++;

        s.push_back(v);
    }
    return s;
}

std::string tohex(const char *src, int len) {
    const unsigned char *source = (const unsigned char*) src;
    std::string s;
    for (int i = 0; i < len; i++) {
        s.push_back(toHexChar((*source) >> 4));
        s.push_back(toHexChar((*source) & 0xf));
        source++;
    }
    return s;
}

std::string x(std::string a, std::string b) {
    std::string c;
    for (int i = 0; i < a.size(); i++) {
        c.push_back( a[i] ^ b[i] );
    }
    return c;
}


int main(int argc, char **argv) {
    std::string a = fromhex(argv[1]);
    std::string b = fromhex(argv[2]);
    std::string iv2 = fromhex(argv[3]);
    std::string iv3 = fromhex(argv[4]);

    std::unordered_map<std::string, std::string> map;
    auto left = x(iv2, iv3);

    unsigned char* m1 = (unsigned char*)malloc(sizeof(unsigned char) * a.size()) ;
    unsigned char* m2 = (unsigned char*)malloc(sizeof(unsigned char) * a.size()) ;

    unsigned char *key = (unsigned char*)malloc(sizeof(unsigned char) * MD5_DIGEST_LENGTH);
    unsigned char k[16];
    int N = 3;
    memset(&k, 0, 16);
    for (;;) {
        md5((const char*)&k, N, key);
        encrypt((const char*)key, iv3.c_str(), iv3.size(), m1);
        auto t = x(left, std::string((char*) m1));
        map[t] = tohex((const char*)key, 16);

        int i = 0;
        while (i < N && k[i] == 255) {
            k[i] = 0;
            i++;
        }
        if (i == N) {
            break;
        }
        k[i]++;
    }

    memset(&k, 0, 16);
    std::string k1, k3;
    for (;;) {
        md5((const char*)&k, N, key);
        encrypt((const char*)key, a.c_str(), a.size(), m1);
        encrypt((const char*)key, b.c_str(), b.size(), m2);
        auto t = x(std::string((char*) m2), std::string((char*) m1));

        if (map.find(t) != map.end()) {
            printf("%s\n", tohex((const char*)key, 16).c_str());
            printf("%s\n", map.at(t).c_str());

            k1 = std::string((char*)key);
            k3 = fromhex(map.at(t).c_str());

            break;
        }

        int i = 0;
        while (i < N && k[i] == 255) {
            k[i] = 0;
            i++;
        }
        if (i == N) {
            return 1;
        }
        k[i]++;
    }

    encrypt(k1.c_str(), a.c_str(), a.size(), m1);
    std::string target = x(std::string((char*)m1), iv2);
    encrypt(k3.c_str(), iv3.c_str(), iv3.size(), m1);
    std::string cmp_to = x(std::string((char*)m1), iv3);
    memset(&k, 0, 16);

    for (;;) {
        md5((const char*)&k, N, key);
        encrypt((const char*)key, target.c_str(), target.size(), m1);
        std::string result((char*) m1);
        if (result == cmp_to) {
            printf("%s\n", tohex((const char*)key, 16).c_str());
            break;
        }

        int i = 0;
        while (i < N && k[i] == 255) {
            k[i] = 0;
            i++;
        }
        if (i == N) {
            return 1;
        }
        k[i]++;
    }

    return 0;
}
