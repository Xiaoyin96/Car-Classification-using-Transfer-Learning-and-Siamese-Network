%%% RGB stat
%%% Youbin Mo
%%% 2019/03/02
%%% Split RGB from image and make a histogram of RGB

imgFolderMaster = 'sampleImage\train';
csvFolder = '\train_color_density';

% imgFolderMaster = 'sampleImage\valid';
% csvFolder = '\valid_color_density';

folders = dir(imgFolderMaster);

for idx = 3: length(folders)
    className = folders(idx).name
    imgFolder = [imgFolderMaster,'\',className];
    imgFiles = dir(imgFolder);
    density = zeros(length(imgFiles)-2, 256*3);
    for imgidx = 3:length(imgFiles)
        
        imgName = [imgFolder, '\', imgFiles(imgidx).name];
        img = imread(imgName);
        [m,n,d] = size(img);
        if d == 1
            j = 1;
            k = 1;
        else
            j = 2;
            k = 3;
        end
        img_red = reshape(img(:,:,1), [1, m*n]);
        img_green = reshape(img(:,:,j), [1, m*n]);
        img_blue = reshape(img(:,:,k), [1, m*n]);
       
        
        X = 0:255;
        N_red = hist(img_red, X);
        N_green = hist(img_green, X);
        N_blue = hist(img_blue, X);
        density(imgidx-2,:) = [N_red, N_green, N_blue]/(m*n);
    end
    
    csvFile = [csvFolder,'\',className,'.csv'];
    csvwrite(csvFile,density)
    
    d = sum(density,1);
    figure()
    plot(d)
end





