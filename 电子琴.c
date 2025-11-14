// ============================================================================
// FPGA电子琴完整系统 - Cyclone IV E
// 功能：矩阵键盘扫描、音符生成、DDS合成、和弦支持、自动演奏、录音回放
// ============================================================================

// ============================================================================
// 1. 顶层模块
// ============================================================================
module top (
    input wire clk_50m,           // 50MHz时钟
    input wire rst_n,             // 复位按键(低电平有效)
    input wire [2:0] func_key,    // 3个功能键
    input wire [3:0] key_row,     // 矩阵键盘行输入
    output wire [3:0] key_col,     // 矩阵键盘列扫描输出
    output wire [3:0] led,        // 4个LED
    output wire buzzer,           // 无源蜂鸣器
    output wire speaker,          // 扬声器输出
    output wire [5:0] seg_sel,    // 数码管位选
    output wire [7:0] seg_data,   // 数码管段选
    input wire uart_rx            // UART接收
);

    // 内部信号
    wire [3:0] key_value;
    wire key_pressed;
    wire [4:0] note_code;         // 音符编码 (0-11为C-B, 12-23为高八度)
    wire [2:0] octave;            // 八度选择 (0=低, 1=中, 2=高)
    wire [15:0] note_freq;        // 音符频率
    wire [15:0] audio_out;        // 音频输出
    wire pwm_out;
    wire dds_out;
    
    // 功能控制信号
    wire output_sel;              // 0=蜂鸣器, 1=扬声器
    wire [3:0] volume;            // 音量等级
    wire play_mode;               // 0=手动, 1=自动演奏
    wire record_en;               // 录音使能
    wire playback_en;             // 回放使能
    
    // 和弦支持 - 最多3个音符
    wire [4:0] note1, note2, note3;
    wire note1_en, note2_en, note3_en;
    
    // 时钟分频
    wire clk_1k, clk_100k, clk_scan;
    
    // 功能键解析
    assign output_sel = func_key[0];    // 输出模式切换
    assign play_mode = func_key[1];     // 播放模式
    assign record_en = func_key[2];     // 录音/回放
    
    // ========================================================================
    // 时钟分频模块实例化
    // ========================================================================
    clk_divider u_clk_div (
        .clk(clk_50m),
        .rst_n(rst_n),
        .clk_1k(clk_1k),
        .clk_100k(clk_100k),
        .clk_scan(clk_scan)
    );
    
    // ========================================================================
    // 矩阵键盘扫描模块
    // ========================================================================
    key_scan u_key_scan (
        .clk(clk_scan),
        .rst_n(rst_n),
        .key_row(key_row),
        .key_col(key_col),
        .key_value(key_value),
        .key_pressed(key_pressed)
    );
    
    // ========================================================================
    // 按键消抖模块
    // ========================================================================
    wire [3:0] key_value_stable;
    wire key_stable;
    
    key_debounce u_debounce (
        .clk(clk_1k),
        .rst_n(rst_n),
        .key_in(key_value),
        .key_pressed_in(key_pressed),
        .key_out(key_value_stable),
        .key_valid(key_stable)
    );
    
    // ========================================================================
    // 音符译码模块
    // ========================================================================
    note_decoder u_note_dec (
        .clk(clk_50m),
        .rst_n(rst_n),
        .key_value(key_value_stable),
        .key_valid(key_stable),
        .octave_sel(octave),
        .note_code(note_code),
        .note1(note1),
        .note2(note2),
        .note3(note3),
        .note1_en(note1_en),
        .note2_en(note2_en),
        .note3_en(note3_en)
    );
    
    // ========================================================================
    // 频率表查找
    // ========================================================================
    freq_table u_freq_table (
        .note_code(note_code),
        .note_freq(note_freq)
    );
    
    // ========================================================================
    // DDS波形生成器（用于扬声器，支持和弦）
    // ========================================================================
    wire [15:0] dds_out1, dds_out2, dds_out3;
    wire [15:0] note_freq1, note_freq2, note_freq3;
    
    freq_table u_freq1 (.note_code(note1), .note_freq(note_freq1));
    freq_table u_freq2 (.note_code(note2), .note_freq(note_freq2));
    freq_table u_freq3 (.note_code(note3), .note_freq(note_freq3));
    
    dds_generator u_dds1 (
        .clk(clk_50m),
        .rst_n(rst_n),
        .freq(note_freq1),
        .enable(note1_en),
        .wave_out(dds_out1)
    );
    
    dds_generator u_dds2 (
        .clk(clk_50m),
        .rst_n(rst_n),
        .freq(note_freq2),
        .enable(note2_en),
        .wave_out(dds_out2)
    );
    
    dds_generator u_dds3 (
        .clk(clk_50m),
        .rst_n(rst_n),
        .freq(note_freq3),
        .enable(note3_en),
        .wave_out(dds_out3)
    );
    
    // ========================================================================
    // 和弦混音器
    // ========================================================================
    wire [15:0] mixed_audio;
    
    chord_mixer u_mixer (
        .clk(clk_50m),
        .rst_n(rst_n),
        .audio1(dds_out1),
        .audio2(dds_out2),
        .audio3(dds_out3),
        .en1(note1_en),
        .en2(note2_en),
        .en3(note3_en),
        .mixed_out(mixed_audio)
    );
    
    // ========================================================================
    // 包络发生器
    // ========================================================================
    wire [15:0] envelope_audio;
    
    envelope_generator u_envelope (
        .clk(clk_50m),
        .rst_n(rst_n),
        .note_on(key_stable),
        .audio_in(mixed_audio),
        .audio_out(envelope_audio)
    );
    
    // ========================================================================
    // 音量控制
    // ========================================================================
    volume_control u_volume (
        .clk(clk_50m),
        .rst_n(rst_n),
        .audio_in(envelope_audio),
        .volume_level(volume),
        .audio_out(audio_out)
    );
    
    // ========================================================================
    // PWM生成器（用于蜂鸣器）
    // ========================================================================
    pwm_generator u_pwm (
        .clk(clk_50m),
        .rst_n(rst_n),
        .freq(note_freq),
        .enable(key_stable),
        .duty_cycle(8'd128),
        .pwm_out(pwm_out)
    );
    
    // ========================================================================
    // UART接收模块（用于自动演奏）
    // ========================================================================
    wire [7:0] uart_data;
    wire uart_valid;
    
    uart_rx_module u_uart (
        .clk(clk_50m),
        .rst_n(rst_n),
        .rx(uart_rx),
        .data_out(uart_data),
        .data_valid(uart_valid)
    );
    
    // ========================================================================
    // 自动演奏模块
    // ========================================================================
    wire [4:0] auto_note;
    wire auto_note_en;
    
    auto_play u_auto_play (
        .clk(clk_50m),
        .rst_n(rst_n),
        .enable(play_mode),
        .uart_data(uart_data),
        .uart_valid(uart_valid),
        .note_out(auto_note),
        .note_enable(auto_note_en)
    );
    
    // ========================================================================
    // 录音回放模块
    // ========================================================================
    wire [4:0] playback_note;
    wire playback_note_en;
    
    record_playback u_record (
        .clk(clk_50m),
        .rst_n(rst_n),
        .record_en(record_en && !playback_en),
        .playback_en(record_en && playback_en),
        .note_in(note_code),
        .note_in_valid(key_stable),
        .note_out(playback_note),
        .note_out_valid(playback_note_en)
    );
    
    // ========================================================================
    // 数码管显示模块
    // ========================================================================
    seg_display u_seg_display (
        .clk(clk_1k),
        .rst_n(rst_n),
        .note_code(note_code),
        .volume(volume),
        .mode(play_mode),
        .seg_sel(seg_sel),
        .seg_data(seg_data)
    );
    
    // ========================================================================
    // LED指示模块
    // ========================================================================
    led_indicator u_led (
        .clk(clk_1k),
        .rst_n(rst_n),
        .note_code(note_code),
        .key_pressed(key_stable),
        .led(led)
    );
    
    // ========================================================================
    // 输出选择
    // ========================================================================
    assign buzzer = output_sel ? 1'b0 : pwm_out;
    assign speaker = output_sel ? audio_out[15] : 1'b0;
    
    // 八度控制（通过按键）
    assign octave = 3'd1;  // 默认中音，可扩展

endmodule

// ============================================================================
// 2. 时钟分频模块
// ============================================================================
module clk_divider (
    input wire clk,           // 50MHz
    input wire rst_n,
    output reg clk_1k,        // 1kHz for debounce
    output reg clk_100k,      // 100kHz for general use
    output reg clk_scan       // ~1kHz for key scan
);

    reg [15:0] cnt_1k;
    reg [8:0] cnt_100k;
    reg [15:0] cnt_scan;
    
    // 1kHz生成 (50MHz/50000 = 1kHz)
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            cnt_1k <= 16'd0;
            clk_1k <= 1'b0;
        end else if (cnt_1k == 16'd24999) begin
            cnt_1k <= 16'd0;
            clk_1k <= ~clk_1k;
        end else begin
            cnt_1k <= cnt_1k + 1'b1;
        end
    end
    
    // 100kHz生成
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            cnt_100k <= 9'd0;
            clk_100k <= 1'b0;
        end else if (cnt_100k == 9'd249) begin
            cnt_100k <= 9'd0;
            clk_100k <= ~clk_100k;
        end else begin
            cnt_100k <= cnt_100k + 1'b1;
        end
    end
    
    // 扫描时钟 ~1kHz
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            cnt_scan <= 16'd0;
            clk_scan <= 1'b0;
        end else if (cnt_scan == 16'd25000) begin
            cnt_scan <= 16'd0;
            clk_scan <= ~clk_scan;
        end else begin
            cnt_scan <= cnt_scan + 1'b1;
        end
    end

endmodule

// ============================================================================
// 3. 矩阵键盘扫描模块 (4×4)
// ============================================================================
module key_scan (
    input wire clk,               // 扫描时钟 ~1kHz
    input wire rst_n,
    input wire [3:0] key_row,     // 行输入
    output reg [3:0] key_col,     // 列扫描输出
    output reg [3:0] key_value,   // 按键值 0-15
    output reg key_pressed        // 按键按下标志
);

    reg [1:0] scan_cnt;
    reg [3:0] key_row_reg;
    
    // 列扫描循环
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            scan_cnt <= 2'd0;
            key_col <= 4'b1110;
        end else begin
            scan_cnt <= scan_cnt + 1'b1;
            case (scan_cnt)
                2'd0: key_col <= 4'b1110;
                2'd1: key_col <= 4'b1101;
                2'd2: key_col <= 4'b1011;
                2'd3: key_col <= 4'b0111;
            endcase
        end
    end
    
    // 行输入采样
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            key_row_reg <= 4'b1111;
        end else begin
            key_row_reg <= key_row;
        end
    end
    
    // 按键译码
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            key_value <= 4'd0;
            key_pressed <= 1'b0;
        end else begin
            if (key_row_reg != 4'b1111) begin
                key_pressed <= 1'b1;
                case ({scan_cnt, key_row_reg})
                    // 第0列
                    {2'd0, 4'b1110}: key_value <= 4'd0;  // C
                    {2'd0, 4'b1101}: key_value <= 4'd1;  // C#
                    {2'd0, 4'b1011}: key_value <= 4'd2;  // D
                    {2'd0, 4'b0111}: key_value <= 4'd3;  // D#
                    // 第1列
                    {2'd1, 4'b1110}: key_value <= 4'd4;  // E
                    {2'd1, 4'b1101}: key_value <= 4'd5;  // F
                    {2'd1, 4'b1011}: key_value <= 4'd6;  // F#
                    {2'd1, 4'b0111}: key_value <= 4'd7;  // G
                    // 第2列
                    {2'd2, 4'b1110}: key_value <= 4'd8;  // G#
                    {2'd2, 4'b1101}: key_value <= 4'd9;  // A
                    {2'd2, 4'b1011}: key_value <= 4'd10; // A#
                    {2'd2, 4'b0111}: key_value <= 4'd11; // B
                    // 第3列
                    {2'd3, 4'b1110}: key_value <= 4'd12; // C(高八度)
                    {2'd3, 4'b1101}: key_value <= 4'd13; // 功能键1
                    {2'd3, 4'b1011}: key_value <= 4'd14; // 功能键2
                    {2'd3, 4'b0111}: key_value <= 4'd15; // 功能键3
                    default: key_value <= key_value;
                endcase
            end else begin
                key_pressed <= 1'b0;
            end
        end
    end

endmodule

// ============================================================================
// 4. 按键消抖模块
// ============================================================================
module key_debounce (
    input wire clk,               // 1kHz
    input wire rst_n,
    input wire [3:0] key_in,
    input wire key_pressed_in,
    output reg [3:0] key_out,
    output reg key_valid
);

    reg [3:0] key_reg1, key_reg2, key_reg3;
    reg key_pressed_reg1, key_pressed_reg2;
    reg [7:0] debounce_cnt;
    
    parameter DEBOUNCE_TIME = 8'd20;  // 20ms
    
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            key_reg1 <= 4'd0;
            key_reg2 <= 4'd0;
            key_reg3 <= 4'd0;
            key_pressed_reg1 <= 1'b0;
            key_pressed_reg2 <= 1'b0;
            debounce_cnt <= 8'd0;
            key_out <= 4'd0;
            key_valid <= 1'b0;
        end else begin
            key_reg1 <= key_in;
            key_reg2 <= key_reg1;
            key_reg3 <= key_reg2;
            key_pressed_reg1 <= key_pressed_in;
            key_pressed_reg2 <= key_pressed_reg1;
            
            if (key_pressed_reg2 && (key_reg2 == key_reg3)) begin
                if (debounce_cnt < DEBOUNCE_TIME) begin
                    debounce_cnt <= debounce_cnt + 1'b1;
                    key_valid <= 1'b0;
                end else begin
                    key_out <= key_reg2;
                    key_valid <= 1'b1;
                end
            end else begin
                debounce_cnt <= 8'd0;
                key_valid <= 1'b0;
            end
        end
    end

endmodule

// ============================================================================
// 5. 音符译码模块
// ============================================================================
module note_decoder (
    input wire clk,
    input wire rst_n,
    input wire [3:0] key_value,
    input wire key_valid,
    input wire [2:0] octave_sel,      // 八度选择
    output reg [4:0] note_code,       // 音符编码
    output reg [4:0] note1,           // 和弦音符1
    output reg [4:0] note2,           // 和弦音符2
    output reg [4:0] note3,           // 和弦音符3
    output reg note1_en,
    output reg note2_en,
    output reg note3_en
);

    reg [4:0] note_buffer [0:2];
    reg [1:0] note_count;
    
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            note_code <= 5'd0;
            note1 <= 5'd0;
            note2 <= 5'd0;
            note3 <= 5'd0;
            note1_en <= 1'b0;
            note2_en <= 1'b0;
            note3_en <= 1'b0;
            note_count <= 2'd0;
        end else if (key_valid) begin
            // 基础音符 + 八度偏移
            note_code <= key_value + (octave_sel * 5'd12);
            
            // 和弦支持：存储最近按下的3个音符
            if (note_count < 2'd3) begin
                note_buffer[note_count] <= key_value + (octave_sel * 5'd12);
                note_count <= note_count + 1'b1;
            end else begin
                note_buffer[0] <= note_buffer[1];
                note_buffer[1] <= note_buffer[2];
                note_buffer[2] <= key_value + (octave_sel * 5'd12);
            end
            
            note1 <= note_buffer[0];
            note2 <= note_buffer[1];
            note3 <= note_buffer[2];
            
            note1_en <= (note_count >= 2'd1);
            note2_en <= (note_count >= 2'd2);
            note3_en <= (note_count >= 2'd3);
        end else begin
            // 释放按键
            note1_en <= 1'b0;
            note2_en <= 1'b0;
            note3_en <= 1'b0;
            note_count <= 2'd0;
        end
    end

endmodule

// ============================================================================
// 6. 频率表模块
// ============================================================================
module freq_table (
    input wire [4:0] note_code,
    output reg [15:0] note_freq
);

    // 频率表：C4-B5 (261.63Hz - 987.77Hz)
    // 存储分频系数，用于50MHz时钟
    always @(*) begin
        case (note_code)
            // 中音C4-B4
            5'd0:  note_freq = 16'd262;   // C4  (261.63Hz)
            5'd1:  note_freq = 16'd277;   // C#4 (277.18Hz)
            5'd2:  note_freq = 16'd294;   // D4  (293.66Hz)
            5'd3:  note_freq = 16'd311;   // D#4 (311.13Hz)
            5'd4:  note_freq = 16'd330;   // E4  (329.63Hz)
            5'd5:  note_freq = 16'd349;   // F4  (349.23Hz)
            5'd6:  note_freq = 16'd370;   // F#4 (369.99Hz)
            5'd7:  note_freq = 16'd392;   // G4  (392.00Hz)
            5'd8:  note_freq = 16'd415;   // G#4 (415.30Hz)
            5'd9:  note_freq = 16'd440;   // A4  (440.00Hz)
            5'd10: note_freq = 16'd466;   // A#4 (466.16Hz)
            5'd11: note_freq = 16'd494;   // B4  (493.88Hz)
            // 高音C5-B5
            5'd12: note_freq = 16'd523;   // C5  (523.25Hz)
            5'd13: note_freq = 16'd554;   // C#5
            5'd14: note_freq = 16'd587;   // D5
            5'd15: note_freq = 16'd622;   // D#5
            5'd16: note_freq = 16'd659;   // E5
            5'd17: note_freq = 16'd698;   // F5
            5'd18: note_freq = 16'd740;   // F#5
            5'd19: note_freq = 16'd784;   // G5
            5'd20: note_freq = 16'd831;   // G#5
            5'd21: note_freq = 16'd880;   // A5
            5'd22: note_freq = 16'd932;   // A#5
            5'd23: note_freq = 16'd988;   // B5
            default: note_freq = 16'd0;
        endcase
    end

endmodule

// ============================================================================
// 7. PWM生成器（用于蜂鸣器）
// ============================================================================
module pwm_generator (
    input wire clk,               // 50MHz
    input wire rst_n,
    input wire [15:0] freq,       // 目标频率
    input wire enable,
    input wire [7:0] duty_cycle,  // 占空比 0-255
    output reg pwm_out
);

    reg [31:0] phase_acc;
    reg [31:0] phase_inc;
    
    // 相位累加器方式生成PWM
    // phase_inc = (freq * 2^32) / clk_freq
    always @(*) begin
        phase_inc = (freq * 32'd85899346) >> 10;  // 简化计算
    end
    
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            phase_acc <= 32'd0;
            pwm_out <= 1'b0;
        end else if (enable) begin
            phase_acc <= phase_acc + phase_inc;
            pwm_out <= (phase_acc[31:24] < duty_cycle) ? 1'b1 : 1'b0;
        end else begin
            phase_acc <= 32'd0;
            pwm_out <= 1'b0;
        end
    end

endmodule

// ============================================================================
// 8. DDS波形生成器（用于扬声器，高质量音频）
// ============================================================================
module dds_generator (
    input wire clk,               // 50MHz
    input wire rst_n,
    input wire [15:0] freq,       // 目标频率
    input wire enable,
    output reg [15:0] wave_out    // 16位音频输出
);

    reg [31:0] phase_acc;
    wire [31:0] phase_inc;
    wire [7:0] sin_addr;
    wire [15:0] sin_data;
    
    // 计算相位增量
    assign phase_inc = (freq * 32'd85899346) >> 10;
    assign sin_addr = phase_acc[31:24];
    
    // 相位累加
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            phase_acc <= 32'd0;
        end else if (enable) begin
            phase_acc <= phase_acc + phase_inc;
        end else begin
            phase_acc <= 32'd0;
        end
    end
    
    // 正弦查找表
    sine_lut u_sine_lut (
        .addr(sin_addr),
        .data(sin_data)
    );
    
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            wave_out <= 16'd0;
        end else if (enable) begin
            wave_out <= sin_data;
        end else begin
            wave_out <= 16'd0;
        end
    end

endmodule

// ============================================================================
// 9. 正弦查找表（256点）
// ============================================================================
module sine_lut (
    input wire [7:0] addr,
    output reg [15:0] data
);

    always @(*) begin
        case (addr[7:4])
            4'd0:  data = 16'd32768 + (addr[3:0] * 16'd5040);
            4'd1:  data = 16'd32768 + (16'd15 - addr[3:0]) * 16'd5040;
            4'd2:  data = 16'd32768 + (16'd15 - addr[3:0]) * 16'd5040;
            4'd3:  data = 16'd32768 + (addr[3:0] * 16'd5040);
            4'd4:  data = 16'd32768 - (addr[3:0] * 16'd5040);
            4'd5:  data = 16'd32768 - (16'd15 - addr[3:0]) * 16'd5040;
            4'd6:  data = 16'd32768 - (16'd15 - addr[3:0]) * 16'd5040;
            4'd7:  data = 16'd32768 - (addr[3:0] * 16'd5040);
            4'd8:  data = 16'd32768 - (addr[3:0] * 16'd5040);
            4'd9:  data = 16'd32768 - (16'd15 - addr[3:0]) * 16'd5040;
            4'd10: data = 16'd32768 - (16'd15 - addr[3:0]) * 16'd5040;
            4'd11: data = 16'd32768 - (addr[3:0] * 16'd5040);
            4'd12: data = 16'd32768 + (addr[3:0] * 16'd5040);
            4'd13: data = 16'd32768 + (16'd15 - addr[3:0]) * 16'd5040;
            4'd14: data = 16'd32768 + (16'd15 - addr[3:0]) * 16'd5040;
            4'd15: data = 16'd32768 + (addr[3:0] * 16'd5040);
        endcase
    end

endmodule

// ============================================================================
// 10. 包络发生器（ADSR）
// ============================================================================
module envelope_generator (
    input wire clk,
    input wire rst_n,
    input wire note_on,           // 音符触发
    input reg [15:0] audio_in,
    output reg [15:0] audio_out
);

    reg [1:0] state;              // 0=idle, 1=attack, 2=decay, 3=sustain, 4=release
    reg [15:0] envelope;
    reg [15:0] counter;
    
    parameter ATTACK_TIME = 16'd1000;
    parameter DECAY_TIME = 16'd2000;
    parameter SUSTAIN_LEVEL = 16'd40000;
    parameter RELEASE_TIME = 16'd3000;
    
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state <= 2'd0;
            envelope <= 16'd0;
            counter <= 16'd0;
        end else begin
            case (state)
                2'd0: begin  // Idle
                    if (note_on) begin
                        state <= 2'd1;
                        counter <= 16'd0;
                    end
                    envelope <= 16'd0;
                end
                
                2'd1: begin  // Attack
                    if (counter < ATTACK_TIME) begin
                        counter <= counter + 1'b1;
                        envelope <= (counter * 16'd65535) / ATTACK_TIME;
                    end else begin
                        state <= 2'd2;
                        counter <= 16'd0;
                    end
                end
                
                2'd2: begin  // Decay
                    if (counter < DECAY_TIME) begin
                        counter <= counter + 1'b1;
                        envelope <= 16'd65535 - ((counter * (16'd65535 - SUSTAIN_LEVEL)) / DECAY_TIME);
                    end else begin
                        state <= 2'd3;
                    end
                end
                
                2'd3: begin  // Sustain
                    envelope <= SUSTAIN_LEVEL;
                    if (!note_on) begin
                        state <= 2'd0;
                        counter <= 16'd0;
                    end
                end
                
                default: state <= 2'd0;
            endcase
        end
    end
    
    // 应用包络
    always @(posedge clk) begin
        audio_out <= (audio_in * envelope) >> 16;
    end

endmodule

// ============================================================================
// 11. 和弦混音器
// ============================================================================
module chord_mixer (
    input wire clk,
    input wire rst_n,
    input wire [15:0] audio1,
    input wire [15:0] audio2,
    input wire [15:0] audio3,
    input wire en1,
    input wire en2,
    input wire en3,
    output reg [15:0] mixed_out
);

    reg [17:0] sum;
    reg [2:0] active_count;
    
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            sum <= 18'd0;
            active_count <= 3'd0;
            mixed_out <= 16'd0;
        end else begin
            // 计算活动音符数量
            active_count <= en1 + en2 + en3;
            
            // 求和
            sum <= (en1 ? audio1 : 16'd0) + 
                   (en2 ? audio2 : 16'd0) + 
                   (en3 ? audio3 : 16'd0);
            
            // 平均并防止溢出
            if (active_count > 0) begin
                mixed_out <= sum / active_count;
            end else begin
                mixed_out <= 16'd0;
            end
        end
    end

endmodule

// ============================================================================
// 12. 音量控制模块
// ============================================================================
module volume_control (
    input wire clk,
    input wire rst_n,
    input wire [15:0] audio_in,
    input wire [3:0] volume_level,    // 0-15
    output reg [15:0] audio_out
);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            audio_out <= 16'd0;
        end else begin
            // 音量调节：使用移位实现快速乘法
            case (volume_level)
                4'd0:  audio_out <= 16'd0;
                4'd1:  audio_out <= audio_in >> 4;
                4'd2:  audio_out <= audio_in >> 3;
                4'd3:  audio_out <= (audio_in >> 3) + (audio_in >> 4);
                4'd4:  audio_out <= audio_in >> 2;
                4'd5:  audio_out <= (audio_in >> 2) + (audio_in >> 4);
                4'd6:  audio_out <= (audio_in >> 2) + (audio_in >> 3);
                4'd7:  audio_out <= (audio_in >> 1) - (audio_in >> 4);
                4'd8:  audio_out <= audio_in >> 1;
                4'd9:  audio_out <= (audio_in >> 1) + (audio_in >> 3);
                4'd10: audio_out <= (audio_in >> 1) + (audio_in >> 2);
                4'd11: audio_out <= audio_in - (audio_in >> 3);
                4'd12: audio_out <= audio_in - (audio_in >> 4);
                4'd13: audio_out <= audio_in;
                4'd14: audio_out <= audio_in + (audio_in >> 3);
                4'd15: audio_out <= audio_in + (audio_in >> 2);
            endcase
        end
    end

endmodule

// ============================================================================
// 13. UART接收模块
// ============================================================================
module uart_rx_module (
    input wire clk,               // 50MHz
    input wire rst_n,
    input wire rx,
    output reg [7:0] data_out,
    output reg data_valid
);

    parameter BAUD_RATE = 115200;
    parameter CLK_FREQ = 50000000;
    parameter BAUD_CNT = CLK_FREQ / BAUD_RATE;
    
    reg [15:0] baud_cnt;
    reg [3:0] bit_cnt;
    reg [7:0] rx_data;
    reg rx_reg1, rx_reg2;
    reg rx_flag;
    
    // RX同步
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            rx_reg1 <= 1'b1;
            rx_reg2 <= 1'b1;
        end else begin
            rx_reg1 <= rx;
            rx_reg2 <= rx_reg1;
        end
    end
    
    // UART接收状态机
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            baud_cnt <= 16'd0;
            bit_cnt <= 4'd0;
            rx_data <= 8'd0;
            data_out <= 8'd0;
            data_valid <= 1'b0;
            rx_flag <= 1'b0;
        end else begin
            data_valid <= 1'b0;
            
            if (!rx_flag && !rx_reg2) begin  // 起始位检测
                rx_flag <= 1'b1;
                baud_cnt <= 16'd0;
                bit_cnt <= 4'd0;
            end else if (rx_flag) begin
                if (baud_cnt < BAUD_CNT - 1) begin
                    baud_cnt <= baud_cnt + 1'b1;
                end else begin
                    baud_cnt <= 16'd0;
                    
                    if (bit_cnt < 4'd8) begin
                        rx_data[bit_cnt] <= rx_reg2;
                        bit_cnt <= bit_cnt + 1'b1;
                    end else begin
                        rx_flag <= 1'b0;
                        data_out <= rx_data;
                        data_valid <= 1'b1;
                    end
                end
            end
        end
    end

endmodule

// ============================================================================
// 14. 自动演奏模块
// ============================================================================
module auto_play (
    input wire clk,
    input wire rst_n,
    input wire enable,
    input wire [7:0] uart_data,
    input wire uart_valid,
    output reg [4:0] note_out,
    output reg note_enable
);

    reg [7:0] note_buffer [0:255];
    reg [7:0] write_ptr;
    reg [7:0] read_ptr;
    reg [23:0] timer;
    reg playing;
    
    parameter NOTE_DURATION = 24'd25000000;  // 0.5秒 @ 50MHz
    
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            write_ptr <= 8'd0;
            read_ptr <= 8'd0;
            timer <= 24'd0;
            playing <= 1'b0;
            note_enable <= 1'b0;
        end else begin
            // 接收UART数据存入缓冲区
            if (uart_valid) begin
                note_buffer[write_ptr] <= uart_data;
                write_ptr <= write_ptr + 1'b1;
            end
            
            // 自动播放
            if (enable && (write_ptr != read_ptr)) begin
                if (!playing) begin
                    note_out <= note_buffer[read_ptr][4:0];
                    note_enable <= 1'b1;
                    playing <= 1'b1;
                    timer <= 24'd0;
                end else if (timer < NOTE_DURATION) begin
                    timer <= timer + 1'b1;
                end else begin
                    note_enable <= 1'b0;
                    playing <= 1'b0;
                    read_ptr <= read_ptr + 1'b1;
                end
            end else if (!enable) begin
                note_enable <= 1'b0;
                playing <= 1'b0;
                read_ptr <= 8'd0;
            end
        end
    end

endmodule

// ============================================================================
// 15. 录音回放模块
// ============================================================================
module record_playback (
    input wire clk,
    input wire rst_n,
    input wire record_en,
    input wire playback_en,
    input wire [4:0] note_in,
    input wire note_in_valid,
    output reg [4:0] note_out,
    output reg note_out_valid
);

    reg [7:0] note_memory [0:255];
    reg [7:0] record_ptr;
    reg [7:0] playback_ptr;
    reg [23:0] timer;
    
    parameter NOTE_DURATION = 24'd25000000;
    
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            record_ptr <= 8'd0;
            playback_ptr <= 8'd0;
            timer <= 24'd0;
            note_out_valid <= 1'b0;
        end else begin
            // 录音模式
            if (record_en && note_in_valid) begin
                note_memory[record_ptr] <= {3'd0, note_in};
                record_ptr <= record_ptr + 1'b1;
                playback_ptr <= 8'd0;
            end
            
            // 回放模式
            if (playback_en) begin
                if (timer < NOTE_DURATION) begin
                    timer <= timer + 1'b1;
                    if (timer == 24'd0 && playback_ptr < record_ptr) begin
                        note_out <= note_memory[playback_ptr][4:0];
                        note_out_valid <= 1'b1;
                    end
                end else begin
                    timer <= 24'd0;
                    note_out_valid <= 1'b0;
                    playback_ptr <= playback_ptr + 1'b1;
                    if (playback_ptr >= record_ptr) begin
                        playback_ptr <= 8'd0;
                    end
                end
            end else begin
                note_out_valid <= 1'b0;
                timer <= 24'd0;
            end
        end
    end

endmodule

// ============================================================================
// 16. 数码管显示模块
// ============================================================================
module seg_display (
    input wire clk,               // 1kHz
    input wire rst_n,
    input wire [4:0] note_code,
    input wire [3:0] volume,
    input wire mode,
    output reg [5:0] seg_sel,
    output reg [7:0] seg_data
);

    reg [2:0] scan_cnt;
    reg [3:0] digit;
    
    // 数码管扫描
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            scan_cnt <= 3'd0;
        end else begin
            scan_cnt <= (scan_cnt == 3'd5) ? 3'd0 : scan_cnt + 1'b1;
        end
    end
    
    // 位选信号
    always @(*) begin
        case (scan_cnt)
            3'd0: seg_sel = 6'b111110;
            3'd1: seg_sel = 6'b111101;
            3'd2: seg_sel = 6'b111011;
            3'd3: seg_sel = 6'b110111;
            3'd4: seg_sel = 6'b101111;
            3'd5: seg_sel = 6'b011111;
            default: seg_sel = 6'b111111;
        endcase
    end
    
    // 显示数据选择
    always @(*) begin
        case (scan_cnt)
            3'd0: digit = note_code % 12;      // 音符
            3'd1: digit = note_code / 12;      // 八度
            3'd2: digit = 4'd15;               // 空
            3'd3: digit = volume;              // 音量
            3'd4: digit = mode ? 4'd10 : 4'd11;// A/M模式
            3'd5: digit = 4'd15;               // 空
            default: digit = 4'd15;
        endcase
    end
    
    // 7段译码
    always @(*) begin
        case (digit)
            4'd0:  seg_data = 8'b11000000;  // 0
            4'd1:  seg_data = 8'b11111001;  // 1
            4'd2:  seg_data = 8'b10100100;  // 2
            4'd3:  seg_data = 8'b10110000;  // 3
            4'd4:  seg_data = 8'b10011001;  // 4
            4'd5:  seg_data = 8'b10010010;  // 5
            4'd6:  seg_data = 8'b10000010;  // 6
            4'd7:  seg_data = 8'b11111000;  // 7
            4'd8:  seg_data = 8'b10000000;  // 8
            4'd9:  seg_data = 8'b10010000;  // 9
            4'd10: seg_data = 8'b10001000;  // A
            4'd11: seg_data = 8'b11000111;  // M
            default: seg_data = 8'b11111111; // 空
        endcase
    end

endmodule

// ============================================================================
// 17. LED指示模块
// ============================================================================
module led_indicator (
    input wire clk,               // 1kHz
    input wire rst_n,
    input wire [4:0] note_code,
    input wire key_pressed,
    output reg [3:0] led
);

    reg [9:0] blink_cnt;
    
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            led <= 4'b0000;
            blink_cnt <= 10'd0;
        end else begin
            if (key_pressed) begin
                // 根据音符显示LED
                led[0] <= (note_code[1:0] == 2'b00);
                led[1] <= (note_code[1:0] == 2'b01);
                led[2] <= (note_code[1:0] == 2'b10);
                led[3] <= (note_code[1:0] == 2'b11);
                
                // 闪烁效果
                blink_cnt <= blink_cnt + 1'b1;
                if (blink_cnt[9]) begin
                    led <= ~led;
                end
            end else begin
                led <= 4'b0000;
                blink_cnt <= 10'd0;
            end
        end
    end

endmodule