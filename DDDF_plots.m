linewidth = 1.2;
set(0, 'DefaultLineLineWidth', linewidth);
set(0,'defaultTextInterpreter','latex');
set(groot, 'defaultAxesTickLabelInterpreter','latex'); 
set(groot, 'defaultLegendInterpreter','latex');

%%

in_path = 'Librairies/Abaqus_results/Tables/';
out_path = '';
filename = 'Weight_10_001_values.pkl';

fid = py.open(strcat(in_path,filename),'rb');
data = py.pickle.load(fid);

%%

fail = data{'failed'};

k = 1;
objective = [];
for i = 1:size(fail,2)
    if fail{i} == 0
        objective = [objective;data{'obj'}{i}];
%         k = k+1;
%         objective_const(i) =  data{'obj'}{i};
%     else
%         objective_const(i) =  data{'obj'}{k};
    end
end

%%

k = 1;
objective_decr(1) = objective(1);
for i = 2:size(objective)
    if objective(i) < objective_decr(i-1)
        objective_decr(i) = objective(i);
    else
        objective_decr(i) = objective_decr(i-1);
    end
end

figure()
plot(objective_decr)
hold on
plot(objective)

%%

filenames = {'PI_2_values.pkl','PI_values.pkl'};
in_path = 'Librairies/Abaqus_results/Tables/';

for i = 1:size(filenames,2)
    filename = filenames{i};
    fid = py.open(strcat(in_path,filename),'rb');
    data = py.pickle.load(fid);
    
    fail = data{'failed'};

    k = 1;
    objective = [];
    for i = 1:size(fail,2)
        if fail{i} == 0
            objective = [objective;data{'obj'}{i}];
        end
    end
    
    objective_decr(1) = objective(1);
    for i = 2:size(objective)
        if objective(i) < objective_decr(i-1)
            objective_decr(i) = objective(i);
        else
            objective_decr(i) = objective_decr(i-1);
        end
    end
    
    name = split(filename,'_');
    name = name{1};
    
    figure(i)
    
    plot(objective_decr, 'DisplayName',name, 'linestyle','--')
    hold on
    plot(objective, 'DisplayName',strcat(name,' obj'))
    legend()
end
