import matplotlib.pyplot as plt

years = [1980, 2040]
population = [62, 109]

plt.bar(years, population, color=['blue', 'red'], linewidth=50)

plt.xticks(years)

plt.xlabel('Año')
plt.ylabel('Población (en millones)')
plt.title('Estimación de Diabetes Mellitus Tipo 2 en las Américas')

plt.savefig('diabetes_mellitus_estimation.png')

plt.clf()
