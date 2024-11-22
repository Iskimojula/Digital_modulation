function [channelimg_double,channelimg_uint8] = singlechannelprocess(channelimg,channelpsf)
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here
channelimg_double = conv2(double(channelimg), double(channelpsf), 'same');

% 使用 mat2gray 将图像缩放到 [0, 1]
normalizedImage = mat2gray(channelimg_double);

% 将 normalizedImage 转换为 uint8 类型
channelimg_uint8 = uint8(normalizedImage * 255); % 线性缩放到 0-255 范围
end