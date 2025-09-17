clear
close all
clc

function ret = R(Z,k,N0,N)
    ret = mean(Z(N0+k+1:N0+N).*Z(N0+1:N0+N-k));     %itemwise multiplication of Z(i) and Z(i-k) stored in a vector and then taking its mean
end

function x = levinson_toeplitz(t, b)
% Solves T*x = b for symmetric Toeplitz T using Levinson recursion
% t: first column of Toeplitz matrix T (n x 1)
% b: right-hand side vector (n x 1)

n = length(t);
x = zeros(n,1);
a = zeros(n,1);

% Initial step
x(1) = b(1)/t(1);
a(1) = 1;
E = t(1);

for k = 1:n-1
    % Compute reflection coefficient
    a_temp = a(1:k);
    t_sub = t(2:k+1);
    lambda = - (t_sub' * flipud(a_temp)) / E;

    % Update a coefficients
    a_new = [a_temp; 0] + lambda * [0; flipud(conj(a_temp))];
    a(1:k+1) = a_new;

    % Update prediction error
    E = E * (1 - abs(lambda)^2);

    % Solve for x
    x(1:k+1) = x(1:k+1) + ((b(k+1) - t_sub' * flipud(x(1:k))) / E) * flipud(a(1:k+1));
end
end

tiledlayout(1,2)
trials = 500;
A_mat = [0.92 0.997];
B_mat = [0.95 0.999];

for test = 1:2
    nexttile
    A = A_mat(test);
    B = B_mat(test);
    h1 = A + B;
    h2 = -A^2 -A*B;
    h3 = B*A^2;
    C = (1 + h1^2 + h2^2 + h3^2)^0.5;
    
    N0_mat = [0 0 0 500 5000];
    N_mat = [100 1000 20000 1000 20000];

    mse_8 = zeros([5 8]);
    
    for nth = 1:5       %for all 5 combinations of N0 and N values
        N0 = N0_mat(nth);
        N = N_mat(nth);
        
        SNR_dB = 0:3:21;
        sigma_v = 10.^(-SNR_dB/20);     %from formula (relation between SNR and sigma_v) given
        
        for sig_no = 1:1:8     %iterating over the 8 SNRs
            sigma = sigma_v(sig_no);
            e2 = zeros([1 trials]);     %stores square error values for each of the 500 trials
            for j = 1:1:trials  %iterating over the 500 trials
                X_n = randn([1 (N0+N)]);
            
                Y_n = zeros([1 (N0+N)]);
                Y_n(1) = X_n(1).*C;
                Y_n(2) = Y_n(1)*h1 + X_n(2).*C;
                Y_n(3) = Y_n(2)*h1 + Y_n(1)*h2 + X_n(3).*C;
                for n= 4:(N0+N)
                    Y_n(n) = Y_n(n-1).*h1 + Y_n(n-2).*h2 + Y_n(n-3).*h3 + X_n(n).*C;
                end
            
                V_n = sigma.*randn([1 (N0+N)]);     %Gaussian RP with variance sigma
                Z_n = Y_n + V_n;
            
                r_vector = [R(Z_n,1,N0,N) R(Z_n,2,N0,N) R(Z_n,3,N0,N)]';
                R_matrix = [[R(Z_n,0,N0,N) R(Z_n,1,N0,N) R(Z_n,2,N0,N)];[R(Z_n,1,N0,N) R(Z_n,0,N0,N) R(Z_n,1,N0,N)];[R(Z_n,2,N0,N) R(Z_n,1,N0,N) R(Z_n,0,N0,N)]];
                %h_pred_1 = R_matrix\r_vector;
                h_pred = levinson_toeplitz(R_matrix(:,1), r_vector);
                e2(j) = (h1-h_pred(1))^2 + (h2-h_pred(2))^2 + (h3-h_pred(3))^2;     %square error values
            end
            mse_8(nth, sig_no) = 10*log10(mean(e2));    %mse for that sigma for that set of N0 and N
        end
    end
    toplot = mse_8';
    p = plot(SNR_dB, toplot(1:8), SNR_dB, toplot(9:16), SNR_dB, toplot(17:24), SNR_dB, toplot(25:32), SNR_dB, toplot(33:40));
    for pltno = 1:1:5
        p(pltno).LineWidth = 2;
        p(pltno).Marker = 'x';
    end
    grid on
    legend({'N0 = 0, N = 100', 'N0 = 0, N = 1000', 'N0 = 0, N = 20000', 'N0 = 500, N = 1000', 'N0 = 5000, N = 20000'}, 'Location','southwest')
    xlabel('SNR (dB) --->')
    ylabel('<--- Mean Square Error (dB)')
    if test == 1
        title('Plot of MSE vs SNR for Case 1 (𝛼 = 0.92; 𝛽 = 0.95)')
    else
        title('Plot of MSE vs SNR for Case 2 (𝛼 = 0.997; 𝛽 = 0.999)')
    end
end