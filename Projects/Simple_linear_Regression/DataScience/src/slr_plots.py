"""Basic plots for the simple regression notebook."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('default')


def plot_fit(data, model):
    """Plot the observations and the fitted line."""
    hours = np.linspace(data['pt3b'].min(), data['pt3b'].max(), 100)
    fitted = model.params.iloc[0] + model.params.iloc[1] * hours
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.scatter(data['pt3b'], data['ingrl'], s=10, alpha=0.2)
    ax.plot(hours, fitted, color='black', label='Recta MCO')
    ax.set(xlabel='Horas de internet', ylabel='Ingreso mensual (USD)', title='Ajuste del modelo')
    ax.legend()
    fig.tight_layout()
    plt.show()


def plot_residuals(data, model):
    """Plot residuals and their dispersion by hours."""
    residuals = pd.DataFrame({'horas': data['pt3b'], 'residuo': model.resid})
    spread = residuals.groupby('horas')['residuo'].agg(['size', 'std'])
    spread = spread.loc[spread['size'] >= 30]
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.5))
    axes[0].scatter(model.fittedvalues, model.resid, s=10, alpha=0.2)
    axes[0].axhline(0, color='black', linestyle='--')
    axes[0].set(xlabel='Ingreso ajustado', ylabel='Residuo', title='Residuos')
    axes[1].plot(spread.index, spread['std'], 'o-')
    axes[1].set(xlabel='Horas de internet', ylabel='Desviación residual (USD)',
                title='Dispersión por horas (n ≥ 30)')
    fig.tight_layout()
    plt.show()


def plot_influence(model):
    """Plot leverage, standardized residuals, and Cook's distance."""
    influence = model.get_influence()
    cook = influence.cooks_distance[0]
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.5))
    axes[0].scatter(influence.hat_matrix_diag, influence.resid_studentized_internal,
                    s=10, alpha=0.2)
    axes[0].axhline(3, color='black', linestyle='--')
    axes[0].axhline(-3, color='black', linestyle='--')
    axes[0].set(xlabel='Apalancamiento', ylabel='Residuo estandarizado', title='Observaciones extremas')
    axes[1].scatter(np.arange(len(cook)), cook, s=8, alpha=0.3)
    axes[1].axhline(4 / len(cook), color='black', linestyle='--', label='4/n')
    axes[1].set_yscale('log')
    axes[1].set(xlabel='Posición en la muestra', ylabel='Distancia de Cook', title='Influencia')
    axes[1].legend()
    fig.tight_layout()
    plt.show()
