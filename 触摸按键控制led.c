//电容触摸按钮控制LED  摸一下开摸一下关
module touch_ctrl_led
(
    input wire sys_clk,
    input wire sys_rst_n,
    input wire touch_key,
    output wire led
);

//保持
reg touch_key1;
//延迟一拍
reg touch_key2;
//组合逻辑  脉冲  若使用时序边缘检测落后一个时钟
wire touch_flag;

//边沿检测
always@(posedge sys_clk or negedge sys_rst_n)
    if(!sys_rst_n)
        begin
            touch_key1 <= 1'b1;
            touch_key2 <= 1'b1;
        end
    else
        begin
            touch_key1 <= touch_key;
            touch_key2 <= touch_key1;
        end

assign touch_flag = ((touch_key1 == 1'b0) && (touch_key2 == 1'b1));

always@(posedge sys_clk or negedge sys_rst_n)
    if(!sys_rst_n)
        led <= 1'b1;
    else if(touch_flag == 1'b1)    
        led <= ~led;
        
endmodule