len = 4096;
t = [0:1:len-1];
N = 256;
k = 50;
phi_1 = deg2rad(72);
phi_2 = deg2rad(24);

sig1 = 0.9*cos(2*pi*k*t/N+phi_1);       %%in the twidd
sig2 = 0.9/1024*cos(2*pi*k*t/N+phi_2);  %%in the twidd

%sig1 = 0.9*cos(2*pi*(k+0.5)*t/N+phi_1);       %%in the middle twidd
%sig2 = 0.9/1024*cos(2*pi*(k+0.5)*t/N+phi_2);  %%in the middle twidd


%sig1 = awgn(sig1, 80);     %add noise
%sig2 = awgn(sig2, 80);     %add noise


data_in1 = zeros(len,2);
data_in1(:,1) = t;
data_in1(:,2) = sig1;

data_in2 = zeros(len,2);
data_in2(:,1) = t;
data_in2(:,2) = sig2;


%software fft
spect_1 = fft(sig1(1:256));
spect_2 = fft(sig2(1:256));

fprintf('Magnitude: %7.4f', 20*(log10(abs(spect_1(k+1)))-log10(abs(spect_2(k+1)))));
fprintf('\n');
fprintf('Phase: %7.4f', (rad2deg(angle(spect_1(k+1)))-rad2deg(angle(spect_2(k+1)))));
fprintf('\n');

figure
subplot(2,1,1);
plot(20*log10(abs(spect_1(1:N/2))), '*-');
title('Power Spectrum1');

subplot(2,1,2);
plot(rad2deg(angle(spect_1(1:N/2))), '*-');
title('Phase1');


figure
subplot(2,1,1);
plot(20*log10(abs(spect_2(1:N/2))), '*-');
title('Power Spectrum2');

subplot(2,1,2);
plot(rad2deg(angle(spect_2(1:N/2))), '*-');
title('Phase2');


