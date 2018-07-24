% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% %
%            Idoneidad ESTRUCTURAL para cultivo                   %
%                 (Elvira Ramos, 13/10/2017)                      %
%                   Matlab 7.12.0 (R2013b)                        %
% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% %

clc
clear all
close all

directorio = 'G:\Proyectos\2017_Cultivo\Datos';

%% 1.- Idoneidad por batimetría y pendiente (limitantes)

bat=xlsread('G:\Proyectos\2017_Cultivo\Datos2\DatosBatiPte.xlsx');
bat(:,5)=bat(:,5)*-1;

IdBati1C=zeros(1039,1);
for i = 1:1039
    if bat(i,5)<300 & bat(i,4)<25
        IdBati1C(i) = 1;
    end
end

IdBati2C=zeros(1039,1);
for i = 1:1039
    if bat(i,5)>15 & bat(i,5)<40 & bat(i,4)<25
        IdBati2C(i) = 1;
    end
end

IdBati1=zeros(1039,1);
for i = 1:1039
    if bat(i,5)<300
        IdBati1(i) = 1;
    end
end

IdBati2=zeros(1039,1);
for i = 1:1039
    if bat(i,5)>15 & bat(i,5)<40
        IdBati2(i) = 1;
    end
end

IdPte=zeros(1039,1);
for i = 1:1039
    if bat(i,4)<25
        IdPte(i) = 1;
    end
end

%% 2.- Idoneidad por oleaje y corrientes PR 50

for i = 1:1039
    
    %Cargar los datos
    load([directorio,'\Hs','\Hs_',num2str((i)),'.mat']); %Altura de ola
    HsR=Hs(1:10592,:); %Hs reducida a 2013
    HsR2=HsR(:,2);
    
    load([directorio,'\Currents','\Uw_',num2str((i)),'.mat']); %Corrientes
    vec=1:24; %pasar los datos de horarios a dirarios
    for k=1:10592
        UwD(k,:)=nanmean(Uw(vec,:));
        vec=vec+24;
    end
    UwD2=UwD(:,2);
    
    %% Cálculo 50 años PR
    % Altura de ola
    t = datevec(HsR(:,1)); %columna tiempo de mis datos
    
    vec=(min(t(:,1)):max(t(:,1))); %calcular maximos anuales
    for j=1:length(vec)
        pos=t(:,1)==(vec(j));
        muestra(j)=max(HsR2(pos,:));
    end
    
    parmhat = gevfit(muestra);%ajusto una GEV
    X = gevinv(1-1/50,parmhat(1),parmhat(2),parmhat(3));%Obtengo el valor asociado al TR=50años
    Hs_50(i) = X; % altura de ola (u otro parámetro) con periodo de retorno 50 años  
  
    % Corrientes
    t = datevec(UwD(:,1)); %columna tiempo de mis datos
    
    vec=(min(t(:,1)):max(t(:,1))); %calcular maximos anuales
    for j=1:length(vec)
        pos=t(:,1)==(vec(j));
        muestra2(j)=max(UwD2(pos,:));
    end
    
    %prob_e = [1:length(muestra2)]/(1+length(muestra2)); %Prueba para comprobar ajuste
    parmhat = gevfit(muestra2);%ajusto una GEV
    X = gevinv(1-1/50,parmhat(1),parmhat(2),parmhat(3));%Obtengo el valor asociado al TR=50años
    
    %figure %Prueba para comprobar ajuste
    %plot(sort(muestra2),prob_e)
    
    UwD_50(i) = X; % altura de ola (u otro parámetro) con periodo de retorno 50 años
    pos2=isnan(UwD_50(i));
    if pos2==1
        UwD_50(i)=0;
    else
        continue
    end
end

%% BUSCAR IDONEIDAD ESTRUCTURAL
for i = 1:1039
    if Hs_50(i)<5
        posHs_50(i) = 1;
    else
        posHs_50(i) = 0;
    end
end

for i = 1:1039
    if UwD_50(i)<1
        posUwD_50(i) = 1;
    else
        posUwD_50(i) = 0;
    end
end

for i = 1:1039
    if posHs_50(i) == 1 & posUwD_50(i) == 1
        posHsUwD_50(i) = 1;
    else
        posHsUwD_50(i) = 0;
    end
end

for i = 1:1039
    if posHs_50(i) == 1 & IdBati1C(i)==1
        posHs_50_1(i) = 1;
    else
        posHs_50_1(i) = 0;
    end
end

for i = 1:1039
    if posHs_50(i) == 1 & IdBati2C(i)==1
        posHs_50_2(i) = 1;
    else
        posHs_50_2(i) = 0;
    end
end

for i = 1:1039
    if posUwD_50(i) == 1 & IdBati1C(i)==1
        posUwD_50_1(i) = 1;
    else
        posUwD_50_1(i) = 0;
    end
end

for i = 1:1039
    if posUwD_50(i) == 1 & IdBati2C(i)==1
        posUwD_50_2(i) = 1;
    else
        posUwD_50_2(i) = 0;
    end
end

for i = 1:1039
    if posHsUwD_50(i) == 1 & IdBati2C(i)==1
        posHsUwD_50_2(i) = 1;
    else
        posHsUwD_50_2(i) = 0;
    end
end

for i = 1:1039
    if posHsUwD_50(i) == 1 & IdBati1C(i)==1
        posHsUwD_50_1(i) = 1;
    else
        posHsUwD_50_1(i) = 0;
    end
end

%% MATRIZ PARA GUARDAR
coord=xlsread('G:\Proyectos\2017_Cultivo\Datos\Coordenadas.xlsx');

IE1(:,1)=coord(:,3);
IE1(:,2)=coord(:,2);
IE1(:,3)=coord(:,1);
IE1(:,4)=IdBati1;
IE1(:,5)=IdPte;
IE1(:,6)=IdBati1C;
IE1(:,7)=posHs_50;
IE1(:,8)=posUwD_50;
IE1(:,9)=posHs_50_1;
IE1(:,10)=posUwD_50_1;
IE1(:,11)=posHsUwD_50_1;

IE2(:,1)=coord(:,3);
IE2(:,2)=coord(:,2);
IE2(:,3)=coord(:,1);
IE2(:,4)=IdBati2;
IE2(:,5)=IdPte;
IE2(:,6)=IdBati2C;
IE2(:,7)=posHs_50;
IE2(:,8)=posUwD_50;
IE2(:,9)=posHs_50_2;
IE2(:,10)=posUwD_50_2;
IE2(:,11)=posHsUwD_50_2;

cd G:\Proyectos\2017_Cultivo\MATLAB\RESULTADOS
xlswrite('IE1',IE1);
xlswrite('IE2',IE2);

%scatter(IE1(:,3),IE1(:,2),[],IE2(:,11),'filled')
