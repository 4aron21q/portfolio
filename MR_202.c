#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <termios.h>
int setup_serial(const char *port_name) {
    int fd = open(port_name, O_RDWR | O_NOCTTY | O_NDELAY);
    if (fd == -1) {
        perror("Не удалось открыть порт");
        return -1;
    }

    struct termios options;
    tcgetattr(fd, &options);
    
    cfsetispeed(&options, B9600);
    cfsetospeed(&options, B9600);
    options.c_cflag &= ~PARENB;
    options.c_cflag &= ~CSTOPB;
    options.c_cflag &= ~CSIZE;
    options.c_cflag |= CS8;
    options.c_cflag &= ~CRTSCTS;
    options.c_lflag = 0; // Raw mode
    options.c_iflag = 0;
    options.c_oflag = 0;

    tcsetattr(fd, TCSANOW, &options);
    return fd;
}

unsigned char calc_checksum(unsigned char *data, int len) {
    unsigned char sum = 0;
    for (int i = 0; i < len; i++) {
        sum += data[i];
    }
    return sum;
}

int main() {
    int fd = setup_serial("/dev/ttyUSB0"); 
    if (fd < 0) return 1;

    printf("Опрос\n");

    while (1) {
        unsigned char request[3];
        request[0] = 0x01; 
        request[1] = 0x06;
        request[2] = calc_checksum(request, 2); // КС

        
        write(fd, request, 3);
        
        usleep(100000);

        
        unsigned char buffer[32];
        int bytes_read = read(fd, buffer, sizeof(buffer));

        if (bytes_read > 0) {
            printf("Получено байт: %d | Данные: ", bytes_read);
            for (int i = 0; i < bytes_read; i++) {
                printf("%02X ", buffer[i]);
            }
            printf("\n");
        } else {
            printf("Нет ответа\n");
        }

        sleep(5); 
    }

    close(fd);
    return 0;
}