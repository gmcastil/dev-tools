#include <stdio.h>
#include <stdint.h>
#include "xvphy.h"

#define XVPHY_BASEADDR 0x80010000U
#define XVPHY_REG_PTR ((volatile uint32_t *)XVPHY_BASEADDR)

int main(void)
{
	xvphy_print_banner();
	xvphy_print_general(XVPHY_REG_PTR);
	xvphy_print_version_info(XVPHY_REG_PTR[XVPHY_VERSION_REG / 4]);
	xvphy_print_pll_status(XVPHY_REG_PTR);
	xvphy_print_refclk_selection(XVPHY_REG_PTR);
	xvphy_print_tx(XVPHY_REG_PTR);
	xvphy_print_rx(XVPHY_REG_PTR);
	xvphy_print_usrclk(XVPHY_REG_PTR);
	xvphy_print_clkdet(XVPHY_REG_PTR);
	xvphy_print_clkdet_control_status(XVPHY_REG_PTR);
	xvphy_print_drp(XVPHY_REG_PTR);
	xvphy_print_dru(XVPHY_REG_PTR);
	xvphy_print_dru_control_status(XVPHY_REG_PTR);
	xvphy_print_interrupt(XVPHY_REG_PTR);
	xvphy_print_patgen(XVPHY_REG_PTR);

	return 0;
}

