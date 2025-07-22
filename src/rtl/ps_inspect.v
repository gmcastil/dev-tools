module ps_inspect #(
    localparam integer PRESCALE     = 8
)
(
    // Fabric clocks from the PS to be scaled down
    input   wire        pl_clk_0,
    input   wire        pl_clk_1,
    input   wire        pl_clk_2,
    input   wire        pl_clk_3,

    // Clock for pre-synthesis ILA insertion
    (* MARK_DEBUG = "TRUE" *)
    input   wire        ila_clk,

    // Asynchronous reset from PS
    (* MARK_DEBUG = "TRUE" *)
    input   wire        pl_resetn,

    // Synchronized reset signals, probably from PS reset IP
    (* MARK_DEBUG = "TRUE" *)
    input   wire        rst_0,
    (* MARK_DEBUG = "TRUE" *)
    input   wire        rst_1,
    (* MARK_DEBUG = "TRUE" *)
    input   wire        rst_2,
    (* MARK_DEBUG = "TRUE" *)
    input   wire        rst_3,

    // Scaled clock outputs (broken out as wires 
    (* MARK_DEBUG = "TRUE" *)
    output  wire        div_pl_clk_0,
    (* MARK_DEBUG = "TRUE" *)
    output  wire        div_pl_clk_1,
    (* MARK_DEBUG = "TRUE" *)
    output  wire        div_pl_clk_2,
    (* MARK_DEBUG = "TRUE" *)
    output  wire        div_pl_clk_3

);

    localparam integer WIDTH = $clog2(PRESCALE);

    reg [(WIDTH-1):0]   counter [3:0];

    // Clocks are bused here to make the logic simpler and then exported as
    // individual pins to make it easier hook up clocks and such in IPI or elsewhere.
    wire [3:0]          pl_clk;
    reg [3:0]           div_pl_clk;

    assign pl_clk       = { pl_clk_3, pl_clk_2, pl_clk_1, pl_clk_0 };

    assign div_pl_clk_0 = div_pl_clk[0];
    assign div_pl_clk_1 = div_pl_clk[1];
    assign div_pl_clk_2 = div_pl_clk[2];
    assign div_pl_clk_3 = div_pl_clk[3];

    genvar i;
    generate
        for (i = 0; i < 4; i = i + 1) begin: g_clk_div
            always @(posedge pl_clk[i]) begin
                counter[i]          <= counter[i] + 1;

                if ( counter[i] == (PRESCALE >> 1) - 1 ) begin
                    div_pl_clk[i]       <= ~div_pl_clk[i];
                    counter[i]          <= 0;
                end

            end
        end
    endgenerate

endmodule
