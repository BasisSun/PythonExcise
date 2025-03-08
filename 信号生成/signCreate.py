import numpy as np
import matplotlib.pyplot as plt

# 设置频率、采样率和时长
frequency = 5000.0
sampling_rate = 100.0
duration = 2.0

# 生成时域采样点的时间序列
time = np.arange(0, duration, 1/sampling_rate)

# 计算正弦波的振幅
amplitude = np.sin(2*np.pi*frequency*time)

# 绘制图像
plt.plot(time, amplitude)
plt.title('Sine Wave')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.show()