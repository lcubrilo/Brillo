%% Read and organize data
% This script reads the .dat file outputed by aixacct when exported as
% ASCII from PZM or DHM mode. It pulls the summary data in a 2D array and
% the measurement data into a 3D array with D1&2 being the table as seen in
% the .dat file and the 3rd dimension being the different meaurement
% ordered as they are in the file.

% Go to file folder while remembering the origin folder from the script to
% be able to come back at the end
a = pwd;
cd(folder)

% Open dat file
fileID = fopen(file_name,'r');

%% PZM or DHM
% The lign of the script tells us weather it is a PZM file or a DHM file.
% Depending on the result, the position of some columns will be different.
% These positions are recorded in a number of variables

temp = textscan(fileID,'%s',1,'delimiter','\n');
% Set all the variables as if it were DHM
ncol=13; % Nb of columns in the data tables
nlign=401; % Nb of ligns in the data tables
fcol=1; % Position of the frequency column in the summary table
vcol=2; % Position of the voltage column in the summary table    
icol=4; % Current column in the data tables
pcol=5; % Polarization column in the data tables
prpcol=5; % Position of Pr+ in the summary table
prmcol=6; % Position of Pr- in the summary table
vcpcol=3; % Position of Vc+ in the summary table
vcmcol=4; % Position of Vc- in the summary table
dcol=10; % Displacement column in the data tables (NaN for DHM measurements)

% If it is PZM, the first lign of the file will be "PiezoResult", read the
% file as pzm
pzm = strcmp(temp{1}{1},'PiezoResult');


%% Read summary
% Skip the next 2 ligns that don't hold any information
textscan(fileID,'%s',1,'delimiter','\n');
textscan(fileID,'%s',1,'delimiter','\n');

% Save the summary headers
headers = {'Hysteresis Frequency [Hz]','Hysteresis Amplitude [V]','Vc+ [V]','Vc- [V]','Pr+ [uC/cm2]','Pr- [uC/cm2]','Current Range []','Pvmax+ [uC/cm2]','Pvmax- [uC/cm2]','Dpp [nm]','Dpp1 [nm]','Dpp2 [nm]','Dpp3 [nm]','Dpp4 [nm]','d33ls [nm/V]','d33ls+ [nm/V]','d33ls- [nm/V]','Pvmax+ [uC/cm2]','Pvmax- [uC/cm2]','Dvmax+ [nm/V]','Dvmax- [nm/V]'};
headers_lign = textscan(fileID,'%s',1,'delimiter','\n');
headers_lign = strsplit(headers_lign{1}{1},'\t');
if pzm
    ind = zeros(1,length(headers));
    for i = 1:length(headers)
        ind(i) = find(strcmp(headers_lign,headers{i}));
    end
else
    ind = zeros(1,length(headers)-12);
    for i = 1:length(headers)-12
        ind(i) = find(strcmp(headers_lign,headers{i}));
    end
end

temp = textscan(fileID,'%s',1,'delimiter','\n');

summary = [];% Inithalize summary variable
% Read each ligns of the summary one by one, convert the data from string
% into numbers and save it in the summary array
while ~isempty(temp{1}{1}) % The lign after the summary table is empty
    temp = strsplit(temp{1}{1},'\t');
    temp = str2double(temp(ind));
    summary = [summary; [temp NaN(1,length(headers)-length(temp))]];
    temp = textscan(fileID,'%s',1,'delimiter','\n');
end
 

%% Read measurement values
%Initialize stored variables
sname = cell(size(summary,1),1); % To be returned to the original script at the end
thickness = zeros(size(summary,1),1); % To be concatenated in the end to the summary matrix
area = zeros(size(summary,1),1); % To be concatenated in the end to the summary matrix
data = zeros(nlign, ncol, size(summary,1));
temp = strsplit(temp{1}{1},':');
for i = 1:size(summary,1) % do this as many times as there are measurements
    % Find sample name
    while ~strcmp(temp(1),'SampleName')
        temp = textscan(fileID,'%s',1,'delimiter','\n');
        if ~isempty(temp{1})
            temp = strsplit(temp{1}{1},':'); % Split the lign at ':' character
        else
            temp = ' ';
        end
    end
    sname{i} = strrep(temp{2},'_',' '); % Replace '_' with space from name part and save it in the sname cell array
    % Find Area value
    while ~strcmp(temp(1),'Area [mm2]')
        temp = textscan(fileID,'%s',1,'delimiter','\n');
        if ~isempty(temp{1})
            temp = strsplit(temp{1}{1},':');
        else
            temp = ' ';
        end
    end
    area(i) = str2double(temp{2}); % Convert to number and save it in area array
    % Find Thickness Value
    while ~strcmp(temp(1),'Thickness [nm]')
        temp = textscan(fileID,'%s',1,'delimiter','\n');
        if ~isempty(temp{1})
            temp = strsplit(temp{1}{1},':');
        else
            temp = ' ';
        end
    end
    thickness(i) = str2double(temp{2})/10e6; % Convert to number, then into cm and save in thickness array
    
    % Find start of data: the last lign before the data starts with the
    % word 'Time'. We read ligns one by one until we find the one that
    % start by that word
    headers = {'Time [s]','V+ [V]','V- [V]','I1 [A]','P1 [uC/cm2]','I2 [A]','P2 [uC/cm2]','I3 [A]','P3 [uC/cm2]','D1 [nm]','D2 [nm]','D3 [nm]'};
    while ~strcmp(temp(1),'Time')
        temp = textscan(fileID,'%s',1,'delimiter','\n');
        if ~isempty(temp{1})
            temp = strsplit(temp{1}{1},' ');
        else
            temp = ' ';
        end
    end
    
    % Read data table
    for j=1:nlign
        temp = textscan(fileID,'%s',1,'delimiter','\n'); % Read each lign
        temp = str2double(strsplit(temp{1}{1},'\t')); % Split the lign at each tab character and convert each part to numbers
        data(j,:,i) = [temp(1:end-1) NaN(1,ncol+1-length(temp))]; % Save the data lign array in the data matrix on the correct sheet
    end
end

% Add the area and thickness information to the summary matrix
summary = [summary area thickness];

% Close file, go back to original folder and cleanup workspace from useless
% variables
fclose(fileID);
cd(a);
clearvars a area file_name fileID i j temp headers headers_lign ind ncol nlign
