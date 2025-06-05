#include <stdio.h>
#include <stdint.h>

#include "xvphy.h"
#include "xvphy_hw.h"

const char *xvphy_refclk_name(uint32_t sel)
{
	switch (sel) {
	case XVPHY_REF_CLK_SEL_XPLL_GTREFCLK0:
		return "GTREFCLK0";
	case XVPHY_REF_CLK_SEL_XPLL_GTREFCLK1:
		return "GTREFCLK1";
	case XVPHY_REF_CLK_SEL_XPLL_GTNORTHREFCLK0:  // also GTEASTREFCLK0
		return "GTNORTH/EASTREFCLK0";
	case XVPHY_REF_CLK_SEL_XPLL_GTNORTHREFCLK1:  // also GTEASTREFCLK1
		return "GTNORTH/EASTREFCLK1";
	case XVPHY_REF_CLK_SEL_XPLL_GTSOUTHREFCLK0:  // also GTWESTREFCLK0
		return "GTSOUTH/WESTREFCLK0";
	case XVPHY_REF_CLK_SEL_XPLL_GTSOUTHREFCLK1:  // also GTWESTREFCLK1
		return "GTSOUTH/WESTREFCLK1";
	case XVPHY_REF_CLK_SEL_XPLL_GTGREFCLK:
		return "GTGREFCLK";
	default:
		return "UNKNOWN";
	}
}
void xvphy_print_reg(const char *label, uint32_t value)
{
	if (!label) {
		printf("Error: Failed null pointer check\n");
		return;
	}
	printf("%-24s: 0x%08X\n", label, value);
}

void xvphy_print_banner()
{
	printf("\n");
	printf("====== VPHY Status ======\n");
}

void xvphy_print_general(volatile uint32_t *regs)
{
	printf("--- VPHY core: general registers ---\n");
	if (!regs) {
		fprintf(stderr, "%s\n", "Error: Null register pointer");
		return;
	}

	xvphy_print_reg("VERSION", regs[XVPHY_VERSION_REG / 4]);
	xvphy_print_reg("BANK SELECT", regs[XVPHY_BANK_SELECT_REG / 4]);
	xvphy_print_reg("REF CLK SELECT", regs[XVPHY_REF_CLK_SEL_REG / 4]);
	xvphy_print_reg("PLL RESET", regs[XVPHY_PLL_RESET_REG / 4]);
	xvphy_print_reg("PLL LOCK STATUS", regs[XVPHY_PLL_LOCK_STATUS_REG / 4]);
	xvphy_print_reg("TX INIT", regs[XVPHY_TX_INIT_REG / 4]);
	xvphy_print_reg("TX INIT STATUS", regs[XVPHY_TX_INIT_STATUS_REG / 4]);
	xvphy_print_reg("RX INIT", regs[XVPHY_RX_INIT_REG / 4]);
	xvphy_print_reg("RX INIT STATUS", regs[XVPHY_RX_INIT_STATUS_REG / 4]);
	xvphy_print_reg("IBUFDS GTXX CTRL", regs[XVPHY_IBUFDS_GTXX_CTRL_REG / 4]);
	xvphy_print_reg("POWERDOWN CONTROL", regs[XVPHY_POWERDOWN_CONTROL_REG / 4]);
	xvphy_print_reg("LOOPBACK CONTROL", regs[XVPHY_LOOPBACK_CONTROL_REG / 4]);
	xvphy_print_reg("ERROR IRQ", regs[XVPHY_ERR_IRQ / 4]);
}

void xvphy_print_version_info(volatile uint32_t *regs)
{
	uint32_t version;

	printf("--- VPHY core: version decoding ---\n");
	if (!regs) {
		fprintf(stderr, "%s\n", "Error: Null register pointer");
		return;
	}
	version = regs[XVPHY_VERSION_REG / 4];
	uint32_t internal_rev = (version & XVPHY_VERSION_INTER_REV_MASK);
	uint32_t core_patch = (version & XVPHY_VERSION_CORE_PATCH_MASK) 
					>> XVPHY_VERSION_CORE_PATCH_SHIFT;
	uint32_t core_rev = (version & XVPHY_VERSION_CORE_VER_REV_MASK)
					>> XVPHY_VERSION_CORE_VER_REV_SHIFT;
	uint32_t core_minor = (version & XVPHY_VERSION_CORE_VER_MNR_MASK)
					>> XVPHY_VERSION_CORE_VER_MNR_SHIFT;
	uint32_t core_major = (version & XVPHY_VERSION_CORE_VER_MJR_MASK)
					>> XVPHY_VERSION_CORE_VER_MJR_SHIFT;

	xvphy_print_reg("Core Major Version", core_major);
	xvphy_print_reg("Core Minor Version", core_minor);
	xvphy_print_reg("Core Revision", core_rev);
	xvphy_print_reg("Core Patch", core_patch);
	xvphy_print_reg("Internal Revision", internal_rev);
}

void xvphy_print_drp(volatile uint32_t *regs)
{
	printf("--- VPHY core: dynamic reconfig port (DRP) registers ---\n");
	if (!regs) {
		fprintf(stderr, "%s\n", "Error: Null register pointer");
		return;
	}

	xvphy_print_reg("DRP CONTROL CH1", regs[XVPHY_DRP_CONTROL_CH1_REG / 4]);
	xvphy_print_reg("DRP CONTROL CH2", regs[XVPHY_DRP_CONTROL_CH2_REG / 4]);
	xvphy_print_reg("DRP CONTROL CH3", regs[XVPHY_DRP_CONTROL_CH3_REG / 4]);
	xvphy_print_reg("DRP CONTROL CH4", regs[XVPHY_DRP_CONTROL_CH4_REG / 4]);

	xvphy_print_reg("DRP STATUS CH1", regs[XVPHY_DRP_STATUS_CH1_REG / 4]);
	xvphy_print_reg("DRP STATUS CH2", regs[XVPHY_DRP_STATUS_CH2_REG / 4]);
	xvphy_print_reg("DRP STATUS CH3", regs[XVPHY_DRP_STATUS_CH3_REG / 4]);
	xvphy_print_reg("DRP STATUS CH4", regs[XVPHY_DRP_STATUS_CH4_REG / 4]);

	xvphy_print_reg("DRP CONTROL COMMON", regs[XVPHY_DRP_CONTROL_COMMON_REG / 4]);
	xvphy_print_reg("DRP STATUS COMMON", regs[XVPHY_DRP_STATUS_COMMON_REG / 4]);

	xvphy_print_reg("DRP CONTROL TXMMCM", regs[XVPHY_DRP_CONTROL_TXMMCM_REG / 4]);
	xvphy_print_reg("DRP STATUS TXMMCM", regs[XVPHY_DRP_STATUS_TXMMCM_REG / 4]);

	xvphy_print_reg("DRP CONTROL RXMMCM", regs[XVPHY_DRP_CONTROL_RXMMCM_REG / 4]);
	xvphy_print_reg("DRP STATUS RXMMCM", regs[XVPHY_DRP_STATUS_RXMMCM_REG / 4]);

}

void xvphy_print_tx(volatile uint32_t *regs)
{
	printf("--- VPHY core: transmitter function registers ---\n");
	if (!regs) {
		fprintf(stderr, "%s\n", "Error: Null register pointer");
		return;
	}

	xvphy_print_reg("TX CONTROL", regs[XVPHY_TX_CONTROL_REG / 4]);
	xvphy_print_reg("TX BUFFER BYPASS", regs[XVPHY_TX_BUFFER_BYPASS_REG / 4]);
	xvphy_print_reg("TX STATUS", regs[XVPHY_TX_STATUS_REG / 4]);
	xvphy_print_reg("TX DRIVER CH12", regs[XVPHY_TX_DRIVER_CH12_REG / 4]);
	xvphy_print_reg("TX DRIVER CH34", regs[XVPHY_TX_DRIVER_CH34_REG / 4]);
}

void xvphy_print_rx(volatile uint32_t *regs)
{
	printf("--- VPHY core: receiver function registers ---\n");
	if (!regs) {
		fprintf(stderr, "%s\n", "Error: Null register pointer");
		return;
	}

	xvphy_print_reg("RX CONTROL", regs[XVPHY_RX_CONTROL_REG / 4]);
	xvphy_print_reg("RX STATUS", regs[XVPHY_RX_STATUS_REG / 4]);
	xvphy_print_reg("RX EQ/CDR", regs[XVPHY_RX_EQ_CDR_REG / 4]);
	xvphy_print_reg("RX TDLOCK", regs[XVPHY_RX_TDLOCK_REG / 4]);
}

void xvphy_print_interrupt(volatile uint32_t *regs)
{
	printf("--- VPHY core: interrupt registers ---\n");
	if (!regs) {
		fprintf(stderr, "%s\n", "Error: Null register pointer");
		return;
	}

	xvphy_print_reg("ERROR IRQ", regs[XVPHY_ERR_IRQ / 4]);
	xvphy_print_reg("INTR ENABLE", regs[XVPHY_INTR_EN_REG / 4]);
	xvphy_print_reg("INTR DISABLE", regs[XVPHY_INTR_DIS_REG / 4]);
	xvphy_print_reg("INTR MASK", regs[XVPHY_INTR_MASK_REG / 4]);
	xvphy_print_reg("INTR STATUS", regs[XVPHY_INTR_STS_REG / 4]);
}

void xvphy_print_usrclk(volatile uint32_t *regs)
{
	printf("--- VPHY core: user clocking (MMCM and BUFGGT) registers ---\n");
	if (!regs) {
		fprintf(stderr, "%s\n", "Error: Null register pointer");
		return;
	}

	/* TX user clocking */
	xvphy_print_reg("MMCM TXUSRCLK CTRL", regs[XVPHY_MMCM_TXUSRCLK_CTRL_REG / 4]);
	xvphy_print_reg("MMCM TXUSRCLK REG1", regs[XVPHY_MMCM_TXUSRCLK_REG1 / 4]);
	xvphy_print_reg("MMCM TXUSRCLK REG2", regs[XVPHY_MMCM_TXUSRCLK_REG2 / 4]);
	xvphy_print_reg("MMCM TXUSRCLK REG3", regs[XVPHY_MMCM_TXUSRCLK_REG3 / 4]);
	xvphy_print_reg("MMCM TXUSRCLK REG4", regs[XVPHY_MMCM_TXUSRCLK_REG4 / 4]);
	xvphy_print_reg("BUFGGT TXUSRCLK", regs[XVPHY_BUFGGT_TXUSRCLK_REG / 4]);
	xvphy_print_reg("MISC TXUSRCLK", regs[XVPHY_MISC_TXUSRCLK_REG / 4]);

	/* RX user clocking */
	xvphy_print_reg("MMCM RXUSRCLK CTRL", regs[XVPHY_MMCM_RXUSRCLK_CTRL_REG / 4]);
	xvphy_print_reg("MMCM RXUSRCLK REG1", regs[XVPHY_MMCM_RXUSRCLK_REG1 / 4]);
	xvphy_print_reg("MMCM RXUSRCLK REG2", regs[XVPHY_MMCM_RXUSRCLK_REG2 / 4]);
	xvphy_print_reg("MMCM RXUSRCLK REG3", regs[XVPHY_MMCM_RXUSRCLK_REG3 / 4]);
	xvphy_print_reg("MMCM RXUSRCLK REG4", regs[XVPHY_MMCM_RXUSRCLK_REG4 / 4]);
	xvphy_print_reg("BUFGGT RXUSRCLK", regs[XVPHY_BUFGGT_RXUSRCLK_REG / 4]);
	xvphy_print_reg("MISC RXUSRCLK", regs[XVPHY_MISC_RXUSRCLK_REG / 4]);
}

void xvphy_print_clkdet(volatile uint32_t *regs)
{
	printf("--- VPHY core: clock detector registers ---\n");
	if (!regs) {
		fprintf(stderr, "%s\n", "Error: Null register pointer");
		return;
	}

	xvphy_print_reg("CLKDET CTRL", regs[XVPHY_CLKDET_CTRL_REG / 4]);
	xvphy_print_reg("CLKDET STATUS", regs[XVPHY_CLKDET_STAT_REG / 4]);
	xvphy_print_reg("CLKDET FREQ TMR TO", regs[XVPHY_CLKDET_FREQ_TMR_TO_REG / 4]);
	xvphy_print_reg("CLKDET FREQ TX", regs[XVPHY_CLKDET_FREQ_TX_REG / 4]);
	xvphy_print_reg("CLKDET FREQ RX", regs[XVPHY_CLKDET_FREQ_RX_REG / 4]);
	xvphy_print_reg("CLKDET TMR TX", regs[XVPHY_CLKDET_TMR_TX_REG / 4]);
	xvphy_print_reg("CLKDET TMR RX", regs[XVPHY_CLKDET_TMR_RX_REG / 4]);
	xvphy_print_reg("CLKDET FREQ DRU", regs[XVPHY_CLKDET_FREQ_DRU_REG / 4]);
}

void xvphy_print_dru(volatile uint32_t *regs)
{
	printf("--- VPHY core: data recovery unit (DRU) registers ---\n");
	if (!regs) {
		fprintf(stderr, "%s\n", "Error: Null register pointer");
		return;
	}

	xvphy_print_reg("DRU CTRL", regs[XVPHY_DRU_CTRL_REG / 4]);
	xvphy_print_reg("DRU STATUS", regs[XVPHY_DRU_STAT_REG / 4]);

	/* Channels are 1-indexed - this is all almost certainly unneeded */
	for (int ch = 1; ch <= 4; ch++) {

		char label[32];

		snprintf(label, sizeof(label), "DRU CFREQ_L CH%d", ch);
		xvphy_print_reg(label, regs[XVPHY_DRU_CFREQ_L_REG(ch) / 4]);

		snprintf(label, sizeof(label), "DRU CFREQ_H CH%d", ch);
		xvphy_print_reg(label, regs[XVPHY_DRU_CFREQ_H_REG(ch) / 4]);

		snprintf(label, sizeof(label), "DRU GAIN CH%d", ch);
		xvphy_print_reg(label, regs[XVPHY_DRU_GAIN_REG(ch) / 4]);
	}
}

void xvphy_print_dru_control_status(volatile uint32_t *regs)
{
	printf("--- VPHY DRU: control and status ---\n");
	if (!regs) {
		fprintf(stderr, "%s\n", "Error: Null register pointer");
		return;
	}

	uint32_t ctrl = regs[XVPHY_DRU_CTRL_REG / 4];
	uint32_t stat = regs[XVPHY_DRU_STAT_REG / 4];

	for (int ch = 1; ch <= 4; ch++) {
		char label[32];

		snprintf(label, sizeof(label), "CH%d RST", ch);
		xvphy_print_reg(label, !!(ctrl & XVPHY_DRU_CTRL_RST_MASK(ch)));

		snprintf(label, sizeof(label), "CH%d ENABLE", ch);
		xvphy_print_reg(label, !!(ctrl & XVPHY_DRU_CTRL_EN_MASK(ch)));

		snprintf(label, sizeof(label), "CH%d ACTIVE", ch);
		xvphy_print_reg(label, !!(stat & XVPHY_DRU_STAT_ACTIVE_MASK(ch)));
	}

	uint32_t version = (stat & XVPHY_DRU_STAT_VERSION_MASK) >> XVPHY_DRU_STAT_VERSION_SHIFT;
	xvphy_print_reg("DRU Block Version", version);
}

void xvphy_print_clkdet_control_status(volatile uint32_t *regs)
{
	printf("--- VPHY clock detector: control / status ---\n");

	if (!regs) {
		fprintf(stderr, "%s\n", "Error: Null register pointer");
		return;
	}

	uint32_t ctrl = regs[XVPHY_CLKDET_CTRL_REG / 4];
	uint32_t stat = regs[XVPHY_CLKDET_STAT_REG / 4];

	/* CTRL flags */
	xvphy_print_reg("CLKDET RUN", !!(ctrl & XVPHY_CLKDET_CTRL_RUN_MASK));
	xvphy_print_reg("TX TMR CLR", !!(ctrl & XVPHY_CLKDET_CTRL_TX_TMR_CLR_MASK));
	xvphy_print_reg("RX TMR CLR", !!(ctrl & XVPHY_CLKDET_CTRL_RX_TMR_CLR_MASK));
	xvphy_print_reg("TX FREQ RST", !!(ctrl & XVPHY_CLKDET_CTRL_TX_FREQ_RST_MASK));
	xvphy_print_reg("RX FREQ RST", !!(ctrl & XVPHY_CLKDET_CTRL_RX_FREQ_RST_MASK));

	uint32_t thresh = (ctrl & XVPHY_CLKDET_CTRL_FREQ_LOCK_THRESH_MASK) >> XVPHY_CLKDET_CTRL_FREQ_LOCK_THRESH_SHIFT;
	xvphy_print_reg("FREQ LOCK THRESH", thresh);

	uint32_t acc_range = (ctrl & XVPHY_CLKDET_CTRL_ACC_RANGE_MASK) >> XVPHY_CLKDET_CTRL_ACC_RANGE_SHIFT;
	xvphy_print_reg("ACC RANGE", acc_range);

	/* STAT flags */
	xvphy_print_reg("TX FREQ ZERO", !!(stat & XVPHY_CLKDET_STAT_TX_FREQ_ZERO_MASK));
	xvphy_print_reg("RX FREQ ZERO", !!(stat & XVPHY_CLKDET_STAT_RX_FREQ_ZERO_MASK));
	xvphy_print_reg("TX REFCLK LOCK", !!(stat & XVPHY_CLKDET_STAT_TX_REFCLK_LOCK_MASK));
	xvphy_print_reg("TX REFCLK LOCK CAP", !!(stat & XVPHY_CLKDET_STAT_TX_REFCLK_LOCK_CAP_MASK));
}

void xvphy_print_refclk_selection(volatile uint32_t *regs)
{
	printf("--- VPHY ref clock select ---\n");
	if (!regs) {
		fprintf(stderr, "%s\n", "Error: Null register pointer");
		return;
	}

	uint32_t reg = regs[XVPHY_REF_CLK_SEL_REG / 4];

	uint32_t qpll0 = reg & XVPHY_REF_CLK_SEL_QPLL0_MASK;
	uint32_t cpll  = (reg & XVPHY_REF_CLK_SEL_CPLL_MASK) >> XVPHY_REF_CLK_SEL_CPLL_SHIFT;
	uint32_t qpll1 = (reg & XVPHY_REF_CLK_SEL_QPLL1_MASK) >> XVPHY_REF_CLK_SEL_QPLL1_SHIFT;

	printf("QPLL0 REFCLK SELECT : %u (%s)\n", qpll0, xvphy_refclk_name(qpll0));
	printf("CPLL  REFCLK SELECT : %u (%s)\n", cpll,  xvphy_refclk_name(cpll));
	printf("QPLL1 REFCLK SELECT : %u (%s)\n", qpll1, xvphy_refclk_name(qpll1));
}

void xvphy_print_pll_status(volatile uint32_t *regs)
{
	printf("--- VPHY core: PLL reset and lock status ---\n");
	if (!regs) {
		fprintf(stderr, "%s\n", "Error: Null register pointer");
		return;
	}

	uint32_t rst = regs[XVPHY_PLL_RESET_REG / 4];
	uint32_t lock = regs[XVPHY_PLL_LOCK_STATUS_REG / 4];

	printf("PLL reset:\n");
	printf("  CPLL  : %s\n", (rst & XVPHY_PLL_RESET_CPLL_MASK) ? "RESET" : "OK");
	printf("  QPLL0 : %s\n", (rst & XVPHY_PLL_RESET_QPLL0_MASK) ? "RESET" : "OK");
	printf("  QPLL1 : %s\n", (rst & XVPHY_PLL_RESET_QPLL1_MASK) ? "RESET" : "OK");

	printf("PLL lock status:\n");
	printf("  CPLL CH1 : %s\n", (lock & XVPHY_PLL_LOCK_STATUS_CPLL_MASK(1)) ? "LOCKED" : "UNLOCKED");
	printf("  CPLL CH2 : %s\n", (lock & XVPHY_PLL_LOCK_STATUS_CPLL_MASK(2)) ? "LOCKED" : "UNLOCKED");
	printf("  CPLL CH3 : %s\n", (lock & XVPHY_PLL_LOCK_STATUS_CPLL_MASK(3)) ? "LOCKED" : "UNLOCKED");
	printf("  CPLL CH4 : %s\n", (lock & XVPHY_PLL_LOCK_STATUS_CPLL_MASK(4)) ? "LOCKED" : "UNLOCKED");
	printf("  QPLL0    : %s\n", (lock & XVPHY_PLL_LOCK_STATUS_QPLL0_MASK) ? "LOCKED" : "UNLOCKED");
	printf("  QPLL1    : %s\n", (lock & XVPHY_PLL_LOCK_STATUS_QPLL1_MASK) ? "LOCKED" : "UNLOCKED");

	printf("\n");
}

void xvphy_print_patgen(volatile uint32_t *regs)
{
	printf("--- VPHY core: TMDS pattern generator register ---\n");
	if (!regs) {
		fprintf(stderr, "%s\n", "Error: Null register pointer");
		return;
	}

	xvphy_print_reg("PATGEN CTRL", regs[XVPHY_PATGEN_CTRL_REG / 4]);
}

