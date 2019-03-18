%%% Reflect img

%%%

imgFolderMaster = 'sampleImage\train';
targetFolder = 'sampleImage\train_reflect';

folders = dir(imgFolderMaster);

for idx = 3: length(folders)
    className = folders(idx).name
    imgFolder = [imgFolderMaster,'\',className];
    imgFiles = dir(imgFolder);
    density = zeros(length(imgFiles)-2, 256*3);
    targetSubFolder = [targetFolder,'\',className];
    mkdir(targetSubFolder);
    
    for imgidx = 3:length(imgFiles)
        
        imgName = [imgFolder, '\', imgFiles(imgidx).name];
        img = imread(imgName);
        [m,n,d] = size(img);
        
        img_reflect = img(:,n:-1:1,:);
        saveFile = [targetSubFolder, '\r', imgFiles(imgidx).name];
        
        imwrite(img_reflect,saveFile);
    end
    

end


