function ChangeImgResolution(img_dir)
    pic_files_info = dir([img_dir '/*.jpg']);
    num_pics = length(pic_files_info);
    pic_dat = zeros(num_pics, 120000);
    for pic_file_info_idx = 1: length(pic_files_info)
        raw_img = reshape(imresize(imread(...
            [pic_files_info(pic_file_info_idx).folder ...
             '/' pic_files_info(pic_file_info_idx).name]), [200, 200]), 1, []);
        
        if size(raw_img, 2) == 40000
            raw_img = cat(2, raw_img, raw_img, raw_img);            
        end
        
        pic_dat(pic_file_info_idx, :) = raw_img;
    end
    csvwrite('img.csv', pic_dat);
end

