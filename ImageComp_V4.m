% Code Written by: Anurag Madan
% For: Orthofix

% The following is a bonus MATLAB script that was produced for image comparison and verification by UTDesign team 543, Team 'TAPP' during the 
% Fall 2017 and Spring 2018 Senior Design courses. 
% This script is called from the main Python function at the end of each test case loop. The script converts 2 images to double format, subtracts
% the 2 pixel by pixel, and then converts the difference image to black and white using a threshold, with white pixels being the areas where a 
% difference occurs. The script then breaks the difference image into a specified number of segments, and flags segments with more than a specified
% percentage of white (difference) pixels. If no such segments are found, the script logs that the images match, else it logs the images don't match.
% The code uses basic image functions like imread and im2double, which are part of the standard MATLAB package. 
% No additional packages should be needed.

f=fopen('C:\Users\utd\Desktop\dummyss.txt');		% This is the location of the two images to be compared. The locations are written in the 
                                                    % file in the python code.
line=fgetl(f);
A=imread(line);
line=fgetl(f);
B=imread(line);
[x1,y1]=size(A);
[x2,y2]=size(B);
sum=0;
count=0;
if x1~=x2 || y1~=y2
    disp('Image sizes dont match!');                % Checks if the sizes for the images are the same
    exit(code);
end
x=x1;
y=y1;
a=im2double(A);
b=im2double(B);
c=a-b;
for i=1:1:x
    for j=1:1:y
        c(i,j)=abs(c(i,j));
        if(c(i,j)<0.45)%0.23  max/3 0.33            % This is the threshold. the 0.45 was determined by trial and error. 
            c(i,j)=0;                               % If the difference is less than 0.45, the pixel is colored black, else it is colored white.
        else
            c(i,j)=1;
        end
        
    end
end
c=im2bw(c,0.0001);                                  % Actually converts the image to black and white. the 0.0001 is the threshold. Since the pixel
                                                    % values are actually 0 or 1, this threshold is not important.
segment=25;                                         % The image is broken into (segment^2) chunks. So in this case, 625 chunks.
success=zeros(segment);
x_segment=floor(x/segment);
y_segment=floor(y/(3*segment));                     % We divide by 3 because when we get the value for y, the image is RGB. After being converted
                                                    % to black and white, we lose the x3 factor. 
l=1;
flag=1;
for k=1:1:segment
    for l=1:1:segment
        for i=(k-1)*x_segment+1:1:k*x_segment
            for j=(l-1)*y_segment+1:1:l*y_segment
                d(i-((k-1)*x_segment),j-((l-1)*y_segment))=c(i,j);	% Gets the difference image for each segment. 
                if(c(i,j)==0)		
                    count=count+1;                                  % Counts the number of white pixels in each segment
                end
            end
            
        end
        success(k,l)=count/(x_segment*y_segment)*100;               % Calculates the percentage of white pixels to total (black + white) pixels.
        count=0;
        if(success(k,l)<90)                                     	% This is the success threshold. the 90 was determined by trial and error
            if(flag==1)
                disp('images dont match');
		result='images dont match';
                flag=0;                             % sets a flag to 0. This is used to display whether the images match or not
            end
            %figure
            %imshow(d)
            %exit(code);
        end
    end
    l=1;    
end
if(flag==1)
	disp('images match!');
	result='images match!';
end
t=datestr(now,'mm-dd-yyyy-HH-MM-SS');
imwrite(c,strcat('C:\Users\utd\Desktop\MFP\MATLAB_diff_',t,'.jpg'));	% This stores the differnce image. The location will need to be changed. 
f2=fopen(strcat('C:\Users\utd\Desktop\Expo\Log files\autotester_',datestamp,'.txt'),'a+');
%fseek(f2,0,'eof');
fprintf(f2,'%s',result);                                                % This stores the result of images matching or not matching in the same log
                                                                        % file as the log file of the test case from which image comparison was
                                                                        % called.
fclose(f2);
imshow(c)