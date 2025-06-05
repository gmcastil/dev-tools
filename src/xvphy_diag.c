#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/mman.h>
#include <stdint.h>

#include "xvphy.h"

#define XVPHY_BASE_ADDR 0x80010000
#define XVPHY_MAP_SIZE  0x1000

volatile uint32_t *xvphy_open()
{
	int fd = open("/dev/mem", O_RDONLY | O_SYNC);
	if (fd < 0) {
		perror("open /dev/mem");
		return NULL;
	}

	void *map = mmap(NULL, XVPHY_MAP_SIZE, PROT_READ, MAP_SHARED, fd, XVPHY_BASE_ADDR);
	close(fd);

	if (map == MAP_FAILED) {
		perror("mmap");
		return NULL;
	}

	return (volatile uint32_t *)map;
}

void xvphy_close(volatile uint32_t *regs)
{
	if (regs) {
		munmap((void *)regs, XVPHY_MAP_SIZE);
	}
}

int main(void)
{
	volatile uint32_t *regs = xvphy_open();
	if (!regs)
		return 1;

	xvphy_print_banner();
	xvphy_print_general(regs);
	xvphy_print_version_info(regs);
	xvphy_print_pll_status(regs);
	xvphy_print_refclk_selection(regs);
	xvphy_print_tx(regs);
	xvphy_print_rx(regs);
	xvphy_print_drp(regs);
	xvphy_print_interrupt(regs);
	xvphy_print_usrclk(regs);
	xvphy_print_clkdet(regs);
	xvphy_print_clkdet_control_status(regs);
	xvphy_print_dru(regs);
	xvphy_print_dru_control_status(regs);
	xvphy_print_patgen(regs);

	xvphy_close(regs);
	return 0;
}

