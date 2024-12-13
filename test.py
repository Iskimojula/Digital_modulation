import numpy as np
import matplotlib.pyplot as plt

# 定义一个简单信号
x = np.linspace(-10, 10, 100)
y = np.sin(x)

# 计算傅里叶变换
y_fft = np.fft.fft(y)

# 移动零频分量到中心
y_fft_shifted = np.fft.fftshift(y_fft)

# 可视化
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.title("原始傅里叶变换")
plt.plot(np.abs(y_fft))

plt.subplot(1, 2, 2)
plt.title("移位后的傅里叶变换")
plt.plot(np.abs(y_fft_shifted))
plt.show()
