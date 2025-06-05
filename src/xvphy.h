#ifndef XVPHY_H
#define XVPHY_H

#include <stdint.h>

void xvphy_print_banner(void);
void xvphy_print_reg(const char *label, uint32_t value);
const char *xvphy_refclk_name(uint32_t sel);

void xvphy_print_general(volatile uint32_t *regs);
void xvphy_print_version_info(uint32_t version);
void xvphy_print_drp(volatile uint32_t *regs);
void xvphy_print_tx(volatile uint32_t *regs);
void xvphy_print_rx(volatile uint32_t *regs);
void xvphy_print_interrupt(volatile uint32_t *regs);
void xvphy_print_usrclk(volatile uint32_t *regs);
void xvphy_print_clkdet(volatile uint32_t *regs);
void xvphy_print_dru(volatile uint32_t *regs);
void xvphy_print_dru_control_status(volatile uint32_t *regs);
void xvphy_print_clkdet_control_status(volatile uint32_t *regs);
void xvphy_print_refclk_selection(volatile uint32_t *regs);
void xvphy_print_pll_status(volatile uint32_t *regs);
void xvphy_print_patgen(volatile uint32_t *regs);

#endif // XVPHY_H


