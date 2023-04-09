#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>

#define BUFSIZE 1024

int main(int argc, char* argv[]) {
    int fd;
    ssize_t n;
    double buf[BUFSIZE];
    struct stat st;


    if (argc != 2) {
        printf("Usage: %s <filename>\n", argv[0]);
        return 1;
    }

    if ((fd = open(argv[1], O_RDONLY)) < 0) {
        perror("open");
        return 1;
    }


    if (fstat(fd, &st) < 0) {
        perror("fstat");
        return 1;
    }

    printf("The size of %s is %ld bytes.\n", argv[1], st.st_size);

    while ((n = read(fd, buf, sizeof(buf))) > 0) {
        for (ssize_t i = 0; i < n / sizeof(double); i++) {
            double value = buf[i];
            // 읽어들인 double 값을 사용하는 코드를 작성합니다.
            printf("%f\n", value);
        }
    }

    if (n < 0) {
        perror("read");
        return 1;
    }

    if (close(fd) < 0) {
        perror("close");
        return 1;
    }

    return 0;
}
