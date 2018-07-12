% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% %
%              Idoneidad BIOLOGICA para cultivo                   %
%                 (Elvira Ramos, 15/11/2017)                      %
%                   Matlab 7.12.0 (R2013b)                        %
% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% %

clc
clear all
close all

directorio = 'G:\Proyectos\2017_Cultivo\Datos';
directorio2 = 'G:\Proyectos\2017_Cultivo\Datos2';
coord=xlsread('G:\Proyectos\2017_Cultivo\Datos\Coordenadas.xlsx');

% %% Mejillon, vieira, zamburiña, volandeira, pulpo (inicial)****MAL****
% for i=1:1039
%     load([directorio2,'\SSTactualizada','\SST_',num2str((i)),'.mat']); %SST
%     tT = datevec(SST(:,1));
%     posIniSST=find(tT(:,1)==1997 & tT(:,2)==9 & tT(:,3)==19);
%     posFinSST=find(tT(:,1)==2013 & tT(:,2)==12 & tT(:,3)==31);
%     SST2=SST(posIniSST:posFinSST,2);
%     
%     load([directorio,'\Salinity','\Sal_',num2str((i)),'.mat']);
%     tS = datevec(Sal(:,1));
%     posIniSal=find(tS(:,1)==1997 & tS(:,2)==9 & tS(:,3)==19);
%     posFinSal=find(tS(:,1)==2013 & tS(:,2)==12 & tS(:,3)==31);
%     Sal2=Sal(posIniSal:posFinSal,2);
%     
%     load([directorio,'\Hs','\Hs_',num2str((i)),'.mat']); %Altura de ola
%     tHs = datevec(Hs(:,1));
%     posIniHs=find(tHs(:,1)==1997 & tHs(:,2)==9 & tHs(:,3)==19);
%     posFinHs=find(tHs(:,1)==2013 & tHs(:,2)==12 & tHs(:,3)==31);
%     Hs2=Hs(posIniSal:posFinSal,2);
%     
%     load([directorio2,'\ClorofilaFechas','\Clor2_',num2str((i)),'.mat']); %Clorofila
%     tC=load([directorio2,'\ClorofilaFechas','\fechas.mat']);
%     tC=tC.fechas;
%     posIniC=find(tC(:,1)==1997 & tC(:,2)==9 & tC(:,3)==19);
%     posFinC=find(tC(:,1)==2013 & tC(:,2)==12 & tC(:,3)==31);
%     clor3=clor2(posIniC:posFinC);
%          
%     load([directorio,'\Currents','\Uw_',num2str((i)),'.mat']); %Corrientes
%     vec=1:24; %pasar los datos de horarios a dirarios
%     for k=1:10592
%         UwD(k,:)=nanmean(Uw(vec,:));
%         vec=vec+24;
%     end
%     tUw = datevec(UwD(:,1));
%     posIniUw=find(tUw(:,1)==1997 & tUw(:,2)==9 & tUw(:,3)==19);
%     posFinUw=find(tUw(:,1)==2013 & tUw(:,2)==12 & tUw(:,3)==31);
%     Uw2=UwD(posIniUw:posFinUw,2);
%     
%     L=length(Hs2);
%     indMe = find(SST2>10 & SST2<20 & Sal2>27 & Sal2<38 & (clor3>1 | isnan(clor3)) & Uw2<0.35);
%     indViei = find(SST2>8 & SST2<16 & Sal2>26 & (clor3>1 | isnan(clor3)) & Uw2<0.35);
%     idMej(i) = length(indMe)/L;
%     idViei(i) = length(indViei)/L;
%     idZamb=idViei;
%     idVoland=idViei;
% end

% %Calculo NaN
% for i=1:1039
% load([directorio2,'\PARFechas','\PAR2_',num2str((i)),'.mat']); 
% kk=isnan(PAR2);
% tt=find(kk==1);
% porc(i)=length(tt)/length(kk)*100;
% end
% 
% mediaC=mean(porc);


%% Mejillon, vieira, zamburiña, volandeira (final)
for i=1:1039
    load([directorio2,'\SSTactualizada','\SST_',num2str((i)),'.mat']); %SST
    tT = datevec(SST(:,1));
    posIniSST=find(tT(:,1)==2002 & tT(:,2)==7 & tT(:,3)==4);
    posFinSST=find(tT(:,1)==2010 & tT(:,2)==12 & tT(:,3)==10);
    SST2=SST(posIniSST:posFinSST,2);
    
    load([directorio,'\Salinity','\Sal_',num2str((i)),'.mat']);
    tS = datevec(Sal(:,1));
    posIniSal=find(tS(:,1)==2002 & tS(:,2)==7 & tS(:,3)==4);
    posFinSal=find(tS(:,1)==2010 & tS(:,2)==12 & tS(:,3)==10);
    Sal2=Sal(posIniSal:posFinSal,2);
    
    load([directorio,'\Hs','\Hs_',num2str((i)),'.mat']); %Altura de ola
    tHs = datevec(Hs(:,1));
    posIniHs=find(tHs(:,1)==2002 & tHs(:,2)==7 & tHs(:,3)==4);
    posFinHs=find(tHs(:,1)==2010 & tHs(:,2)==12 & tHs(:,3)==10);
    Hs2=Hs(posIniSal:posFinSal,2);
    
    load([directorio2,'\ClorofilaFechas','\Clor2_',num2str((i)),'.mat']); %Clorofila
    tC=load([directorio2,'\ClorofilaFechas','\fechas.mat']);
    tC=tC.fechas;
    posIniC=find(tC(:,1)==2002 & tC(:,2)==7 & tC(:,3)==4);
    posFinC=find(tC(:,1)==2010 & tC(:,2)==12 & tC(:,3)==10);
    clor3=clor2(posIniC:posFinC);
    
    load([directorio,'\Currents','\Uw_',num2str((i)),'.mat']); %Corrientes
    vec=1:24; %pasar los datos de horarios a dirarios
    for k=1:10592
        UwD(k,:)=nanmean(Uw(vec,:));
        vec=vec+24;
    end
    tUw = datevec(UwD(:,1));
    posIniUw=find(tUw(:,1)==2002 & tUw(:,2)==7 & tUw(:,3)==4);
    posFinUw=find(tUw(:,1)==2010 & tUw(:,2)==12 & tUw(:,3)==10);
    Uw2=UwD(posIniUw:posFinUw,2);
    
    L=length(Hs2);
    indMe = find(SST2>10 & SST2<20 & Sal2>27 & Sal2<38 & (clor3>1 | isnan(clor3)) & Uw2<0.35);
    indViei = find(SST2>8 & SST2<16 & Sal2>26 & (clor3>1 | isnan(clor3)) & Uw2<0.35);
    idMej(i) = length(indMe)/L;
    idViei(i) = length(indViei)/L;
    idZamb=idViei;
    idVoland=idViei;
end

% Erizo
for i=1:1039
    load([directorio2,'\SSTactualizada','\SST_',num2str((i)),'.mat']); %SST
    tT = datevec(SST(:,1));
    posSST1=find(tT(:,1)==2015 & tT(:,2)==2 & tT(:,3)==11);
    posSST2=find(tT(:,1)==2015 & tT(:,2)==2 & tT(:,3)==13);
    vSST=(SST(posSST1,2)+SST(posSST2,2))/2;
    SST2=zeros(11322,1);
    SST2(1:posSST1)=SST(1:posSST1,2);
    SST2(posSST1+1)=vSST;
    SST2((posSST1+2):end)=SST(posSST2:end,2);
    
    load([directorio,'\Salinity','\Sal_',num2str((i)),'.mat']);
    tS = datevec(Sal(:,1));
    Sal2=Sal(:,2);
      
    L=length(tS);
    indErizo = find(SST2>8 & SST2<28 & Sal2>20 & Sal2<37);
    idErizo(i) = length(indErizo)/L;
end

%% Algas
for i=1:1039
    load([directorio2,'\SSTactualizada','\SST_',num2str((i)),'.mat']); %SST
    tT = datevec(SST(:,1));
    posSST1=find(tT(:,1)==2015 & tT(:,2)==2 & tT(:,3)==11);
    posSST2=find(tT(:,1)==2015 & tT(:,2)==2 & tT(:,3)==13);
    vSST=(SST(posSST1,2)+SST(posSST2,2))/2;
    SST2=zeros(11322,1);
    SST2(1:posSST1)=SST(1:posSST1,2);
    SST2(posSST1+1)=vSST;
    SST2((posSST1+2):end)=SST(posSST2:end,2);
    
    posIniSST=find(tT(:,1)==1997 & tT(:,2)==9 & tT(:,3)==16);
    SST2=SST2(posIniSST:end);
    
    load([directorio,'\Salinity','\Sal_',num2str((i)),'.mat']);
    tS = datevec(Sal(:,1));
    posIniSal=find(tS(:,1)==1997 & tS(:,2)==9 & tS(:,3)==16);
    Sal2=Sal(posIniSal:end,2);
    
    load([directorio2,'\PARFechas','\PAR2_',num2str((i)),'.mat']); 
    load([directorio2,'\PARFechas','\fechas.mat']); 
    posFinPAR=find(fechas(:,1)==2015 & fechas(:,2)==12 & fechas(:,3)==31);
    PAR3=PAR2(1:posFinPAR);
    
    L=length(PAR3);
    indSac = find(SST2>10 & SST2<15 & Sal2>30 & Sal2<40 & (PAR3<43.2 | isnan(PAR3)));
    indUnd = find(SST2>5 & SST2<17 & Sal2>30 & Sal2<40 & (PAR3<43.2 | isnan(PAR3)));
    indPor = find(SST2>15 & SST2<30 & Sal2>30 & Sal2<40 & (PAR3<43.2 | isnan(PAR3)));
    idSac(i) = length(indSac)/L;
    idUnd(i) = length(indUnd)/L;
    idPor(i) = length(indPor)/L;
end

%% Peces
for i=1:1039
    load([directorio2,'\SSTactualizada','\SST_',num2str((i)),'.mat']); %SST
    tT = datevec(SST(:,1));
    posSST1=find(tT(:,1)==2015 & tT(:,2)==2 & tT(:,3)==11);
    posSST2=find(tT(:,1)==2015 & tT(:,2)==2 & tT(:,3)==13);
    vSST=(SST(posSST1,2)+SST(posSST2,2))/2;
    SST2=zeros(11322,1);
    SST2(1:posSST1)=SST(1:posSST1,2);
    SST2(posSST1+1)=vSST;
    SST2((posSST1+2):end)=SST(posSST2:end,2);
    
    load([directorio,'\Salinity','\Sal_',num2str((i)),'.mat']);
    tS = datevec(Sal(:,1));
    Sal=Sal(:,2);
    
    L=length(SST2);
    indLubina= find(SST2>18 & SST2<27 & Sal>30 & Sal<40);
    indDorada = find(SST2>18 & SST2<26 & Sal>30 & Sal<40);
    indSalmon = find(SST2>6 & SST2<16 & Sal>10 & Sal<37);
    indAtun = find(SST2>9.4 & SST2<25 & Sal>30 & Sal<38);
    indCorvina = find(SST2>16.1 & SST2<27.7 & Sal>29.5 & Sal<39.1);
    indBacalao = find(SST2>0 & SST2<20 & Sal>6 & Sal<35);
    indBesugo = find(SST2>10.7 & SST2<20.2 & Sal>34.5 & Sal<37.8);
    indSeriola = find(SST2>19.1 & SST2<28.4 & Sal>33.2 & Sal<37.1);
    indCherna = find(SST2>15 & SST2<20 & Sal>32.4 & Sal<37.88);
    indMujel = find(SST2>8 & SST2<24 & Sal>33.4 & Sal<36.3);
    indAbadejo = find(SST2>14 & SST2<18 & Sal>31 & Sal<34);
    indDenton = find(SST2>8.7 & SST2<16.1 & Sal>35.4 & Sal<38.8);
    indPargo = find(SST2>20 & SST2<27.7 & Sal>31.6 & Sal<38);
    indCobia = find(SST2>21.7 & SST2<28.8 & Sal>32.7 & Sal<35.9);
    indMero = find(SST2>20.4 & SST2<26.5 & Sal>33.2 & Sal<37.2);
    indPerca = find(SST2>24.7 & SST2<28.8 & Sal>32.8 & Sal<35.31);
    indPezLimon = find(SST2>21 & SST2<30 & Sal>34.2 & Sal<36.4);
    indSargoPicudo = find(SST2>16.3 & SST2<21 & Sal>36.5 & Sal<38.7);
    indSargoComun = find(SST2>2.5 & SST2<18.8 & Sal>34.9 & Sal<38.6);
    indCorvinaNegra = find(SST2>14.9 & SST2<21.5 & Sal>34.6 & Sal<39);
    indVerrugato = find(SST2>19.89 & SST2<21.36 & Sal>27.78 & Sal<39);
    
    indPulpo = find(SST2>10 & SST2<20 & Sal>27 & Sal<35.5);
    indSepia = find(SST2>18 & SST2<25 & Sal>27 & Sal<35.5);
    
    idLubina(i) = length(indLubina)/L;
    idDorada(i) = length(indDorada)/L;
    idSalmon(i) = length(indSalmon)/L;
    idAtun(i) = length(indAtun)/L;
    idCorvina(i) = length(indCorvina)/L;
    idBacalao(i) = length(indBacalao)/L;
    idBesugo(i) = length(indBesugo)/L;
    idCherna(i) = length(indCherna)/L;
    idSeriola(i) = length(indSeriola)/L;
    idMujel(i) = length(indMujel)/L;
    idAbadejo(i) = length(indAbadejo)/L;
    idDenton(i) = length(indDenton)/L;
    idPargo(i) = length(indPargo)/L;
    idCobia(i) = length(indCobia)/L;
    idMero(i) = length(indMero)/L;
    idPerca(i) = length(indPerca)/L;
    idPezLimon(i) = length(indPezLimon)/L;
    idSargoPicudo(i) = length(indSargoPicudo)/L;
    idSargoComun(i) = length(indSargoComun)/L;
    idCorvinaNegra(i) = length(indCorvinaNegra)/L;
    idVerrugato(i) = length(indVerrugato)/L;
    
    idPulpo(i) = length(indPulpo)/L;
    idSepia(i) = length(indSepia)/L;
end

IB=zeros(1039,31);
IB(:,1)=idMej;
IB(:,2)=idViei;
IB(:,3)=idZamb;
IB(:,4)=idVoland;
IB(:,5)=idErizo;
IB(:,6)=idSac;
IB(:,7)=idUnd;
IB(:,8)=idPor;
IB(:,9)=idLubina;
IB(:,10)=idDorada;
IB(:,11)=idSalmon;
IB(:,12)=idAtun;
IB(:,13)=idCorvina;
IB(:,14)=idBacalao;
IB(:,15)=idBesugo;
IB(:,16)=idCherna;
IB(:,17)=idSeriola;
IB(:,18)=idMujel;
IB(:,19)=idAbadejo;
IB(:,20)=idDenton;
IB(:,21)=idPargo;
IB(:,22)=idCobia;
IB(:,23)=idMero;
IB(:,24)=idPerca;
IB(:,25)=idPezLimon;
IB(:,26)=idSargoPicudo;
IB(:,27)=idSargoComun;
IB(:,28)=idCorvinaNegra;
IB(:,29)=idVerrugato;
IB(:,30)=idPulpo;
IB(:,31)=idSepia;
% 
% cd G:\Proyectos\2017_Cultivo\MATLAB\RESULTADOS
% xlswrite('IB',IB);

