%% reiniciar variables, consola y figuras
clear; clc; close all


%% Definicion parametros

di1 = 0.00;   
di2 = 0.25;   
di3 = 0.38;


%% Lectura puerto serial

n_step = 1;
s = serialport("COM1",921600);
r = read(s,22,"string");
e = isempty(r);

while e == 0
    tramaList(:,n_step)=[r]
    n_step = n_step + 1;
    r = read(s,22,"string");
    e=isempty(r);
end


factor = 4*300/pi;

for m_step = 1:n_step-1
    str = '';
    i_step = 1;
    t = tramaList(m_step);
    t_char = char(t);
    [m,n]=size(t_char);
    pos_puntos = strfind(t,":");
    pos_coma = strfind(t,",");
    coma1 = pos_coma(1,1);
    coma2 = pos_coma(1,2);

    % Extract comando
    pos_com = pos_puntos + 1;  
    val = extract(t,pos_com);
    A = cell2mat(val); %Comando para pasar en str y no en cell array
    str_commando = append(str,A); % comando en str

    % Extract q11
    str = '';
    while i_step+3 < coma2
        pos = coma1 + i_step;
        val = extract(t,pos);
        A = cell2mat(val);
        str = append(str,A);
        i_step = i_step + 1;
    end

    str_dec11 = hex2dec(str);
    q11 = str_dec11/factor;
    
    % Extract q12
    str = '';
    while i_step+5 < n
        pos = coma2 + i_step-8;
        val = extract(t,pos);
        A = cell2mat(val);
        str = append(str,A);
        i_step = i_step + 1;
    end

    str_dec12 = hex2dec(str);
    q12 = str_dec12/factor;
    qi1_t(:,m_step) = [q11,q12]'; 
end

[m,n]=size(qi1_t);
m_steps = n;

for i_step = 1:m_steps
    [x, y] = xy_from_q(qi1_t(1,i_step), qi1_t(2,i_step), di1, di2, di3, 1, 1);
    x_t(:, i_step) = [x];
    y_t(:, i_step) =  [y]; %[y+0.1];%
    [q21, q22] = q2_from_xy(x_t(:, i_step), y_t(:, i_step), qi1_t(1,i_step), qi1_t(2,i_step), di1, di2);
    qi2_t(:, i_step) = [q21,q22]';
end


figure
for i_step = 1:m_steps
    % efector final
    scatter(x_t(:, i_step), y_t(:, i_step))
    hold on
    
    % brazos izquierda
    arrow_length = di2;
    % brazo 1
    startX = -di1;
    startY = 0;
    angle_radians = qi1_t(1, i_step);
    % Calculate the ending coordinates of the arrow
    endX = startX + arrow_length * cos(angle_radians);
    endY = startY + arrow_length * sin(angle_radians);
    % Plot the arrow
    quiver(startX, startY, endX - startX, endY - startY, 0, 'LineWidth', 4);

    arrow_length = di3;
    startX = endX;
    startY = endY;
    angle_radians = qi2_t(1, i_step) + qi1_t(1, i_step);
    % Calculate the ending coordinates of the arrow
    endX = startX + arrow_length * cos(angle_radians);
    endY = startY + arrow_length * sin(angle_radians);
    % Plot the arrow
    quiver(startX, startY, endX - startX, endY - startY, 0, 'LineWidth', 4);

    
    % brazos derecha
    arrow_length = di2;
    % brazo 2
    startX = di1;
    startY = 0;
    angle_radians = qi1_t(2, i_step);
    % Calculate the ending coordinates of the arrow
    endX = startX + arrow_length * cos(angle_radians);
    endY = startY + arrow_length * sin(angle_radians);
    % Plot the arrow
    quiver(startX, startY, endX - startX, endY - startY, 0, 'LineWidth', 2);
    
    arrow_length = di3;
    startX = endX;
    startY = endY;
    angle_radians = qi2_t(2, i_step) + qi1_t(2, i_step);
    % Calculate the ending coordinates of the arrow
    endX = startX + arrow_length * cos(angle_radians);
    endY = startY + arrow_length * sin(angle_radians);
    % Plot the arrow
    quiver(startX, startY, endX - startX, endY - startY, 0, 'LineWidth', 2);
    
    
    xlim([-.5, .5])
    ylim([-.4, .6])
    drawnow
    pause(0.01)
    hold off
end

figure
xlim([-.5, .5])
ylim([-.4, .6])
subplot(3,1,1)
plot(x_t,y_t)
subplot(3,1,2)
hold on
plot(x_t)
plot(y_t)
subplot(3,1,3)
hold on
plot(qi1_t(1,:))
plot(qi1_t(2,:))


%% functions
function [q21, q22] = q2_from_xy(x, y, q11, q12, di1, di2)

    q21 = atan2(((y - di2*sin(q11))),(x - di1 - di2*cos(q11))) - q11;
    q22 = atan2(((y - di2*sin(q12))),(x - di1 - di2*cos(q12))) - q12;

end

function [x, y] = xy_from_q(q11, q21, di1, di2, di3, xa, ya)

    a1 = -2*(di1 + di2 * cos(q11)); 
    b1 = -2*di2*sin(q11);
    c1 = (di1 + di2*cos(q11))^2 + (di2*sin(q11))^2 - di3^2; 

    a2 = -2*(di1 + di2 * cos(q21));
    b2 = -2*di2*sin(q21);
    c2 = (di1 + di2*cos(q21))^2 + (di2*sin(q21))^2 - di3^2;

    d1 = a2 - a1;
    d2 = b2 - b1;
    d3 = c2 - c1;
    e1 = -d1/d2;
    e2 = -d3/d2;
    f1 = 1 + e1^2;
    f2 = 2*e1*e2 + a1 + b1*e1;
    f3 = e2^2 + b1*e2 + c1;
    
    if b1 == b2
        if ya < 0
            x = -((c2 - c1)/(a2 - a1));
            y = (-b1 - sqrt(b1^2 - 4*(x^2 + a1*x + c1)))/ 2 ;   % val de y_t negativas
        else 
            x = -((c2 - c1)/(a2 - a1));
            y = (-b1 + sqrt(b1^2 - 4*(x^2 + a1*x + c1)))/ 2 ;   % val de y_t positivas     
        end
    
    else
        if xa < 0 
            x = (-f2 - sqrt(f2^2 - 4*f1*f3))/ (2*f1);   % val de x_t negativas
            y = e1*x + e2;
        else
            x = (-f2 + sqrt(f2^2 - 4*f1*f3))/ (2*f1);   % val de x_t positivas
            y = e1*x + e2 ;
        end
    end
end
