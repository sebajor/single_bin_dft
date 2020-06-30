import numpy as np
import os
import matplotlib.pyplot as plt

pow_avg = np.zeros(57)
pow_std = np.zeros(57)
ang_avg = np.zeros(57)
ang_std = np.zeros(57)

for i in range(57):
    os.chdir(str(i+4))
    pow_val = np.loadtxt('pow_avg')
    ang_val = np.loadtxt('ang_avg')
    pow_avg[i] = np.mean(pow_val[:20])
    pow_std[i] = np.std(pow_val[:20])
    ang_avg[i] = np.mean(ang_val[:20])
    ang_std[i] = np.std(ang_val[:20])
    os.chdir('..')    


att_vals = np.linspace(4, 60, 57)

fig = plt.figure()
ax1 = fig.add_subplot(221)
ax1.set_title('Average power difference')
ax1.set_ylabel('avg pow diff dB')
#ax1.set_xlabel('dB')
ax1.grid()
ax1.plot(att_vals, pow_avg, '-*')    

ax2 = fig.add_subplot(222)
ax2.set_title('Standar deviation power difference')
ax2.set_ylabel('std pow diff dB')
#ax2.set_xlabel('db')
ax2.grid()
ax2.plot(att_vals, pow_std, '-*')    

ax3 = fig.add_subplot(223)
ax3.set_title('Average phase difference')
ax3.set_ylabel('avg phase diff ['+u'\xb0'+']')
ax3.set_xlabel('Input power diff [dB]')
ax3.grid()
ax3.plot(att_vals, ang_avg, '-*')
    
ax4 = fig.add_subplot(224)
ax4.set_title('Standar deviation phase difference')
ax4.set_ylabel('std phase diff ['+u'\xb0'+']')
ax4.set_xlabel('Input power diff[dB]')
ax4.grid()
ax4.plot(att_vals, ang_std, '-*')
plt.show()

