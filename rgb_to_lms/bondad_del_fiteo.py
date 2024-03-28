from sklearn.linear_model import LinearRegression
import numpy as np
from matplotlib import pyplot as plt

def nonlinear_fit(X, A, gammas, A0):
    # Ensure X is a column vector
    #X = np.array(X).reshape(3, -1)
    
    # Calculate Y using the nonlinear fit formula
    Y = np.transpose(np.power(X, np.transpose(gammas)))
    Y = np.dot(A, Y) + A0
    
    return np.transpose(Y)

# Given parameters
optimized_A = np.array([[0.0000018953, 0.0000050506, 0.0000002077],
                        [0.0000005988, 0.0000051039, 0.0000002803],
                        [0.0000000362, 0.000000087, 0.000001023]])

optimized_gammas = np.array([2.2368352, 2.20488322, 2.41013882])

optimized_A0 = np.array([[0.00079304],
                         [0.00111091],
                         [0.00528226]])

# Example usage
X_input = [0, 2.0, 3.0]  # Replace with your actual input data
result = nonlinear_fit(X_input, optimized_A, optimized_gammas, optimized_A0)



data = np.loadtxt("rgb_to_lms/rgb_to_lms_R_G_B_L_M_S_data_final_normalizada.txt", skiprows=1)

#RGB = np.transpose(data[:, :3])  # First three columns as independent variables (A, B, C)
#LMS = np.transpose(data[:, 3:])
RGB = data[:, :3]
LMS = data[:, 3:]


LMS_fitted = nonlinear_fit(RGB, optimized_A, optimized_gammas, optimized_A0)

index_B = [i for i in range(11)]
index_G = [0] + [12, 17, 18, 19, 24, 25, 30, 31, 32, 37, 38]
index_R = [0] + [39, 64, 65, 66, 91, 92, 116, 117, 118, 143, 144]
index_102 = [44,45,46,47,48]

R_axis = RGB[index_R, 0]
G_axis = RGB[index_G, 1]
B_axis = RGB[index_B, 2]
RGB_102 = RGB[index_102, 2]

LMS_blue = LMS[index_B]
LMS_blue_fitted = LMS_fitted[index_B,:]
LMS_green = LMS[index_G]
LMS_green_fitted = LMS_fitted[index_G, :]
LMS_red = LMS[index_R]
LMS_red_fitted = LMS_fitted[index_R, :]
LMS_102 = LMS[index_102]
LMS_102_fitted = LMS_fitted[index_102]

plt.figure(figsize = (8,6))
plt.scatter(B_axis[np.argsort(B_axis)], LMS_blue[np.argsort(B_axis),0], marker = 'o', label = 'Coordenada L en función de B', color = '#CC0000')
plt.scatter(B_axis[np.argsort(B_axis)], LMS_blue[np.argsort(B_axis),1], marker = 'o', label = 'Coordenada M en función de B', color = '#00CC00')
plt.scatter(B_axis[np.argsort(B_axis)], LMS_blue[np.argsort(B_axis),2], marker = 'o', label = 'Coordenada S en función de B', color = '#0000CC')
plt.plot(B_axis[np.argsort(B_axis)], LMS_blue_fitted[np.argsort(B_axis),0], linewidth = 2.5, color = '#CC0000')
plt.plot(B_axis[np.argsort(B_axis)], LMS_blue_fitted[np.argsort(B_axis),1], linewidth = 2.5, color = '#00CC00')
plt.plot(B_axis[np.argsort(B_axis)], LMS_blue_fitted[np.argsort(B_axis),2], linewidth = 2.5, color = '#0000CC')
#plt.legend(fontsize = 16)
plt.xlabel('Coordenada B', fontsize=16)
plt.ylabel('Coordenadas S,M y L', fontsize=16)
plt.xticks(fontsize = 12)
plt.yticks(fontsize = 12)
plt.grid()
plt.show()


plt.figure(figsize = (8,6))
plt.scatter(G_axis[np.argsort(G_axis)], LMS_green[np.argsort(G_axis),0], marker = 'o', label = 'Coordenada L en función de G', color = '#CC0000')
plt.scatter(G_axis[np.argsort(G_axis)], LMS_green[np.argsort(G_axis),1], marker = 'o', label = 'Coordenada M en función de G', color = '#00CC00')
plt.scatter(G_axis[np.argsort(G_axis)], LMS_green[np.argsort(G_axis),2], marker = 'o', label = 'Coordenada S en función de G', color = '#0000CC')
plt.plot(G_axis[np.argsort(G_axis)], LMS_green_fitted[np.argsort(G_axis),0], linewidth = 2.5, color = '#CC0000')
plt.plot(G_axis[np.argsort(G_axis)], LMS_green_fitted[np.argsort(G_axis),1], linewidth = 2.5, color = '#00CC00')
plt.plot(G_axis[np.argsort(G_axis)], LMS_green_fitted[np.argsort(G_axis),2], linewidth = 2.5, color = '#0000CC')
#plt.legend(fontsize = 16)
plt.xlabel('Coordenada G', fontsize=16)
plt.ylabel('Coordenadas S,M y L', fontsize=16)
plt.xticks(fontsize = 12)
plt.yticks(fontsize = 12)
plt.grid()
plt.show()

plt.figure(figsize = (8,6))
plt.scatter(R_axis[np.argsort(R_axis)], LMS_red[np.argsort(R_axis),0], marker = 'o', label = 'Coordenada L en función de R', color = '#CC0000')
plt.scatter(R_axis[np.argsort(R_axis)], LMS_red[np.argsort(R_axis),1], marker = 'o', label = 'Coordenada M en función de R', color = '#00CC00')
plt.scatter(R_axis[np.argsort(R_axis)], LMS_red[np.argsort(R_axis),2], marker = 'o', label = 'Coordenada S en función de R', color = '#0000CC')
plt.plot(R_axis[np.argsort(R_axis)], LMS_red_fitted[np.argsort(R_axis),0], linewidth = 2.5, color = '#CC0000')
plt.plot(R_axis[np.argsort(R_axis)], LMS_red_fitted[np.argsort(R_axis),1], linewidth = 2.5, color = '#00CC00')
plt.plot(R_axis[np.argsort(R_axis)], LMS_red_fitted[np.argsort(R_axis),2], linewidth = 2.5, color = '#0000CC')
plt.legend(fontsize = 16)
plt.xlabel('Coordenada R', fontsize=16)
plt.ylabel('Coordenadas S,M y L', fontsize=16)
plt.xticks(fontsize = 12)
plt.yticks(fontsize = 12)
plt.grid()
plt.show()

plt.figure(figsize = (8,6))
plt.scatter(RGB_102[np.argsort(RGB_102)], LMS_102[np.argsort(RGB_102),0], marker = 'o', label = 'Coordenada L en función de B', color = '#CC0000')
plt.scatter(RGB_102[np.argsort(RGB_102)], LMS_102[np.argsort(RGB_102),1], marker = 'o', label = 'Coordenada M en función de B', color = '#00CC00')
plt.scatter(RGB_102[np.argsort(RGB_102)], LMS_102[np.argsort(RGB_102),2], marker = 'o', label = 'Coordenada S en función de B', color = '#0000CC')
plt.plot(RGB_102[np.argsort(RGB_102)], LMS_102_fitted[np.argsort(RGB_102),0], linewidth = 2.5,  color = '#CC0000')
plt.plot(RGB_102[np.argsort(RGB_102)], LMS_102_fitted[np.argsort(RGB_102),1], linewidth = 2.5,  color = '#00CC00')
plt.plot(RGB_102[np.argsort(RGB_102)], LMS_102_fitted[np.argsort(RGB_102),2], linewidth = 2.5,  color = '#0000CC')
#plt.legend(fontsize = 1)
plt.xlabel('Coordenada B', fontsize=16)
plt.ylabel('Coordenadas S,M y L', fontsize=16)
plt.xticks(fontsize = 12)
plt.yticks(fontsize = 12)
plt.grid()
plt.show()
