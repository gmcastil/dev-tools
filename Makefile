CC = gcc
CFLAGS = -Wall -Wextra -Isrc

SRC_DIR = src
SRC_FILES = $(wildcard $(SRC_DIR)/*.c)
OBJ_FILES = $(SRC_FILES:.c=.o)
TARGET = xvphy_diag

all: $(TARGET)

$(TARGET): $(OBJ_FILES)
	$(CC) $(CFLAGS) -o $@ $^

clean:
	rm -f $(SRC_DIR)/*.o $(TARGET)

.PHONY: all clean

