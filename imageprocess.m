function resimg = imageprocess(imgsrc,PSF,type)
% imageprocess.m
% image process
% imgsrc = imread('sample_rgb_653.jpg');
% type = 'rgb';
figure;

centerrow = (size(imgsrc,2)+ 1)/2;
centercol = (size(imgsrc,1)+ 1)/2;
maskradius = 100;
transition_width = 20;

if strcmp(type,'gray')

[~,resimg] = singlechannelmodulation(imgsrc,PSF,centerrow,centercol,maskradius,transition_width);

elseif strcmp(type,'rgb')
    resimg = zeros(size(imgsrc,1),size(imgsrc,2),size(imgsrc,3),'uint8');
    for channel = 1: size(imgsrc,3)
        [~,resimg(:,:,channel)] = singlechannelmodulation(imgsrc(:,:,channel),PSF,centerrow,centercol,maskradius,transition_width);
    end
end

% 显示合并图像
subplot(1, 2, 1);
imshow(resimg,[]);
title('PSF处理图像');

% 显示原图像
subplot(1, 2, 2);
imshow(imgsrc,[]);
title('原图像');


