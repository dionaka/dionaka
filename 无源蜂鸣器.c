module beep
#(
    parameter CNT_MAX = 25'd24_999_999,
    parameter DO = 17'd95602,
    parameter RE = 17'd85179,
    parameter MI = 17'd75873,
    parameter FA = 17'd71633,
    parameter SO = 17'd63776,
    parameter LA = 17'd56818,
    parameter XI = 17'd50607
)
(
    input wire sys_clk,
    input wire sys_rst_n,
    output reg beep
);

reg [24:0] cnt;
reg [2:0] cnt_500ms;
reg [16:0] freq_cnt;
reg [16:0] freq_data;
wire [15:0] duty_data;

always@(posedge sys_clk or negedge sys_rst_n)
    if(!sys_rst_n)
        cnt <= 25'd0;
    else if(cnt == CNT_MAX)
        cnt <= 25'd0;
    else
        cnt <= cnt + 25'd1;
        
always@(posedge sys_clk or negedge sys_rst_n)
    if(!sys_rst_n)
        cnt_500ms <= 3'd0;
    else if((cnt_500ms == 3'd6) && (cnt == CNT_MAX))
        cnt_500ms <= 3'd0;
    else if(cnt == CNT_MAX)
        cnt_500ms <= cnt_500ms + 3'd1;
        
always@(posedge sys_clk or negedge sys_rst_n)
    if(!sys_rst_n)
        freq_cnt <= 17'd0;
    else if((cnt == CNT_MAX) || (freq_cnt == freq_data))
        freq_cnt <= 17'd0;   
    else
        freq_cnt <= freq_cnt + 17'd1;
        
always@(posedge sys_clk or negedge sys_rst_n)
    if(!sys_rst_n)
        freq_data <= DO;
    else
        case(cnt_500ms)
            3'd0:    freq_data <= DO;
            3'd1:    freq_data <= RE;
            3'd2:    freq_data <= MI;
            3'd3:    freq_data <= FA;
            3'd4:    freq_data <= SO;
            3'd5:    freq_data <= LA;
            3'd6:    freq_data <= XI;
            default: freq_data <= DO; 
        endcase       
        
assign duty_data = freq_data >> 1;

always@(posedge sys_clk or negedge sys_rst_n)
    if(!sys_rst_n)
        beep <= 1'b0;
    else if(freq_cnt >= duty_data)
        beep <= 1'b1;
    else
        beep <= 1'b0;
        
                                     
endmodule