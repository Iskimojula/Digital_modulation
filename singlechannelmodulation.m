function [resimg_double,resimg_uint8] = singlechannelmodulation(singlechannel,PSF,centerrow,centercol,maskradius,transition_width)
%UNTITLED5 Summary of this function goes here
%   Detailed explanation goes here
    [~,uchannel] = singlechannelprocess(singlechannel,PSF);

    %合并通道
    mask = zeros(size(singlechannel,1),size(singlechannel,2),'double');
     for row = 1: size(singlechannel,1)
        for col = 1: size(singlechannel,2)
            dist = sqrt((row - centercol)^2 + (col - centerrow)^2);
            if dist < maskradius
                mask(row, col) = 1;
            elseif dist < (maskradius + transition_width)
                mask(row, col) = 1 - (dist - maskradius) / transition_width;
            end
        end
     end
    
    % 将卷积结果与原图像结合
    resimg_double = double(uchannel) .* mask + double(singlechannel) .* (1 - mask);

    resimg_double(resimg_double>=255) = 255;
    
    resimg_uint8 = uint8(resimg_double); % 线性缩放到 0-255 范围
end