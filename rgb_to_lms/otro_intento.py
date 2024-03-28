from sklearn.linear_model import LinearRegression
import numpy as np



data = np.loadtxt("rgb_to_lms/rgb_to_lms_R_G_B_L_M_S_data_final.txt", skiprows=1)  # Skip the header row

# Find the maximum value in the entire array
max_value = np.max(data)
# Divide the last three columns by the maximum value
data[:, 3:] /= max_value
np.savetxt("rgb_to_lms/rgb_to_lms_R_G_B_L_M_S_data_final_normalizada.txt", data, delimiter='\t', header="R\tG\tB\tL\tM\tS", comments='')

# Sample data (replace with your actual data)
RGB_original = np.array(data[:, :3])  # First three columns as independent variables (A, B, C)
RGB = RGB_original**[2.23,2.22,2.37]
LMS = np.array(data[:, 3:])
L = np.array(data[:,3])
M = np.array(data[:,4])
S = np.array(data[:,5])

# Create a linear regression model
model_l = LinearRegression()
model_m = LinearRegression()
model_s = LinearRegression()
# Fit the model to the data
model_l.fit(RGB, L)
model_m.fit(RGB, M)
model_s.fit(RGB, S)


# Get the coefficients and intercept
intercept_l = model_l.intercept_
coefficients_l = model_l.coef_

intercept_m = model_m.intercept_
coefficients_m = model_m.coef_

intercept_s = model_s.intercept_
coefficients_s = model_s.coef_

print(f"Intercept: {intercept_l}")
print(f"Coefficients: {coefficients_l}")

print(f"Intercept: {intercept_m}")
print(f"Coefficients: {coefficients_m}")

print(f"Intercept: {intercept_s}")
print(f"Coefficients: {coefficients_s}")

# Predict Y for new data
from sklearn.metrics import r2_score

predicted_L = np.dot(RGB,coefficients_l) + intercept_l
predicted_M = np.dot(RGB,coefficients_m) + intercept_m
predicted_S = np.dot(RGB,coefficients_s) + intercept_s

r2_l = r2_score(L, predicted_L)
print(f"R-squared (R2) Score: {r2_l}")

r2_m = r2_score(M, predicted_M)
print(f"R-squared (R2) Score: {r2_m}")

r2_s = r2_score(S, predicted_S)
print(f"R-squared (R2) Score: {r2_s}")

#S_error = S - predicted_S

# Add a fourth column to RGB_original containing S_error
#RGB_with_error = np.column_stack((RGB_original, S, S_error))

# Save the modified data to a text file
#np.savetxt("rgb_to_lms/rgb_with_S_and_error.txt", RGB_with_error, delimiter='\t', header="R\tG\tB\tS\tS_error", comments='')

# This will save the data with a tab delimiter and a header row.