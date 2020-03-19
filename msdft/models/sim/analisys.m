%analisys data taken by msdft

N = 256;
delay = 8; %im not 100 sure that it is, but is enough
fft_mag = 60.2417;                
fft_ang = 48.5;


re1 = re_part1.data();
im1 = im_part1.data();
re2 = re_part2.data();
im2 = im_part2.data();
data1 = re1+1j*im1;
data2 = re2+1j*im2;

mag1 = 20*log10(abs(data1));
mag2 = 20*log10(abs(data2));
ang1 = rad2deg(angle(data1));
ang2 = rad2deg(angle(data2));


subplot(211)
plot(mag1-mag2, '*-');
title('Relative magnitude');
ylabel('[dB]')
line = fft_mag*ones(length(mag1));
hold on
plot(line, 'r')

subplot(212)
plot(ang1-ang2)
title('Relative phase')
ylabel('deg')
line = fft_ang*ones(length(mag1));
hold on 
plot(line, 'r')


%calculate statistics


mag_avg = mean(mag1(N+delay:end)-mag2(N+delay:end));
mag_std = std(mag1(N+delay:end)-mag2(N+delay:end));
ang_avg = mean(ang1(N+delay:end)-ang2(N+delay:end));
ang_std = std(ang1(N+delay:end)-ang2(N+delay:end));


fprintf('Avg magnitude: %7.4f', mag_avg);
fprintf('\n');
fprintf('Std magnitude: %7.4f', mag_std);
fprintf('\n');
fprintf('Avg phase: %7.4f', ang_avg);
fprintf('\n');
fprintf('Std phase: %7.4f', ang_std);









