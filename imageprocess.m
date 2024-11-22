function uchannel = imageprocess(imgsrc,PSF,type)
% imageprocess.m
% image process
% imgsrc = imread('sample_rgb_653.jpg');
% type = 'rgb';
figure;
colorindex = ["red","green" ,"blue"];
if strcmp(type,'gray')
    redChannel =  imgsrc(:,:,1);
    greenChannel =  imgsrc(:,:,1);
    blueChannel =  imgsrc(:,:,1);
elseif strcmp(type,'rgb')
    uchannel = zeros(size(imgsrc,1),size(imgsrc,2),size(imgsrc,3),'uint8');
    for channel = 1: size(imgsrc,3)
        [dchannel,uchannel(:,:,channel)] = singlechannelprocess(imgsrc(:,:,channel),PSF);

        % 显示颜色通道
        subplot(2, 3, channel);
        imshow(dchannel,[]);
        titleStr = "channel_ "+ colorindex(channel);
        title(titleStr);
    end

    % 显示合并图像
    subplot(2, 3, 4);
    imshow(uchannel,[]);
    title('PSF处理图像');
end

% 显示原图像
subplot(2, 3, 5);
imshow(imgsrc,[]);
title('原图像');

%灰度图
if 1
imagePath2 = 'sample_gray653.jpg';
img2= (imread(imagePath2));
result2 = conv2(double(img2), double(PSF), 'same');
% subplot(1, 3, 3);
subplot(2, 3, 6);
imshow(result2, []);
title('灰度图');
end
