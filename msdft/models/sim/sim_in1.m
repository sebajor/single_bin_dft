len = 4096;
t = [0:1:len-1];
N = 256;
k = 50;
phi = deg2rad(200);

sig = 0.8*cos(2*pi*k*t/N+phi);

data_in = zeros(len,2);
data_in(:,1) = t;
data_in(:,2) = sig;

%software fft
spect = fft(sig(1:256));

fprintf('Magnitude: %7.4f', 20*log10(abs(spect(k+1))));
fprintf('\n');
fprintf('Phase: %7.4f', rad2deg(angle(spect(k+1))));
fprintf('\n');

subplot(2,1,1);
plot(20*log10(abs(spect(1:N/2))), '*-');
title('Power Spectrum');

subplot(2,1,2);
plot(rad2deg(angle(spect(1:N/2))), '*-');
title('Phase');