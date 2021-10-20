#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdint.h>
#include <sys/mman.h>

/***** vvvvv ***** OBFUSCATOR ****** vvvvv ******/
typedef struct {
  void *f_begin, *f_end;
  size_t key;
} scope_t;
#define MAX_SCOPE 0x100
#define MARK_BOF 0x0df0adab
#define MARK_EOF 0xabadf00d
#define BEGIN_PROTECT(key)                       \
  __asm__(".intel_syntax noprefix;"              \
          "call Lpb%=;"                          \
          "Lpb%=:"                               \
          "mov rsi, %0;"                         \
          "pop rdi;"                             \
          "call __unlock;"                       \
          ".byte 0xab,0xad,0xf0,0x0d;"           \
          : : "r"(key) : "rdi","rsi");
#define END_PROTECT()                            \
  __asm__(".intel_syntax noprefix;"              \
          ".byte 0x0d,0xf0,0xad,0xab;"           \
          "call __lock;"                         \
          : : );

int __current_scope = 0;
scope_t __scope[MAX_SCOPE] = { NULL };

void swap_state(void) {
  unsigned char *begin = __scope[__current_scope].f_begin + 4;
  unsigned char *end = __scope[__current_scope].f_end;
  size_t key = __scope[__current_scope].key;

  unsigned int A = key & 0xffffffff;
  unsigned int B = key >> 32;

  unsigned int X = (size_t)end - (size_t)begin;
  for(unsigned char *p = begin; p + sizeof(unsigned int) <= end; ++p) {
    X = A * X + B;
    *(unsigned int*)p ^= X;
  }
}

void contiguous_protect(void *addr, int prot) {
  void *base = (void*)((size_t)addr & 0xfffffffffffff000);

  while(mprotect(base, 0x1000, prot) != -1) {
    base += 0x1000;
  }
}

__attribute__((no_caller_saved_registers))
void __unlock(void *addr, size_t key) {
  contiguous_protect(addr, PROT_READ | PROT_WRITE | PROT_EXEC);

  /* Unmark BOF & EOF */
  unsigned char *p;
  for(p = addr; *(unsigned int*)p != MARK_BOF; p++);
  __scope[__current_scope].f_begin = p;
  *(unsigned int*)p = 0x90909090;
  for(p += sizeof(unsigned int); *(unsigned int*)p != MARK_EOF; p++);
  __scope[__current_scope].f_end = p;
  *(unsigned int*)p = 0x90909090;
  __scope[__current_scope].key = key;

  swap_state();

  __current_scope++;
  contiguous_protect(addr, PROT_READ | PROT_EXEC);
}

__attribute__((no_caller_saved_registers))
void __lock(void) {
  __current_scope--;
  void *addr = __scope[__current_scope].f_begin;

  contiguous_protect(addr, PROT_READ | PROT_WRITE | PROT_EXEC);

  /* Mark BOF & EOF */
  *(unsigned int*)__scope[__current_scope].f_begin = MARK_BOF;
  *(unsigned int*)__scope[__current_scope].f_end = MARK_EOF;

  swap_state();

  contiguous_protect(addr, PROT_READ | PROT_EXEC);
}
/***** ^^^^^ ***** OBFUSCATOR ****** ^^^^^ ******/
#define STORE32H(x, y)                                                                     \
     { (y)[0] = (unsigned char)(((x)>>24)&255); (y)[1] = (unsigned char)(((x)>>16)&255);   \
       (y)[2] = (unsigned char)(((x)>>8)&255); (y)[3] = (unsigned char)((x)&255); }
#define LOAD32H(x, y)                            \
     { x = ((unsigned long)((y)[0] & 255)<<24) | \
           ((unsigned long)((y)[1] & 255)<<16) | \
           ((unsigned long)((y)[2] & 255)<<8)  | \
           ((unsigned long)((y)[3] & 255)); }
#define ROL16(x, y) ((((x)<<(y)) | ((x)>>(16-(y)))) & 0xFFFF)

struct kasumi_key {
  uint32_t KLi1[8], KLi2[8],
    KOi1[8], KOi2[8], KOi3[8],
    KIi1[8], KIi2[8], KIi3[8];
};
typedef struct {
  struct kasumi_key kasumi;
  void *data;
} symmetric_key;

uint16_t FI(uint16_t in, uint16_t subkey )
{
  BEGIN_PROTECT(0x926f8490c6064008);

  uint16_t nine, seven;
  static const uint16_t S7[128] = {
    54, 50, 62, 56, 22, 34, 94, 96, 38, 6, 63, 93, 2, 18, 123, 33,
    55, 113, 39, 114, 21, 67, 65, 12, 47, 73, 46, 27, 25, 111,124, 81,
    53, 9, 121, 79, 52, 60, 58, 48, 101, 127, 40, 120, 104, 70, 71, 43,
    20, 122, 72, 61, 23, 109, 13, 100, 77, 1, 16, 7, 82, 10, 105, 98,
    117, 116, 76, 11, 89, 106, 0, 125, 118, 99, 86, 69, 30, 57, 126, 87,
    112, 51, 17, 5, 95, 14, 90, 84, 91, 8, 35,103, 32, 97, 28, 66,
    102, 31, 26, 45, 75, 4, 85, 92, 37, 74, 80, 49, 68, 29, 115, 44,
    64, 107, 108, 24, 110, 83, 36, 78, 42, 19, 15, 41, 88, 119, 59, 3
  };
  static const uint16_t S9[512] = {
    167,239,161,379,391,334, 9,338, 38,226, 48,358,452,385, 90,397,
    183,253,147,331,415,340, 51,362,306,500,262, 82,216,159,356,177,
    175,241,489, 37,206, 17, 0,333, 44,254,378, 58,143,220, 81,400,
    95, 3,315,245, 54,235,218,405,472,264,172,494,371,290,399, 76,
    165,197,395,121,257,480,423,212,240, 28,462,176,406,507,288,223,
    501,407,249,265, 89,186,221,428,164, 74,440,196,458,421,350,163,
    232,158,134,354, 13,250,491,142,191, 69,193,425,152,227,366,135,
    344,300,276,242,437,320,113,278, 11,243, 87,317, 36, 93,496, 27,
    487,446,482, 41, 68,156,457,131,326,403,339, 20, 39,115,442,124,
    475,384,508, 53,112,170,479,151,126,169, 73,268,279,321,168,364,
    363,292, 46,499,393,327,324, 24,456,267,157,460,488,426,309,229,
    439,506,208,271,349,401,434,236, 16,209,359, 52, 56,120,199,277,
    465,416,252,287,246, 6, 83,305,420,345,153,502, 65, 61,244,282,
    173,222,418, 67,386,368,261,101,476,291,195,430, 49, 79,166,330,
    280,383,373,128,382,408,155,495,367,388,274,107,459,417, 62,454,
    132,225,203,316,234, 14,301, 91,503,286,424,211,347,307,140,374,
    35,103,125,427, 19,214,453,146,498,314,444,230,256,329,198,285,
    50,116, 78,410, 10,205,510,171,231, 45,139,467, 29, 86,505, 32,
    72, 26,342,150,313,490,431,238,411,325,149,473, 40,119,174,355,
    185,233,389, 71,448,273,372, 55,110,178,322, 12,469,392,369,190,
    1,109,375,137,181, 88, 75,308,260,484, 98,272,370,275,412,111,
    336,318, 4,504,492,259,304, 77,337,435, 21,357,303,332,483, 18,
    47, 85, 25,497,474,289,100,269,296,478,270,106, 31,104,433, 84,
    414,486,394, 96, 99,154,511,148,413,361,409,255,162,215,302,201,
    266,351,343,144,441,365,108,298,251, 34,182,509,138,210,335,133,
    311,352,328,141,396,346,123,319,450,281,429,228,443,481, 92,404,
    485,422,248,297, 23,213,130,466, 22,217,283, 70,294,360,419,127,
    312,377, 7,468,194, 2,117,295,463,258,224,447,247,187, 80,398,
    284,353,105,390,299,471,470,184, 57,200,348, 63,204,188, 33,451,
    97, 30,310,219, 94,160,129,493, 64,179,263,102,189,207,114,402,
    438,477,387,122,192, 42,381, 5,145,118,180,449,293,323,136,380,
    43, 66, 60,455,341,445,202,432, 8,237, 15,376,436,464, 59,461};

  nine  = (uint16_t)(in >> 7) & 0x1FF;
  seven = (uint16_t)(in & 0x7F);

  nine   = (uint16_t)(S9[nine] ^ seven);
  seven  = (uint16_t)(S7[seven] ^ (nine & 0x7F));
  seven ^= (subkey >> 9);
  nine  ^= (subkey & 0x1FF);
  nine   = (uint16_t)(S9[nine] ^ seven);
  seven  = (uint16_t)(S7[seven] ^ (nine & 0x7F));

  END_PROTECT();
  return (uint16_t)(seven << 9) + nine;
}

static uint32_t FO(symmetric_key *key, uint32_t in, int round_no)
{
  BEGIN_PROTECT(0x2194d29e7590998d);
  uint16_t left, right;

  left = (uint16_t)(in >> 16);
  right = (uint16_t)in & 0xFFFF;

  left ^= key->kasumi.KOi1[round_no];
  left = FI(left, key->kasumi.KIi1[round_no]);
  left ^= right;

  right ^= key->kasumi.KOi2[round_no];
  right = FI(right, key->kasumi.KIi2[round_no]);
  right ^= left;

  left ^= key->kasumi.KOi3[round_no];
  left = FI(left, key->kasumi.KIi3[round_no]);
  left ^= right;

  END_PROTECT();
  return (((uint32_t)right) << 16) + left;
}

uint32_t FL(symmetric_key *key, uint32_t in, int round_no)
{
  BEGIN_PROTECT(0x07d9d585e6e989a8);
  uint16_t l, r, a, b;

  l = (uint16_t)(in >> 16);
  r = (uint16_t)(in) & 0xFFFF;
  a = (uint16_t)(l & key->kasumi.KLi1[round_no]);
  r ^= ROL16(a, 1);
  b = (uint16_t)(r | key->kasumi.KLi2[round_no]);
  l ^= ROL16(b, 1);

  END_PROTECT();
  return (((uint32_t)l)<<16) + r;
}

void kasumi_ecb_encrypt(symmetric_key *skey, const unsigned char *pt, unsigned char *ct)
{
  BEGIN_PROTECT(0x6ab9591947053767);
  uint32_t left, right, temp;
  int n;

  LOAD32H(left, pt);
  LOAD32H(right, pt+4);

  for (n = 0; n <= 7; ) {     
    temp = FL(skey, left, n);
    temp = FO(skey, temp, n++);
    right ^= temp;
    temp = FO(skey, right, n);
    temp = FL(skey, temp, n++);
    left ^= temp;
  }

  STORE32H(left, ct);
  STORE32H(right, ct+4);

  END_PROTECT();
}

void kasumi_cbc_encrypt(symmetric_key *skey, const unsigned char *iv,
                        const unsigned char *pt, unsigned char *ct,
                        int length)
{
  int i, j;

  char block[8];
  memcpy(block, iv, 8);
  for (i = 0; i < length / 8; i++) {
    for (j = 0; j < 8; j++) {
      block[j] ^= pt[i*8 + j];
    }
    kasumi_ecb_encrypt(skey, block, &ct[i*8]);
    memcpy(block, &ct[i*8], 8);
  }
}

void kasumi_setup(symmetric_key *skey, const unsigned char *key)
{
  BEGIN_PROTECT(0xd5df98abdac7303c);

  static const uint16_t C[8] = {0x0123, 0x4567, 0x89AB, 0xCDEF, 0xFEDC, 0xBA98, 0x7654, 0x3210};
  uint16_t ukey[8], Kprime[8];
  int n;

  for (n = 0; n < 8; n++ ) {
    ukey[n] = (((uint16_t)key[2*n]) << 8) | key[2*n+1];
  }

  for (n = 0; n < 8; n++) {
    Kprime[n] = ukey[n] ^ C[n];
  }

  for(n = 0; n < 8; n++) {
    skey->kasumi.KLi1[n] = ROL16(ukey[n],1);
    skey->kasumi.KLi2[n] = Kprime[(n+2)&0x7];
    skey->kasumi.KOi1[n] = ROL16(ukey[(n+1)&0x7],5);
    skey->kasumi.KOi2[n] = ROL16(ukey[(n+5)&0x7],8);
    skey->kasumi.KOi3[n] = ROL16(ukey[(n+6)&0x7],13);
    skey->kasumi.KIi1[n] = Kprime[(n+4)&0x7];
    skey->kasumi.KIi2[n] = Kprime[(n+3)&0x7];
    skey->kasumi.KIi3[n] = Kprime[(n+7)&0x7];
  }

  END_PROTECT();
}

uint64_t check(const unsigned char *flag) {
  BEGIN_PROTECT(0x989e105ba25f98eb);

  uint64_t r;
  unsigned char iv[8];
  uint64_t cipher[64 / sizeof(uint64_t)];
  symmetric_key key;

  kasumi_setup(&key, "zer0pts CTF 2021");
  memcpy(iv, "Lazy Fox", sizeof(iv));

  memset(cipher, 0, sizeof(cipher));
  kasumi_cbc_encrypt(&key, iv, flag, (char*)cipher, 64);

  r = 0;
  r |= cipher[0] ^ 0x2de23334718727bb;
  r |= cipher[1] ^ 0xb298de796e944115;
  r |= cipher[2] ^ 0xe45ef960fbec841b;
  r |= cipher[3] ^ 0x314fc3f835e2958e;
  r |= cipher[4] ^ 0xdc115329aa177509;
  r |= cipher[5] ^ 0x7cb37e8f516bc981;
  r |= cipher[6] ^ 0x2d9d9ad4adaf9925;
  r |= cipher[7] ^ 0x1808a242a2a693e1;

  END_PROTECT();
  return r;
}

int main(int argc, char **argv)
{
  char flag[64];

  printf("FLAG: ");
  memset(flag, 0, sizeof(flag));
  if (scanf("%63s", flag) != 1)
    _exit(1);
  if (check(flag)) {
    puts("Wrong...");
  } else {
    puts("Correct!");
  }

  return 0;
}
