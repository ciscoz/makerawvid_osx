% Make video images from 3 views
% Originally made for Will's JF talk
% Feb 2010
function makevideo(frame_start,frame_end,bgpath,seqpath)

close all; clc

cd /Users/cisco/Documents/MATLAB
out_path='/Users/cisco/Desktop/';

if nargin < 4
	quit;
    [bgfileName,bgpathName] = uigetfile({'*.bmp';'*.tif'},'Click on any background image in video sequence','/Users/cisco/Documents/MATLAB/NEW/data');
    dir_str = findstr(filesep,bgpathName); 
    [foo,pathName] = uigetfile({'*.bmp';'*.tif'},'Click on any image in video sequence',bgpathName(1:dir_str(end-1)));    
else
    dir_str = findstr(filesep,bgpath); 
    bgfileName=bgpath(dir_str(end)+1:end);
    bgpathName=bgpath(1:dir_str(end));
    dir_str = findstr(filesep,bgpath); 
    pathName=seqpath(1:dir_str(end));   
end

bg1=imread([bgpathName bgfileName]);
bg1=imadjust(bg1);
bgpathName(end-10) = '2';
bg2=imread([bgpathName bgfileName]);
bg2=imadjust(bg2);
bgpathName(end-10) = '3';
bg3=imread([bgpathName bgfileName]);
bg3=imadjust(bg3);

seq_num = findstr('S',pathName);
seq_num = pathName(seq_num:end-1);

adjustment = true;
saving = true;
frames = [frame_start:frame_end];


if saving == true
    cc = clock;
    cc = num2str(cc(2:end-1),'%02d');
    out_dir = [out_path cc(find(~isspace(cc))) '_' seq_num];    
    if ~exist(out_dir,'dir')
        mkdir(out_dir)
    end
end

noiseTol=[1 8 20];
for ii = frames
	f = figure('Position',[0 0 1200 350],'PaperType','B','Visible','off');
    frameName = [num2str(ii,'%06d') '.bmp'];
    figure(f)
    %Hack!
    pathName(end-10) = '1';
    raw1=imread([pathName frameName]);
    if adjustment == true
        cam1=imadjust(raw1);            
        cam1=imsubtract(bg1,cam1);
        cam1=imsubtract(cam1,noiseTol(1));
        %cam1=immultiply(cam1,256);
        %cam1=imcomplement(cam1);
        %cam1=imadd(raw1,cam1);
        %cam1=imcomplement(cam1);        
        %cam1=im2bw(immultiply(cam1,256),0.1); % Thresholds to get a pure white fly                   
    end
    imagesc(cam1); hold on; colormap(gray)
    ax1 = gca;
    set(ax1,'YDir','reverse','visible','off','Position',[-0.2925 0 1 1],'clim',[0 200]);
    axis square

    mpos = get(ax1,'position');
    figure(f)
    %Hack!
    pathName(end-10) = '2';
    cam2=imread([pathName frameName]);
    if adjustment == true
        cam2=imadjust(cam2);            
        cam2=imsubtract(bg2,cam2);
        cam2=imsubtract(cam2,noiseTol(2));        
        %cam2=imcomplement(cam2);        
        %cam2=immultiply(cam2,20);             
    end
    ax2 = axes;
    imagesc(cam2); colormap(gray)
    set(ax2,'YDir','reverse','visible','off','Position',[0.0 0 1 1],'clim',[0 200]);
    axis square

    impos = get(ax2,'position');
    figure(f)    
    %Hack!
    pathName(end-10) = '3';
    cam3=imread([pathName frameName]);    
    if adjustment == true
        cam3=imadjust(cam3);                    
        cam3=imsubtract(bg3,cam3); 
        cam3=imsubtract(cam3,noiseTol(3));                
        %cam3=imcomplement(cam3);        
        %cam3=immultiply(cam3,20);     
    end
    ax3 = axes;
    imagesc(cam3); colormap(gray)
    set(ax3,'YDir','reverse','visible','off','Position',[0.2925 0 1 1],'clim',[0 200]);
    axis square
    set(gcf,'PaperPositionMode','auto')
    if saving == true
        print('-dtiff','-r300',[out_dir '/' num2str(ii,'%06d') '.tif']);    
    end
	close(f)
end
disp(['Done with iteration: ' num2str(frame_start) ' to ' num2str(frame_end)])
return
