#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>
#include "obfuscator.h"

#define C0 0x6A09E667F3BCC908
#define C1 0xBB67AE8584CAA73B
#define C2 0x3C6EF372FE94F82B

const uint8_t SBOX[] = {
  0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5,
  0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
  0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0,
  0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
  0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc,
  0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
  0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a,
  0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
  0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0,
  0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
  0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b,
  0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
  0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85,
  0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
  0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5,
  0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
  0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17,
  0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
  0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88,
  0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
  0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c,
  0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
  0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9,
  0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
  0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6,
  0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
  0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e,
  0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
  0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94,
  0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
  0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68,
  0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
};

int main()
{
  int i, j, k;
  uint64_t t;

  /**
   * rotl16, rotr16
   */
  DEF_ARG(rotl, uint64_t, x);
  DEF_ARG(rotl, uint8_t, n);
  DEF_FUNC(rotl, {
      RET((ARG(rotl, x) << ARG(rotl, n)) | (ARG(rotl, x) >> (64-ARG(rotl, n))));
    });
  DEF_ARG(rotr, uint64_t, x);
  DEF_ARG(rotr, uint8_t, n);
  DEF_FUNC(rotr, {
      RET((ARG(rotr, x) >> ARG(rotr, n)) | (ARG(rotr, x) << (64-ARG(rotr, n))));
    });

  /**
   * mul2
   */
  DEF_ARG(mul2, uint8_t, x);
  DEF_FUNC(mul2, {
      RET((ARG(mul2, x) << 1) ^ (((ARG(mul2, x) >> 7) & 1) ? 0x11b : 0));
    });

  /**
   * M
   */
  uint8_t m[4];
  uint8_t y[4];
  DEF_ARG(M, uint8_t*, x);
  DEF_FUNC(M, {
      for (i = 0; i < 4; i++) {
        ARG(mul2, x) = ARG(M, x)[i];
        m[i] = (uint8_t)CALL(mul2);
      }
      y[0] = ARG(M, x)[0] ^ ARG(M, x)[1] ^ ARG(M, x)[2] ^ m[0] ^ m[3];
      y[1] = ARG(M, x)[0] ^ ARG(M, x)[1] ^ ARG(M, x)[3] ^ m[2] ^ m[3];
      y[2] = ARG(M, x)[0] ^ ARG(M, x)[2] ^ ARG(M, x)[3] ^ m[1] ^ m[2];
      y[3] = ARG(M, x)[1] ^ ARG(M, x)[2] ^ ARG(M, x)[3] ^ m[0] ^ m[1];
      for (i = 0; i < 4; i++)
        ARG(M, x)[i] = y[i];
      RET(NULL);
    });

  /**
   * F
   */
  uint8_t p[8];
  uint64_t x;
  uint64_t r;
  DEF_ARG(F, uint64_t, buf);
  DEF_ARG(F, uint64_t, val);
  DEF_FUNC(F, {
      x = ARG(F, buf) ^ ARG(F, val);

      p[0] = SBOX[(x >> 56) & 0xff];
      p[1] = SBOX[(x >> 48) & 0xff];
      p[2] = SBOX[(x >> 40) & 0xff];
      p[3] = SBOX[(x >> 32) & 0xff];
      p[4] = SBOX[(x >> 24) & 0xff];
      p[5] = SBOX[(x >> 16) & 0xff];
      p[6] = SBOX[(x >> 8 ) & 0xff];
      p[7] = SBOX[(x >> 0 ) & 0xff];

      ARG(M, x) = &p[0];
      CALL(M);
      ARG(M, x) = &p[4];
      CALL(M);
      r = 0;
      r |= (uint64_t)p[0] << 8*4;
      r |= (uint64_t)p[1] << 8*5;
      r |= (uint64_t)p[2] << 8*2;
      r |= (uint64_t)p[3] << 8*3;
      r |= (uint64_t)p[4] << 8*0;
      r |= (uint64_t)p[5] << 8*1;
      r |= (uint64_t)p[6] << 8*6;
      r |= (uint64_t)p[7] << 8*7;
      RET(r);
    });

  /**
   * rho
   */
  uint64_t a0, br;
  DEF_ARG(rho, uint64_t*, a);
  DEF_ARG(rho, uint64_t*, b);
  DEF_FUNC(rho, {
      a0 = ARG(rho, a)[0];
      ARG(rotl, x) = ARG(rho, b) ? ARG(rho, b)[10] : 0;
      ARG(rotl, n) = 17;
      br = (uint64_t)CALL(rotl);
      ARG(rho, a)[0] = ARG(rho, a)[1];
      t = ARG(rho, a)[2]; // gcc bug! need this!
      ARG(F, buf) = ARG(rho, a)[1];
      ARG(F, val) = ARG(rho, b) ? ARG(rho, b)[4]: 0;
      ARG(rho, a)[1] = t ^ (uint64_t)CALL(F) ^ C1;
      ARG(F, val) = br;
      ARG(rho, a)[2] = a0 ^ (uint64_t)CALL(F) ^ C2;
      RET(NULL);
    });

  /**
   * lambda
   */
  DEF_ARG(lambda, uint64_t*, a);
  DEF_ARG(lambda, uint64_t*, b);
  DEF_FUNC(lambda, {
      t = ARG(lambda, b)[15];
      for (i = 15; i > 0; i--) {
        ARG(lambda, b)[i] = ARG(lambda, b)[i-1];
      }
      ARG(lambda, b)[0] = t ^ ARG(lambda, a)[0];
      ARG(lambda, b)[4] ^= ARG(lambda, b)[8];
      ARG(rotr, x) = ARG(lambda, b)[14]; ARG(rotr, n) = 32;
      ARG(lambda, b)[10] ^= (uint64_t)CALL(rotr);
      RET(NULL);
    });

  /**
   * update
   */
  uint64_t na[3];
  DEF_ARG(update, uint64_t*, a);
  DEF_ARG(update, uint64_t*, b);
  DEF_FUNC(update, {
      for (i = 0; i < 3; i++)
        na[i] = ARG(update, a)[i];
      ARG(rho, a) = ARG(update, a); ARG(rho, b) = ARG(update, b);
      CALL(rho);
      ARG(lambda, a) = na; ARG(lambda, b) = ARG(update, b);
      CALL(lambda);
      RET(NULL);
    });

  /**
   * Read input
   */
  DEF_ARG(readflag, char*, buf);
  DEF_FUNC(readflag, {
      printf("Text: ");
      RET(scanf("%127s", ARG(readflag, buf)));
    });

  /**
   * Encode flag
   */
  char *iv;
  char *key;
  uint64_t a[3];
  uint64_t b[16];
  DEF_ARG(encoder, char*, flag);
  DEF_ARG(encoder, uint64_t*, result);
  DEF_FUNC(encoder, {
      /* Initialize MUGI */
      memset(b, 0, sizeof(b));

      iv = &ARG(encoder, flag)[0];
      key = "\xf3\x28\x11\x0b\xde\x7a\xc4\x95\x5d\xef\x30\x37\x4f\x7e\xc2\xbb";

      a[0] = *(uint64_t*)(&key[0]);
      a[1] = *(uint64_t*)(&key[8]);
      ARG(rotl, x) = *(uint64_t*)(&key[0]); ARG(rotl, n) = 7;
      a[2]  = (uint64_t)CALL(rotl) ^ C0;
      ARG(rotr, x) = *(uint64_t*)(&key[8]); ARG(rotr, n) = 7;
      a[2] ^= (uint64_t)CALL(rotr);

      for (j = 0; j < 16; j++) {
        ARG(rho, a) = a; ARG(rho, b) = NULL;
        CALL(rho);
        b[15-j] = a[0];
      }
      memcpy(ARG(encoder, result), a, sizeof(a));

      a[0] ^= *(uint64_t*)(&iv[0]);
      a[1] ^= *(uint64_t*)(&iv[8]);
      ARG(rotl, x) = *(uint64_t*)(&iv[0]); ARG(rotl, n) = 7;
      a[2] ^= (uint64_t)CALL(rotl) ^ C0;
      ARG(rotr, x) = *(uint64_t*)(&iv[8]); ARG(rotr, n) = 7;
      t = (uint64_t)CALL(rotr);
      a[2] ^= t;
      memcpy(&ARG(encoder, result)[3], a, sizeof(a));

      for (j = 0; j < 16; j++) {
        ARG(rho, a) = a; ARG(rho, b) = NULL;
        CALL(rho);
      }

      for (j = 0; j < 16; j++) {
        ARG(update, a) = a;
        ARG(update, b) = b;
        CALL(update);
      }

      for (j = 0; j < strlen(ARG(encoder, flag)); j++) {
        ARG(encoder, result)[6+j] = ARG(encoder, flag)[j] ^ a[2];
        CALL(update);
      }
      RET(NULL);
    });

  /**
   * Entry Point 
   */
  char *flag = (char*)malloc(128 * sizeof(char*));
  uint64_t *result = (uint64_t*)calloc(134, sizeof(uint64_t));
  ARG(readflag, buf) = flag;
  if ((int)CALL(readflag) != 1) {
    puts("I/O Error");
    return 1;
  }
  ARG(encoder, flag) = flag;
  ARG(encoder, result) = result;
  CALL(encoder);

  for (i = 0; i < strlen(flag)+6; i++)
    printf("%016lx\n", result[i]);
}
