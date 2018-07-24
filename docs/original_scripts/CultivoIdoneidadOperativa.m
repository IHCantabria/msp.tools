% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% %
%              Idoneidad OPERATIVA para cultivo                   %
%                 (Elvira Ramos, 17/10/2017)                      %
%                   Matlab 7.12.0 (R2013b)                        %
% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% %

clc
clear all
close all

coord=xlsread('G:\Proyectos\2017_Cultivo\Datos\Coordenadas.xlsx');
directorio = 'G:\Proyectos\2017_Cultivo\Datos';
 
for i = 1:1039
    
    %Cargar los datos
    load([directorio,'\HsHour','\HsH_',num2str((i)),'.mat']); %Altura de ola horaria
    t = datevec(HsH(:,1));
    pos1=find(t(:,1)==1985);
    pos1=pos1(1);
    HsH=HsH(pos1:end,:);
    t = datevec(HsH(:,1));
    
    %% Ventanas de 8 horas
    vent = HsH(:,2);
    vent(HsH(:,2)>1) = 0; % este límite del paramero es para viento, si se hace para olas u otro parámetro cambiar
    vent(HsH(:,2)<=1) = 1;
    pa = ones(8,1);
    k = 1;
    cc = 0;
    while k + 7 < length(vent)
        if vent(k:k+7) == pa
            cc = cc + 1;
            k = k + 8;
        else
            k = k + 1;
        end
    end
    V_ventanas(i) = cc/(1 + max(t(:,1))-min(t(:,1)));
end

VentT=(365*24)/8;
IdHs= V_ventanas/VentT;
 
for i = 1:1039
    
    %Cargar los datos
    load([directorio,'\WindHour','\WsH_',num2str((i)),'.mat']); %Altura de ola horaria
    t = datevec(WsH(:,1));
    
    %% Ventanas de 8 horas
    vent = WsH(:,2);
    vent(WsH(:,2)>15) = 0; % este límite del paramero es para viento, si se hace para olas u otro parámetro cambiar
    vent(WsH(:,2)<=15) = 1;
    pa = ones(8,1);
    k = 1;
    cc = 0;
    while k + 7 < length(vent)
        if vent(k:k+7) == pa
            cc = cc + 1;
            k = k + 8;
        else
            k = k + 1;
        end
    end
    V_ventanas2(i) = cc/(1 + max(t(:,1))-min(t(:,1)));
end

VentT=(365*24)/8;
IdWs= V_ventanas2/VentT;

IdOperativa=coord(:,3);
IdOperativa(:,2)=coord(:,1);
IdOperativa(:,3)=coord(:,2);
IdOperativa(:,4)=IdHs;
IdOperativa(:,5)=IdWs;
IdOperativa(:,6)=V_ventanas2;
IdOperativa(:,7)=V_ventanas;

cd G:\Proyectos\2017_Cultivo\MATLAB\RESULTADOS
xlswrite('IdOperativa',IdOperativa);

figure (1)
scatter(coord(:,1),coord(:,2),[], IdWs,'filled')