import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse

subject_s = ["toto", "gasti", "martina", "tade", "herrmaestre", "bauti", "ines"]
k_min_s = [0.3939, 0.576, 0.48625, 0.5975, 0.44, 0.405, 0.43]
k_error_s = [0.025, 0.025, 0.025, 0.025, 0.04, 0.025, 0.025]
h_min_s = [0.0042, 0.0041, 0.0044, 0.0032, 0.0042, 0.0075, 0.008]
h_error_s = [0.0004, 0.00023, 0.0005, 0.00036, 0.0003, 0.0008, 0.0008]

subject_lm = ["martinal", "tade", "ines", "bauti"]
k_min_lm = [1.21, 1.55, 0.86, 0.81]
k_error_lm = [0.025, 0.025, 0.025, 0.025]
h_min_lm = [0.0055, 0.0052, 0.0067, 0.0060]
h_error_lm = [0.0005, 0.0003, 0.0008, 0.0004]

subject_l_minus_m = ["tade", "ines"]
k_min_l_minus_m = [0.62, 0.43]
k_error_l_minus_m = [0.06, 0.02]
h_min_l_minus_m = [0.00142, 0.0028]
h_error_min_l_minus_m = [0.00008, 0.0002]

# Filter arrays for the subject 'tade'
tade_index_s = subject_s.index("tade")
k_min_tade_s = k_min_s[tade_index_s]
k_error_tade_s = k_error_s[tade_index_s]
h_min_tade_s = h_min_s[tade_index_s]
h_error_tade_s = h_error_s[tade_index_s]

tade_index_lm = subject_lm.index("tade")
k_min_tade_lm = k_min_lm[tade_index_lm]
k_error_tade_lm = k_error_lm[tade_index_lm]
h_min_tade_lm = h_min_lm[tade_index_lm]
h_error_tade_lm = h_error_lm[tade_index_lm]

k_min_tade_l_minus_m = k_min_l_minus_m[0]
k_error_tade_l_minus_m = k_error_l_minus_m[0]
h_min_tade_l_minus_m = h_min_l_minus_m[0]
h_error_tade_l_minus_m = h_error_min_l_minus_m[0]

# Filter arrays for the subject 'ines'
ines_index_s = subject_s.index("ines")
k_min_ines_s = k_min_s[ines_index_s]
k_error_ines_s = k_error_s[ines_index_s]
h_min_ines_s = h_min_s[ines_index_s]
h_error_ines_s = h_error_s[ines_index_s]

ines_index_lm = subject_lm.index("ines")
k_min_ines_lm = k_min_lm[ines_index_lm]
k_error_ines_lm = k_error_lm[ines_index_lm]
h_min_ines_lm = h_min_lm[ines_index_lm]
h_error_ines_lm = h_error_lm[ines_index_lm]



#---------------------------------------------------

k_2min_s = [0.48625, 0.5975, 0.405, 0.43]
k_2error_s = [ 0.025, 0.025, 0.025, 0.025]
k_2min_lm = [1.21, 1.55, 0.81, 0.86]
k_2error_lm = [0.025, 0.025, 0.025, 0.025]

plt.figure(figsize=(8, 8))
plt.errorbar(k_2min_s,k_2min_lm, xerr=k_2error_s, yerr= k_2error_lm, markersize = 6, elinewidth=3, fmt = 'o', color = '#7189FF')
plt.title('Comparación de frecuencias espaciales \n óptimas en las direcciones S y L+M', fontsize = 18)
plt.xlabel('Frecuencia espacial óptima en dirección S (1/°)', fontsize=16)
plt.ylabel('Frecuencia espacial óptima en dirección L + M (1/°)', fontsize=16)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend()
plt.grid(True)
plt.show()

#-------------------------------------------------
k_3min_s = [0.5975, 0.43]
k_3error_s = [0.025, 0.025]

fig, ax = plt.subplots(figsize = (8,8))
#plt.figure(figsize=(8, 8))
ax.errorbar(k_3min_s,k_min_l_minus_m, xerr=k_3error_s, yerr= k_error_l_minus_m, markersize = 6, elinewidth=3, fmt = 'o', color = '#D81159')
plt.title('Comparación de frecuencias espaciales \n óptimas en las direcciones S y L-M', fontsize = 18)
plt.xlabel('Frecuencia espacial óptima en dirección S (1/°)', fontsize=16)
plt.ylabel('Frecuencia espacial óptima en dirección L - M (1/°)', fontsize=16)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend()
ax.grid(True)
plt.show()


#-------------------------------------------------
ines_indices_l_minus_m = [i for i, sub in enumerate(subject_l_minus_m) if sub == "ines"]
k_min_ines_l_minus_m = [k_min_l_minus_m[i] for i in ines_indices_l_minus_m]
k_error_ines_l_minus_m = [k_error_l_minus_m[i] for i in ines_indices_l_minus_m]
h_min_ines_l_minus_m = [h_min_l_minus_m[i] for i in ines_indices_l_minus_m]
h_error_ines_l_minus_m = [h_error_min_l_minus_m[i] for i in ines_indices_l_minus_m]







# Filter arrays for the subject 'bauti'
bauti_index_s = subject_s.index("bauti")
k_min_bauti_s = k_min_s[bauti_index_s]
k_error_bauti_s = k_error_s[bauti_index_s]
h_min_bauti_s = h_min_s[bauti_index_s]
h_error_bauti_s = h_error_s[bauti_index_s]

bauti_index_lm = subject_lm.index("bauti")
k_min_bauti_lm = k_min_lm[bauti_index_lm]
k_error_bauti_lm = k_error_lm[bauti_index_lm]
h_min_bauti_lm = h_min_lm[bauti_index_lm]
h_error_bauti_lm = h_error_lm[bauti_index_lm]

# Filter arrays for the subject 'bauti'
martina_index_s = subject_s.index("martina")
k_min_martina_s = k_min_s[martina_index_s]
k_error_martina_s = k_error_s[martina_index_s]
h_min_martina_s = h_min_s[martina_index_s]
h_error_martina_s = h_error_s[martina_index_s]

martina_index_lm = subject_lm.index("martinal")
k_min_martina_lm = k_min_lm[martina_index_lm]
k_error_martina_lm = k_error_lm[martina_index_lm]
h_min_martina_lm = h_min_lm[martina_index_lm]
h_error_martina_lm = h_error_lm[martina_index_lm]


bauti_index_lm = subject_lm.index("bauti")
k_min_bauti_lm = k_min_lm[bauti_index_lm]
k_error_bauti_lm = k_error_lm[bauti_index_lm]
h_min_bauti_lm = h_min_lm[bauti_index_lm]
h_error_bauti_lm = h_error_lm[bauti_index_lm]

# Create scatter plot
plt.figure(figsize=(8, 6))

plt.errorbar(k_min_s, h_min_s, yerr= h_error_s, xerr= k_error_s, fmt='o', color = '#7189FF', markersize = 5, label='Posición del mínimo en la dirección S')
plt.errorbar(k_min_lm, h_min_lm, yerr= h_error_lm, xerr= k_error_lm, fmt='o', color = '#D81159', markersize = 5, label='Posición del mínimo en la dirección L+M')
plt.errorbar(k_min_l_minus_m, h_min_l_minus_m, yerr= h_error_min_l_minus_m, xerr= k_error_l_minus_m, fmt='o', color = '#48A9A6', markersize = 5, label='Posición del mínimo en la dirección L-M')
plt.errorbar(k_min_tade_s, h_min_tade_s,xerr= k_error_tade_s, yerr= h_error_tade_s,fmt = 's', markersize = 7, color = '#7189FF')
plt.errorbar(k_min_tade_lm, h_min_tade_lm, xerr= k_error_tade_lm, yerr= h_error_tade_lm, fmt = 's', markersize = 7, color = '#D81159')
plt.errorbar(k_min_tade_l_minus_m, h_min_tade_l_minus_m, xerr= k_error_tade_l_minus_m, yerr= h_error_tade_l_minus_m, fmt = 's', markersize = 7, color = '#48A9A6')

# Add errorbar plots for 'ines' with a different marker (e.g., triangle)
plt.errorbar(k_min_ines_s, h_min_ines_s, xerr=k_error_ines_s, yerr=h_error_ines_s, fmt='^', markersize = 9, color='#7189FF')
plt.errorbar(k_min_ines_lm, h_min_ines_lm, xerr=k_error_ines_lm, yerr=h_error_ines_lm, fmt='^', markersize = 9, color='#D81159')
plt.errorbar(k_min_ines_l_minus_m, h_min_ines_l_minus_m, xerr=k_error_ines_l_minus_m, yerr=h_error_ines_l_minus_m, fmt='^', markersize = 8, color='#48A9A6')
# Add errorbar plots for 'bauti' with a different marker (e.g., star)
plt.errorbar(k_min_bauti_s, h_min_bauti_s, xerr=k_error_bauti_s, yerr=h_error_bauti_s, fmt='D', markersize = 7.5, color='#7189FF')
plt.errorbar(k_min_bauti_lm, h_min_bauti_lm, xerr=k_error_bauti_lm, yerr=h_error_bauti_lm, fmt='D', markersize = 7.5, color='#D81159')

plt.errorbar(k_min_martina_s, h_min_martina_s, xerr=k_error_martina_s, yerr=h_error_martina_s, fmt='p', markersize = 9, color='#7189FF')
plt.errorbar(k_min_martina_lm, h_min_martina_lm, xerr=k_error_martina_lm, yerr=h_error_martina_lm, fmt='p', markersize = 9, color='#D81159')


# Customize the plot
#plt.title('Ubicación de los mínimos de umbral en diferentes direcciones \n del espacio de colores con fondo [128,128,128]', fontsize = 14)
plt.xlabel('Frecuencia espacial k (1/°)', fontsize=16)
plt.ylabel('Umbral de discriminación h', fontsize=16)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend(fontsize = 14)
plt.grid(True)
plt.show()
# Show the p
