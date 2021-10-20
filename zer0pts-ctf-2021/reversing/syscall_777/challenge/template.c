#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <signal.h>
#include <string.h>
#include <stddef.h>
#include <linux/filter.h>
#include <linux/seccomp.h>
#include <sys/prctl.h>
#include <sys/ptrace.h>
#include <sys/syscall.h>
#include <pthread.h>

__attribute__((constructor))
void setup(void) {

  /* setup seccomp */
  if (prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0)) {
    exit(1);
  }

  struct sock_filter filter[] = {
%%%%
  };

  struct sock_fprog prog = {
    .len = (unsigned short)(sizeof(filter) / sizeof(filter[0])),
    .filter = filter,
  };
  if (prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &prog)) {
    exit(1);
  }
}

int main(int argc, char **argv) {
  int i;
  unsigned int flag[14] = {0};

  printf("FLAG: ");
  if (scanf("%55s", (char*)flag) != 1) return 1;

  for(i = 0; i < 14; i++) {
    syscall(777, flag[i], flag[(i+1)%14], flag[(i+2)%14], flag[(i+3)%14]);
    if (errno == 1) {
      puts("Wrong...");
      return 1;
    }
  }

  puts("Correct!");
  return 0;
}
