clear all
%% Parameters that need to be provided to the script to find and plot the data correctly
% Folder where the data is stored. All the files in this fomder should be
% of the same type DHM or PZM

folder = 'C:\Users\Mathieu Fricaudet\OneDrive - CentraleSupelec\Documents\PVDF_BFO_composite\BFO_caracterization\Aixacct\berlincourd_poling\PVDF-20TrFE';

% Reordering of the files ([] if you want to plot everything)
ord = [1 5 2 3 4];
% ord = [11 14 15 16 17 12 13];
% Plot parameters
compo = [0 5 10 15 20]; % used to specify the spacing of the different measurements on the graph if necessary. If not, enter a regularly spaced array of the same length as labels

labels = {'0% BFO','5% BFO','10% BFO','15% BFO','20% BFO'};
% labels = {};

ticks = 1:length(labels);
x_list = 1:length(labels);

%% Start
a = pwd;
cd(folder)
files = dir;
cd(a)

% Find the files with the .dat format
i_list = false(length(files),1);
for j=3:length(files)
    if length(files(j).name)>=4
        name = files(j).name(end-3:end);
        i_list(j) = strcmp(name,'.dat');
    end
end
files = files(i_list); % Remove the files with the wrong format from the files listso that they won't be read by accident

%% Reorder the files if needed
% The default order is alphabetical. This ordering will be how they will
% appear in the graphs. If you wish to change this order to better reflect
% your data, you should use the ord array
if exist('ord')
    files = files(ord);
end

%% Read all the files and store the data in a 3D array + Summary
% Initialize variable to store the data
data_all = []; % This will be a 3D array dimensions: D1*D2 = table as returned by aixacct; D3 = individual measurements 
summary_all = []; % This will be a 2D array with each measurements on top of each other, and each file on top of the previous one
sname_all = {};
% Read all files one by one
for l = 1:length(files)
    file_name = files(l).name; % Get file name
    read_aixacct_dat_long % Read the file using the dat reading script
    data_all = cat(3,data_all, data); % Concatenate the new data to the already stored data along the 3rd dimension
    summary_all = [summary_all; summary]; % Put new summary under the previous ones
    sname_all = [sname_all; sname]; % Idem
end

% Rename to simplify
data = data_all;
summary = summary_all;
sname = sname_all;
% Cleanup workspace of useless variables
clearvars sname_all a l data_all i_list ord name summary_all thickness


%% Choose which  to plot
% The "plot_list" variable is an arry with the indices of the measurements
% that you want to plot in the "summary" table  

plot_list = find(abs(floor(summary(:,vcol)./summary(:,end)/1000)-1000)<10); % Loops at 1000kV/cm here

% plot_list = unique([plot_list(diff(plot_list)>1); plot_list(end);size(summary,1)])
% plot_list = 1:size(summary,1); % If you want to plot all measurements

% If labels isn't specified, the sample names will be used
if isempty(labels)
    labels = sname(plot_list);
end

%% Plot PE
%This part will plot the polarization VS the electric field for the
%measurements selected in "plot_list"

figure('Name','PE curves','NumberTitle','off');
P_E = zeros(size(data,1),2*size(plot_list,1)); % The data will be saved in this array in case the user wants to export it to file
headers = cell(1,2*size(plot_list,1));
for j=1:length(plot_list)
    E = data(:,2,plot_list(j))/summary(plot_list(j),end)/1000; % Electric field in kV/cm at each point (column 2 holds the Voltage data)
    plot(E, data(:,pcol,plot_list(j)));hold on; % Plot the data in pcol VS the electric field
    P_E(:,[2*j-1 2*j]) = [E data(:,pcol,plot_list(j))];
    headers([2*j-1 2*j]) = {'E [kV/cm]', ['P_{' labels{j} '} [µC/cm2]']};
end
xlabel('Electric field [kV/cm]');
ylabel('Polarization [µC/cm^2]');
legend(labels);
P_E = [headers;num2cell(P_E)]; % Final formating of the storing array for nice output file

%% Plot IE
%This part will plot the current VS the electric field for the
%measurements selected in "plot_list"

figure('Name','Current curves','NumberTitle','off');
I_E = zeros(size(data,1),2*size(plot_list,1)); % The data will be saved in this array y case the user wants to export it to file
for j=1:length(plot_list)
    E = data(:,2,plot_list(j))/summary(plot_list(j),end)/1000; % Electric field in kV/cm at each point (column 2 holds the Voltage data)
    plot(E, data(:,icol,plot_list(j))*1000000);hold on; % Plot the data in icol VS the electric field in µA
    I_E(:,[2*j-1 2*j]) = [E data(:,icol,plot_list(j))*1000000];
    headers(2*j) = {['I_{' labels{j} '} [µA]']};
end
xlabel('Electric field [kV/cm]');
ylabel('Current [µA]');
legend(labels);
I_E = [headers;num2cell(I_E)];% Final formating of the storing array for nice output file


%% Plot Strain
%This part will plot the strain VS the electric field for the
%measurements selected in "plot_list"

if pzm
    figure('Name','SE curves','NumberTitle','off');
    S_E = zeros(size(data,1),2*size(plot_list,1)); % The data will be saved in this array y case the user wants to export it to file
    for j=1:length(plot_list)
        E = data(:,2,plot_list(j))/summary(plot_list(j),end)/1000; % Electric field in kV/cm at each point (column 2 holds the Voltage data)
        S = data(:,dcol,plot_list(j))./summary(plot_list(j),end)/100000; % Compute the Strain at each point
        plot(E, S);hold on;
        S_E(:,[2*j-1 2*j]) = [E S];
        headers(2*j) = {['S_{' labels{j} '} [%]']};
    end
    xlabel('Electric field [kV/cm]');
    ylabel('Strain [%]');
    legend(labels);
    S_E = [headers;num2cell(S_E)]; % Final formating of the storing array for nice output file
end

%% Compute Pr Ec
% Here, we pull the remanent polarization and the coercive field from the
% summary table and we plot it VS the experiments in "plot_list". These
% experiments may vary depending on how you organized your data folder.
% That's why you will find a variable "labels" which you can update to
% reflect you data. You may want to update as well the "ticks" and "x_list"
% variable depending if your points should be evenly distributed or not.
% These parameters are located on the top of the script for easy access

% Initialize vectors 2 columns: one for Pr+ and one for Pr-, same for Ec
Pr = zeros(length(plot_list),2);
Ec = zeros(length(plot_list),2);

% If you want to compute Pr and Ec from the curve rather than using the
% values computed by aixacct

% for j=1:length(plot_list)
%     % Remanant polarization positive
%     tempV = data(data(:,5,plot_list(j))>=0 & [diff(data(:,5,plot_list(j)));0]<0, 2, plot_list(j));
%     tempP = data(data(:,5,plot_list(j))>=0 & [diff(data(:,5,plot_list(j)));0]<0, 5, plot_list(j));
%     Pr(j,1) = interp1(tempV, tempP, 0);
%     % Remanant polarization negative
%     tempV = data(data(:,5,plot_list(j))<=0 & [diff(data(:,5,plot_list(j)));0]>0, 2, plot_list(j));
%     tempP = data(data(:,5,plot_list(j))<=0 & [diff(data(:,5,plot_list(j)));0]>0, 5, plot_list(j));
%     Pr(j,2) = interp1(tempV, tempP, 0);
%     % Coercive Field positive
%     tempV = data(data(:,2,plot_list(j))>=0 & [diff(data(:,2,plot_list(j)));0]>0, 2, plot_list(j));
%     tempP = data(data(:,2,plot_list(j))>=0 & [diff(data(:,2,plot_list(j)));0]>0, 5, plot_list(j));
%     Ec(j,1) = interp1(tempP, tempV, 0)/summary{plot_list(j),end}/1000;
%     % Coercive Field positive
%     tempV = data(data(:,2)<=0 & [diff(data(:,2,plot_list(j)));0]<0, 2, plot_list(j));
%     tempP = data(data(:,2)<=0 & [diff(data(:,2,plot_list(j)));0]<0, 5, plot_list(j));
%     Ec(j,2) = interp1(tempP, tempV, 0)/summary{plot_list(j),end}/1000;
% end

% Use Aixacct measurement
Pr = summary(plot_list,[prpcol prmcol]); % Pull values from summary
Ec = summary(plot_list,[vcpcol vcmcol])./summary(plot_list,end)/1000; % Aixacct provides Vc, so we need to devide by the thickness to get Ec

% Plot
figure('Name','Pr and Ec','NumberTitle','off');
nexttile

plot(compo, Pr(:,1)); hold on % plot Pr + and -
plot(compo, Pr(:,2));
title('Remanent polarization');
xlabel('Composition [% BFO]');
ylabel('Polarization [µC/cm^2]')
legend({'Pr+','Pr-'});

nexttile % New graph in figure
plot(compo, Ec(:,1)); hold on % Plot Ec + and -
plot(compo, Ec(:,2));
title('Coercive field');
xlabel('Composition [% BFO]');
ylabel('Coercive Field [kV/cm]');
legend({'Ec+','Ec-'});

Pr_Ec = [{'Composition [% BFO]','Pr+ [µC/cm2]','Pr- [µC/cm2]','Ec+ [kV/cm]','Ec- [kV/cm]'} ; num2cell([compo' Pr Ec])]; % Put data in cell array in case of data expprt to file


%% Plot Strain Vs experiment
% Initialize variables for max and min of displacement at positive and
% negative voltages
if pzm
    DispPosM = zeros(length(plot_list),1);
    DispPosm = zeros(length(plot_list),1);
    DispNegM = zeros(length(plot_list),1);
    DispNegm = zeros(length(plot_list),1);

    % Find the maxs and mins over the correct part of the curves
    for i=1:length(plot_list)
        DispPosM(i) = max(data(data(:,2,plot_list(i))>0,dcol,plot_list(i))); % Displacement max at positive field
        DispPosm(i) = min(data(data(:,2,plot_list(i))>0,dcol,plot_list(i))); % Displacement min at positive field
        DispNegM(i) = max(data(data(:,2,plot_list(i))<0,dcol,plot_list(i))); % Displacement max at negative field
        DispNegm(i) = min(data(data(:,2,plot_list(i))<0,dcol,plot_list(i))); % Displacement min at negative field
    end

    % Plot
    figure('Name','Strain min and max','NumberTitle','off');
    plot(compo, DispPosM./summary(plot_list,end)/100000); hold on; % devide by thickness to get strain
    plot(compo, DispPosm./summary(plot_list,end)/100000);
    plot(compo, DispNegM./summary(plot_list,end)/100000);
    plot(compo, DispNegm./summary(plot_list,end)/100000);
    legend({'S_m_a_x Positive Field','S_m_i_n Positive Field','S_m_a_x Negative Field','S_m_i_n Negative Field'});
    xlabel('Composition');
    ylabel('Strain [%]');


    %% Plot d33
    figure('Name','dS/dE','NumberTitle','off');
    nexttile
    d33 = zeros(length(plot_list),1);
    for j=1:length(plot_list)
        E = data(:,2,plot_list(j))/summary(plot_list(j),end)/1000; % Electric field in kV/cm at each point (column 2 holds the Voltage data)
        S = data(:,dcol,plot_list(j))./summary(plot_list(j),end)/10000000; % Compute the Strain at each point
        d = diff(S)./diff(E)*1e-5*1e12;
        E = E(1:end-1);
        plot(E, smooth(d,10));hold on;
        d33(j) = -interp1(E(diff(E)<0), d(diff(E)<0), 0); % extract the derivative of the strain with respect to the eletcric field at 0 field to get d33
    end
    xlabel('Electric field [kV/cm]');
    ylabel('d33 [pC/N]');
    legend(labels);
    xlim([Ec(j,2)*0.8 Ec(j,1)*0.8]);

    % Plot d33
    nexttile
    plot(compo,d33);
    xlabel('composition [%BFO]');
    ylabel('d33 [pC/N]');
    d33 = [{'Composition [% BFO]', 'd33 [pC/N]'};num2cell([compo' d33])]; % Save in cell array for potential data exporting into file
end



%This is a script that I have developped to redistribute the plot windows
%on your screen. It is not part of Matlab, and it should be added to the
%Matlab folder to be accessible from any script on your computer
orgfig



%% If you want to export the data into files, you can use any of these lines. Make sure that you specify the correct file name and folder because it will automatically overwrite the file
%% Without asking for confirmation
% save2file(d33,'PVDF-30TrFE_d33_allcompo.dat','folder','C:\Users\Mathieu Fricaudet\OneDrive - CentraleSupelec\Documents\PVDF_BFO_composite\BFO_caracterization\Aixacct\loops\exports')
save2file(P_E,'PVDF-20TrFE_PE.dat','folder','C:\Users\Mathieu Fricaudet\OneDrive - CentraleSupelec\Documents\PVDF_BFO_composite\BFO_caracterization\Aixacct\loops\exports')
save2file(I_E,'PVDF-20TrFE_IE.dat','folder','C:\Users\Mathieu Fricaudet\OneDrive - CentraleSupelec\Documents\PVDF_BFO_composite\BFO_caracterization\Aixacct\loops\exports')
% save2file(S_E,'PVDF-30TrFE_SE_allcompo.dat','folder','C:\Users\Mathieu Fricaudet\OneDrive - CentraleSupelec\Documents\PVDF_BFO_composite\BFO_caracterization\Aixacct\loops\exports')
save2file(Pr_Ec,'PVDF-20TrFE_PrEc.dat','folder','C:\Users\Mathieu Fricaudet\OneDrive - CentraleSupelec\Documents\PVDF_BFO_composite\BFO_caracterization\Aixacct\loops\exports')
