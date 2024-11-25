function resimg = imageprocess(imgsrc,PSF,type)
% imageprocess.m
% image process
% imgsrc = imread('sample_rgb_653.jpg');
% type = 'rgb';
figure('Position', [100, 100,1200, 600]);

centerrow = (size(imgsrc,2)+ 1)/2;
centercol = (size(imgsrc,1)+ 1)/2;
maskradius = 100;
transition_width = 20;

if strcmp(type,'gray')

[~,resimg,resimg_nomask] = singlechannelmodulation(imgsrc,PSF,centerrow,centercol,maskradius,transition_width);

elseif strcmp(type,'rgb')
    resimg = zeros(size(imgsrc,1),size(imgsrc,2),size(imgsrc,3),'uint8');
    resimg_nomask = resimg;
    for channel = 1: size(imgsrc,3)
        [~,resimg(:,:,channel),resimg_nomask(:,:,channel)] = singlechannelmodulation(imgsrc(:,:,channel),PSF,centerrow,centercol,maskradius,transition_width);
    end
end

% 显示合并图像
subplot(2, 3, 1);
imshow(resimg_nomask,[]);
title('像差图像');

% 显示合并图像
subplot(2, 3, 2);
imshow(resimg,[]);
title('数字调制图像');

% 显示原图像
subplot(2, 3, 3);
imshow(imgsrc,[]);
title('原图像');


