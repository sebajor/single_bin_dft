function msdft_init(input_bitsize, fft_len, bin_range, ... 
    twid_bitsize, out_bitsize)
    din = xInport('din');
    sync = xInport('sync');
    rst = xInport('rst');
    twidd_im = xInport('im_twidd');
    twidd_re = xInport('re_twidd');
    msdft_loc = xInport('msdft_loc');
    mem_addr = xInport('mem_addr');
    
    sync_out = xOutport('sync_out');
    
    delay = xBlock('sys_lib/Delay',struct('latency', 2^(fft_len)+7),{sync},{sync_out});
    
    
    for i=1:length(bin_range)
        compare = xSignal;
        const_sig = xSignal;
        const =  xBlock('sys_lib/Constant', struct('const', i-1),{},{const_sig});
        rel = xBlock('sys_lib/Relational',struct(), {msdft_loc, const_sig}, {compare});
        
        out = xOutport(strcat('dout',num2str(i)));
        xBlock('sys_lib/msdft', struct('in_bit', input_bitsize,'N', fft_len,...
                'init_twidd', bin_range(i), 'twidd_bit', twid_bitsize, ...
                'out_bit', out_bitsize), {din, sync, rst, twidd_im, twidd_re, ...
                compare, mem_addr}, {out});
    end   
end