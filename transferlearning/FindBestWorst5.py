import os
import subprocess

validFolder = 'sampleImage\valid'

img = [[None for i in range(2)] for j in range(196*5)]
idx = 0
with open('classify_result.txt', 'a') as f:
    for classes in range(1,197):
        c = str(classes).zfill(4)
        imgfolder = os.path.join(validFolder, c)
        imglist = os.listdir(imgfolder)
        print("========== writing class " + str(classes) + " ===========")
        for k in range(min(5,len(imglist))):
            imgName = os.path.join(imgfolder, imglist[k])
            labeling = 'python label_image.py --graph=/model/resnet152_twin_4000/output_graph.pb --labels=/model/resnet152_twingray_4000/output_labels.txt --input_layer=Placeholder --output_layer=final_result --image=' + imgName
            #print(labeling)
            #r = os.popen(labeling)
            r = subprocess.check_output(labeling).decode("utf-8")
            line = r.split('\r\n')
            img[idx][0] = imglist[k]
            for i in range(5):
                [c_predict, prob] = line[i].split(' ')
                if c == c_predict:
                    img[idx][1] = prob
            if img[idx][1]==None: img[idx][1] = prob
                
            
            f.write("%s %s\n" %(imglist[k],img[idx][1]))
            idx+=1
print(img)

        

    
