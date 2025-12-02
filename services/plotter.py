import pandas as pd
import numpy as np
import plotly.graph_objects as go
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
        """Generate a contour plot using Plotly"""
        if len(self.velocidad_valid) < 3:
            return self.generate_scatter_plot()

        # Dynamic range
        zmin = float(np.nanmin(self.eficiencia_valid))
        zmax = float(np.nanmax(self.eficiencia_valid))

        # Avoid flat scale
        if zmin == zmax:
            zmax = zmin + 0.01

        try:
            fig = go.Figure(
                data=go.Contour(
                    x=self.velocidad_valid,
                    y=self.torque_valid,
                    z=self.eficiencia_valid,
                    colorscale="RdYlGn",

                    # 🔥 dynamic contour range
                    zmin=zmin,
                    zmax=zmax,
                    contours=dict(
                        showlabels=True,
                        labelfont=dict(size=10, color="white"),
                        start=zmin,
                        end=zmax,
                        size=(zmax - zmin) / 10,
                    ),

                    colorbar=dict(
                        title="Eficiencia (%)",
                        tickformat=".2f"
                    ),

                    hovertemplate=(
                        "Velocidad: %{x:.2f} RPM<br>"
                        "Torque: %{y:.2f} Nm<br>"
                        "Eficiencia: %{z:.3f}%<br>"
                        "<extra></extra>"
                    ),
                )
            )

            fig.update_layout(
                title=dict(
                    text="Mapa de Eficiencia del Motor",
                    x=0.5,
                    xanchor="center",
                ),
                xaxis_title="Velocidad (RPM)",
                yaxis_title="Torque (Nm)",
                template="plotly_white",
                width=1000,
                height=600
            )

            return fig

        except Exception as e:
            print("Plot error:", e)
            return self.generate_scatter_plot()

    def generate_scatter_plot(self):
        """Generate scatter plot as fallback"""
        fig = go.Figure(
            data=go.Scatter(
                x=self.velocidad_valid,
                y=self.torque_valid,
                mode="markers",
                marker=dict(
                    size=8,
                    color=self.eficiencia_valid,
                    colorscale="RdYlGn",
                    colorbar=dict(title="Eficiencia (%)"),
                    showscale=True,
                ),
                hovertemplate=(
                        "Velocidad: %{x:.2f} RPM<br>"
                        + "Torque: %{y:.2f} Nm<br>"
                        + "Eficiencia: %{marker.color:.2f}%<br>"
                        + "<extra></extra>"
                ),
            )
        )

        fig.update_layout(
            title={
                "text":"Mapa de Eficiencia del Motor (Scatter Plot)",
                "x":0.5,
                "xanchor":"center",
            },
            xaxis_title="Velocidad (RPM)",
            yaxis_title="Torque (Nm)",
            width=1000,
            height=600,
            template="plotly_white",
            font=dict(size=12),
        )

        return fig

    def generate_plot_image(self, plot_type="contour"):
        """Generate plot and return as PNG bytes"""
        if plot_type == "contour":
            fig = self.generate_contour_plot()
        else:
            fig = self.generate_scatter_plot()

        # Convert to PNG bytes
        image_bytes = fig.to_image(format="png", width=1000, height=600, scale=2)
        return image_bytes

    def generate_plot_html(self, plot_type="contour"):
        """Generate plot and return as HTML string (for web embedding)"""
        if plot_type == "contour":
            fig = self.generate_contour_plot()
        else:
            fig = self.generate_scatter_plot()

        return fig.to_html(include_plotlyjs="cdn", full_html=False)


def fetch_test_info(db):
    return db.query(TestInfo).all()
