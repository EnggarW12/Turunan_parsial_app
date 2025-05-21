import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

# Konfigurasi awal
st.set_page_config(page_title="Aplikasi Turunan Parsial", layout="wide")
st.title("📚 Aplikasi Interaktif Turunan Parsial")

# Definisi simbol
x, y = sp.symbols('x y')

# Petunjuk penggunaan
with st.expander("ℹ️ Petunjuk Penggunaan", expanded=False):
    st.write("""
    - Masukkan fungsi dua variabel (format Python), contoh: `x**2 + y**3`
    - Masukkan titik evaluasi (x₀, y₀)
    - Lihat hasil turunan dan visualisasi interaktif
    """)

# Tab layout
tab1, tab2, tab3 = st.tabs(["📝 Input Fungsi", "📊 Hasil Analisis", "📈 Visualisasi"])

with tab1:
    fungsi_str = st.text_input("Masukkan fungsi f(x, y):", "x**2 + y + y**3")
    x0 = st.number_input("Nilai x₀:", value=1.0)
    y0 = st.number_input("Nilai y₀:", value=2.0)

try:
    # Parsing fungsi
    f = sp.sympify(fungsi_str)
    fx = sp.diff(f, x)
    fy = sp.diff(f, y)

    # Evaluasi di titik (x0, y0)
    f_val = float(sp.N(f.subs({x: x0, y: y0})))
    fx_val = float(sp.N(fx.subs({x: x0, y: y0})))
    fy_val = float(sp.N(fy.subs({x: x0, y: y0})))

    with tab2:
        st.subheader("📌 Fungsi dan Turunan Parsial")
        st.latex(f"f(x, y) = {sp.latex(f)}")
        st.latex(f"\\frac{{\\partial f}}{{\\partial x}} = {sp.latex(fx)}")
        st.latex(f"\\frac{{\\partial f}}{{\\partial y}} = {sp.latex(fy)}")

        st.markdown("### 📍 Evaluasi di Titik (x₀, y₀)")
        col1, col2 = st.columns(2)
        col1.metric("Nilai Fungsi", f"{f_val}")
        col2.metric("Gradien", f"({fx_val}, {fy_val})")

    with tab3:
        st.subheader("📊 Grafik Permukaan dan Bidang Singgung")

        # Meshgrid untuk plot
        x_vals = np.linspace(x0 - 2, x0 + 2, 50)
        y_vals = np.linspace(y0 - 2, y0 + 2, 50)
        X, Y = np.meshgrid(x_vals, y_vals)

        # Evaluasi fungsi dan bidang singgung
        f_lamb = sp.lambdify((x, y), f, "numpy")
        Z = f_lamb(X, Y)
        Z_tangent = f_val + fx_val * (X - x0) + fy_val * (Y - y0)

        # Plotting
        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.75)
        ax.plot_surface(X, Y, Z_tangent, color='red', alpha=0.5)
        ax.scatter(x0, y0, f_val, color='black', s=50)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.set_title("Grafik f(x, y) dan bidang singgung di titik (x₀, y₀)")
        st.pyplot(fig)

except Exception as e:
    st.error(f"⚠️ Terjadi kesalahan dalam parsing atau evaluasi fungsi: {e}")
