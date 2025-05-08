import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Heat Transfer by Natural Convection - Virtual Lab")

st.sidebar.header("Input Parameters")

# Constants
g = 9.81  # m/s²
Cp = 1005  # J/kg·K (approx. for air)
k_air = st.sidebar.number_input("Thermal Conductivity of Air (W/m·K)", 0.01, 1.0, 0.0296)
mu_air = st.sidebar.number_input("Dynamic Viscosity of Air (kg/m·s)", 1e-6, 1e-4, 1.846e-5)
rho_air = st.sidebar.number_input("Density of Air (kg/m³)", 0.5, 2.0, 1.1614)
Pr = st.sidebar.number_input("Prandtl Number", 0.1, 2.0, 0.707)

# Tube dimensions
D = st.sidebar.number_input("Diameter of the Tube (m)", 0.01, 0.2, 0.032)
L = st.sidebar.number_input("Length of the Tube (m)", 0.1, 1.5, 0.5)

# Electrical input
V = st.sidebar.number_input("Voltage (V)", 1.0, 250.0, 90.0)
I = st.sidebar.number_input("Current (A)", 0.01, 10.0, 1.5)

# Temperature inputs
st.header("Temperature Inputs")
Ts_values = st.text_input("Enter Surface Temperatures (°C) separated by commas", "85,87,88,86,89")
Ts_list = [float(t) for t in Ts_values.split(",")]
Ta = st.number_input("Ambient Air Temperature (°C)", 10.0, 50.0, 30.0)

# Calculations
Ts_avg = sum(Ts_list) / len(Ts_list)
Tf = (Ts_avg + Ta) / 2
beta = 1 / (Tf + 273.15)  # in 1/K
delta_T = Ts_avg - Ta
A = np.pi * D * L
q = V * I
hexp = q / (A * delta_T)
nu_air = mu_air / rho_air
Gr = (g * beta * delta_T * L**3) / (nu_air**2)
GrPr = Gr * Pr

# Empirical Nusselt number
if 1e4 < GrPr < 1e9:
    Nu = 0.59 * (GrPr)**0.25
elif 1e9 <= GrPr <= 1e12:
    Nu = 0.13 * (GrPr)**0.33
else:
    Nu = 0
    st.warning("Gr.Pr is out of the empirical formula range!")

hemp = (Nu * k_air) / L

# Display results
st.subheader("Results")
st.write(f"Average Surface Temperature, Ts = {Ts_avg:.2f} °C")
st.write(f"Mean Film Temperature, Tf = {Tf:.2f} °C")
st.write(f"Heat Supplied, q = {q:.2f} W")
st.write(f"Heat Transfer Area, A = {A:.5f} m²")
st.write(f"Temperature Difference, ΔT = {delta_T:.2f} °C")
st.write(f"Experimental Heat Transfer Coefficient, hexp = {hexp:.2f} W/m²·K")
st.write(f"Empirical Heat Transfer Coefficient, hemp = {hemp:.2f} W/m²·K")

# Graph
st.subheader("Graph: Heat Transfer Coefficient vs ΔT")
delta_T_range = np.linspace(5, 50, 100)
hexp_vals = q / (A * delta_T_range)
plt.plot(delta_T_range, hexp_vals, label="Experimental")
plt.axhline(hemp, color='r', linestyle='--', label='Empirical Hemp')
plt.xlabel("ΔT (°C)")
plt.ylabel("Heat Transfer Coefficient (W/m²·K)")
plt.title("hexp vs ΔT")
plt.legend()
st.pyplot(plt)
'''

# Save to a file
file_path = "/mnt/data/natural_convection_lab.py"
with open(file_path, "w") as f:
    f.write(streamlit_code)

