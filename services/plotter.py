import pandas as pd
import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.tri as tri


from models.scadalts import TestInfo
from sqlalchemy import text


class EfficiencyPlot:
    def __init__(self, db, test_id):
        self.db = db
        self.test_id = test_id
        self.df = self.execute_query(self.db, self.test_id)
        self.velocidad_valid, self.torque_valid, self.eficiencia_valid = (
            self.data_transformation()
        )

    def execute_query(self, db, test_id):
        query_sql = text("CALL dyno_test(:tid)")
        df = pd.read_sql(query_sql, db.bind, params={"tid": test_id})
        return df

    def data_transformation(self):
        """Transform and clean the data for plotting"""
        # Use linear interpolation for missing values
        corriente = (
            self.df["meta_corriente_1"]
            .interpolate(method="linear", limit_direction="both")
            .astype(float)
            .to_numpy()
        )
        voltaje = (
            self.df["meta_lv25p_1"]
            .interpolate(method="linear", limit_direction="both")
            .astype(float)
            .to_numpy()
        )
        torque = (
            self.df["meta_peso_2"]
            .interpolate(method="linear", limit_direction="both")
            .astype(float)
            .to_numpy()
        )
        velocidad = (
            self.df["meta_encoder"]
            .interpolate(method="linear", limit_direction="both")
            .astype(float)
            .to_numpy()
        )

        # Calculate mechanical and electrical power
        potencia_mecanica = (2 * np.pi * velocidad * torque) / 60
        potencia_electrica = voltaje * corriente

        # Avoid division by zero
        potencia_electrica = potencia_electrica.astype(float)
        potencia_electrica[potencia_electrica == 0] = np.nan

        # Calculate efficiency
        eficiencia = (potencia_mecanica / potencia_electrica) * 100

        # Filter valid data
        mask_valid = (
                ~np.isnan(eficiencia)
                & ~np.isinf(eficiencia)
                & (eficiencia >= 0)
                & (eficiencia <= 100)
        )

        velocidad_valid = velocidad[mask_valid]
        torque_valid = torque[mask_valid]
        eficiencia_valid = eficiencia[mask_valid]

        print(f"Valid data points for plotting: {len(velocidad_valid)}")
        return velocidad_valid, torque_valid, eficiencia_valid

    def generate_contour_plot(self):
        if len(self.velocidad_valid) < 3:
            raise ValueError(f"Not enough data points, {len(self.velocidad_valid)}")

        velocidad_valid = self.velocidad_valid
        torque_valid = self.torque_valid
        eficiencia_valid = self.eficiencia_valid

        # Create figure
        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111)

        # Triangulation and interpolation
        triang = tri.Triangulation(velocidad_valid, torque_valid)
        interpolador = tri.LinearTriInterpolator(triang, eficiencia_valid)

        X, Y = np.meshgrid(
            np.linspace(min(velocidad_valid), max(velocidad_valid), 100),
            np.linspace(min(torque_valid), max(torque_valid), 100)
        )

        Z = interpolador(X, Y)

        # Filled contour
        contour = ax.contourf(X, Y, Z, levels=15, cmap="RdYlGn")

        # Contour lines
        lines = ax.contour(X, Y, Z, levels=15, colors="black", linewidths=0.5)
        ax.clabel(lines, inline=True, fontsize=8, fmt="%d")

        # Labels & settings exactly like your script
        ax.set_xlabel("Velocidad (RPM)")
        ax.set_ylabel("Torque (Nm)")
        ax.set_title("Mapa de Eficiencia del Motor")
        ax.grid(True)

        fig.colorbar(contour).set_label("Eficiencia (%)")
        fig.tight_layout()

        return fig

    def generate_plot_image(self, plot_type="contour"):
        if plot_type == "contour":
            fig = self.generate_contour_plot()

        import io
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=150)
        plt.close(fig)
        buf.seek(0)
        return buf.getvalue()


def fetch_test_info(db):
    return db.query(TestInfo).all()
