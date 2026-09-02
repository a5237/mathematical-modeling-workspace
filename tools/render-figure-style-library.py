#!/usr/bin/env python3
"""Render reproducible synthetic references for scientific-figure aesthetics."""

from __future__ import annotations

import os
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
MPL_CONFIG_DIR = WORKSPACE_ROOT / "var" / "tmp" / "matplotlib"
MPL_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPL_CONFIG_DIR))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import TwoSlopeNorm
from PIL import Image, ImageDraw, ImageFont


OUTPUT_DIR = WORKSPACE_ROOT / "resources" / "figure-style-library" / "references"
RNG = np.random.default_rng(20260828)

BLUE = "#356AA0"
ORANGE = "#C96A4B"
GREEN = "#4C8C72"
PURPLE = "#7B6BA8"
INK = "#30343B"
MUTED = "#6F7782"
GRID = "#E4E8ED"


def configure_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 9,
            "axes.labelsize": 9,
            "axes.titlesize": 9,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            "legend.fontsize": 8,
            "axes.edgecolor": INK,
            "axes.labelcolor": INK,
            "xtick.color": INK,
            "ytick.color": INK,
            "text.color": INK,
            "axes.linewidth": 0.8,
            "xtick.major.width": 0.7,
            "ytick.major.width": 0.7,
            "xtick.major.size": 3.2,
            "ytick.major.size": 3.2,
            "legend.frameon": False,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "savefig.facecolor": "white",
            "savefig.bbox": "tight",
            "savefig.pad_inches": 0.08,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )


def polish_axis(ax: plt.Axes, *, grid: str | None = "y") -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(direction="out")
    if grid:
        ax.grid(axis=grid, color=GRID, linewidth=0.65, zorder=0)
    ax.set_axisbelow(True)


def panel_label(ax: plt.Axes, label: str) -> None:
    ax.text(
        -0.12,
        1.04,
        label,
        transform=ax.transAxes,
        fontsize=10,
        fontweight="bold",
        va="bottom",
    )


def save(fig: plt.Figure, filename: str) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_DIR / filename, dpi=220)
    plt.close(fig)


def render_line_uncertainty() -> None:
    x = np.linspace(0, 12, 60)
    mean_a = 0.62 + 0.26 * (1 - np.exp(-x / 3.2))
    mean_b = 0.58 + 0.23 * (1 - np.exp(-x / 4.6))
    width_a = 0.025 + 0.012 * np.exp(-x / 4)
    width_b = 0.03 + 0.009 * np.exp(-x / 5)

    fig, ax = plt.subplots(figsize=(6.6, 3.8), constrained_layout=True)
    ax.fill_between(x, mean_a - width_a, mean_a + width_a, color=BLUE, alpha=0.15, linewidth=0)
    ax.fill_between(x, mean_b - width_b, mean_b + width_b, color=ORANGE, alpha=0.14, linewidth=0)
    ax.plot(x, mean_a, color=BLUE, linewidth=1.8, label="Method A")
    ax.plot(x, mean_b, color=ORANGE, linewidth=1.7, linestyle="--", label="Method B")
    ax.axhline(0.80, color=MUTED, linewidth=0.9, linestyle=(0, (3, 3)), label="Reference")
    ax.set(xlabel="Time (h)", ylabel="Response (a.u.)", xlim=(0, 12), ylim=(0.54, 0.94))
    ax.legend(loc="lower right", ncol=1, handlelength=2.6)
    ax.text(0.02, 0.96, "Bands show 95% intervals", transform=ax.transAxes, color=MUTED, va="top", fontsize=7.5)
    polish_axis(ax)
    save(fig, "01-line-uncertainty.png")


def render_scatter_fit() -> None:
    x = np.linspace(0.4, 9.6, 72)
    y_true = 1.15 + 0.56 * x
    noise = RNG.normal(0, 0.5 + 0.025 * x, size=x.size)
    y = y_true + noise
    fit = np.polyfit(x, y, 1)
    y_hat = np.polyval(fit, x)
    band = 0.34 + 0.018 * np.abs(x - x.mean())

    fig, ax = plt.subplots(figsize=(6.2, 4.0), constrained_layout=True)
    ax.scatter(x, y, s=25, color=BLUE, alpha=0.72, edgecolor="white", linewidth=0.45, zorder=3)
    ax.fill_between(x, y_hat - band, y_hat + band, color=BLUE, alpha=0.13, linewidth=0)
    ax.plot(x, y_hat, color=INK, linewidth=1.45)
    ax.set(xlabel="Predictor, x", ylabel="Observed response, y", xlim=(0, 10))
    ax.text(
        0.04,
        0.94,
        "Linear fit  ·  95% interval",
        transform=ax.transAxes,
        va="top",
        fontsize=8,
        bbox={"boxstyle": "round,pad=0.25", "facecolor": "white", "edgecolor": GRID},
    )
    polish_axis(ax, grid=None)
    save(fig, "02-scatter-fit.png")


def render_estimate_interval() -> None:
    labels = ["Baseline", "Variant A", "Variant B", "Variant C", "Variant D"]
    estimates = np.array([-0.08, 0.18, 0.31, 0.46, 0.64])
    errors = np.array([0.16, 0.13, 0.17, 0.12, 0.15])
    y = np.arange(len(labels))
    colors = [MUTED, BLUE, BLUE, ORANGE, BLUE]

    fig, ax = plt.subplots(figsize=(6.3, 3.8), constrained_layout=True)
    ax.axvline(0, color=MUTED, linewidth=0.9, linestyle=(0, (3, 3)), zorder=1)
    for yi, value, error, color in zip(y, estimates, errors, colors, strict=True):
        ax.plot([value - error, value + error], [yi, yi], color=color, linewidth=1.8, solid_capstyle="round")
        ax.scatter(value, yi, s=39, color=color, edgecolor="white", linewidth=0.6, zorder=3)
    ax.set_yticks(y, labels)
    ax.invert_yaxis()
    ax.set(xlabel="Estimated effect (95% CI)", xlim=(-0.32, 0.9))
    ax.text(0.46, 3, "selected", color=ORANGE, fontsize=7.5, va="bottom", ha="center")
    polish_axis(ax, grid="x")
    save(fig, "03-estimate-interval.png")


def render_distribution() -> None:
    groups = [
        RNG.normal(0.1, 0.72, 34),
        RNG.normal(0.65, 0.58, 34),
        RNG.normal(1.0, 0.82, 34),
    ]
    positions = np.arange(1, 4)
    colors = [BLUE, GREEN, ORANGE]

    fig, ax = plt.subplots(figsize=(6.2, 4.0), constrained_layout=True)
    parts = ax.violinplot(groups, positions=positions, widths=0.72, showextrema=False)
    for body, color in zip(parts["bodies"], colors, strict=True):
        body.set_facecolor(color)
        body.set_edgecolor(color)
        body.set_alpha(0.18)
    for pos, values, color in zip(positions, groups, colors, strict=True):
        jitter = RNG.normal(0, 0.045, len(values))
        ax.scatter(np.full_like(values, pos) + jitter, values, s=18, color=color, alpha=0.58, edgecolor="white", linewidth=0.3)
        quartiles = np.quantile(values, [0.25, 0.5, 0.75])
        ax.plot([pos, pos], [quartiles[0], quartiles[2]], color=INK, linewidth=3.6, solid_capstyle="butt")
        ax.scatter(pos, quartiles[1], color="white", edgecolor=INK, linewidth=0.8, s=30, zorder=4)
    ax.set_xticks(positions, ["Control", "Treatment 1", "Treatment 2"])
    ax.set(ylabel="Measured response (a.u.)", xlim=(0.45, 3.55))
    polish_axis(ax)
    save(fig, "04-distribution.png")


def render_field_panels() -> None:
    x = np.linspace(-3, 3, 140)
    y = np.linspace(-2.4, 2.4, 110)
    xx, yy = np.meshgrid(x, y)
    field = np.exp(-((xx - 0.7) ** 2 + (yy + 0.15) ** 2) / 1.7) - 0.68 * np.exp(
        -((xx + 1.15) ** 2 + (yy - 0.55) ** 2) / 0.9
    )
    norm = TwoSlopeNorm(vmin=-0.66, vcenter=0, vmax=0.96)

    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.25), constrained_layout=True, sharex=True, sharey=True)
    image = axes[0].imshow(
        field,
        extent=[x.min(), x.max(), y.min(), y.max()],
        origin="lower",
        cmap="coolwarm",
        norm=norm,
        aspect="equal",
        interpolation="bilinear",
    )
    axes[1].contourf(xx, yy, field, levels=13, cmap="coolwarm", norm=norm)
    axes[1].contour(xx, yy, field, levels=7, colors=INK, linewidths=0.45, alpha=0.65)
    for ax, label in zip(axes, ["A", "B"], strict=True):
        panel_label(ax, label)
        ax.set(xlabel="x (m)", ylabel="y (m)")
        ax.tick_params(direction="out")
    colorbar = fig.colorbar(image, ax=axes, shrink=0.84, pad=0.025)
    colorbar.set_label("Normalized field")
    colorbar.outline.set_linewidth(0.6)
    save(fig, "05-field-panels.png")


def render_scientific_3d() -> None:
    x = np.linspace(-2.7, 2.7, 75)
    y = np.linspace(-2.7, 2.7, 75)
    xx, yy = np.meshgrid(x, y)
    zz = np.exp(-0.25 * (xx**2 + yy**2)) * np.cos(1.4 * np.sqrt(xx**2 + yy**2))

    fig = plt.figure(figsize=(6.2, 4.6), constrained_layout=True)
    ax = fig.add_subplot(111, projection="3d")
    surface = ax.plot_surface(xx, yy, zz, cmap="viridis", linewidth=0, antialiased=True, alpha=0.94)
    z_floor = float(zz.min() - 0.18)
    ax.contour(xx, yy, zz, zdir="z", offset=z_floor, levels=8, cmap="viridis", linewidths=0.7)
    ax.set(xlabel="x (m)", ylabel="y (m)", zlabel="Response, z", zlim=(z_floor, float(zz.max())))
    ax.view_init(elev=27, azim=-52)
    ax.grid(True, color=GRID, linewidth=0.5)
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.pane.set_facecolor((1, 1, 1, 0))
        axis.pane.set_edgecolor(GRID)
    colorbar = fig.colorbar(surface, ax=ax, shrink=0.62, pad=0.08)
    colorbar.set_label("Response, z")
    colorbar.outline.set_linewidth(0.6)
    save(fig, "06-scientific-3d.png")


def render_composite() -> None:
    fig, axes = plt.subplots(2, 2, figsize=(7.2, 5.2), constrained_layout=True)
    ax_a, ax_b, ax_c, ax_d = axes.flat

    t = np.linspace(0, 8, 60)
    score = 0.25 + 0.68 * (1 - np.exp(-t / 2.2))
    ax_a.plot(t, score, color=BLUE, linewidth=1.7)
    ax_a.axhline(0.85, color=MUTED, linewidth=0.8, linestyle=(0, (3, 3)))
    ax_a.set(xlabel="Iteration (×100)", ylabel="Score")
    polish_axis(ax_a)

    fitted = np.linspace(2, 11, 60)
    residual = RNG.normal(0, 0.32 + 0.018 * fitted, size=fitted.size)
    ax_b.scatter(fitted, residual, s=19, color=GREEN, alpha=0.68, edgecolor="white", linewidth=0.35)
    ax_b.axhline(0, color=MUTED, linewidth=0.85)
    ax_b.set(xlabel="Fitted value", ylabel="Residual")
    polish_axis(ax_b, grid=None)

    cost = np.linspace(1.2, 6.5, 38)
    benefit = 0.92 - 0.56 * np.exp(-0.52 * cost)
    dominated_x = RNG.uniform(1.5, 6.2, 42)
    dominated_y = 0.32 + 0.52 * RNG.random(42) - 0.04 * dominated_x
    ax_c.scatter(dominated_x, dominated_y, s=15, color="#BAC1C9", alpha=0.8, edgecolor="none")
    ax_c.plot(cost, benefit, color=ORANGE, linewidth=1.6)
    ax_c.scatter(cost[::5], benefit[::5], s=24, color=ORANGE, edgecolor="white", linewidth=0.4, zorder=3)
    ax_c.set(xlabel="Cost", ylabel="Benefit")
    polish_axis(ax_c, grid=None)

    parameters = ["p1", "p2", "p3", "p4", "p5"]
    sensitivity = np.array([0.18, -0.11, 0.08, -0.05, 0.03])
    y_pos = np.arange(len(parameters))
    colors = [BLUE if value >= 0 else ORANGE for value in sensitivity]
    ax_d.barh(y_pos, sensitivity, color=colors, height=0.56, alpha=0.86)
    ax_d.axvline(0, color=MUTED, linewidth=0.8)
    ax_d.set_yticks(y_pos, parameters)
    ax_d.invert_yaxis()
    ax_d.set(xlabel="Standardized sensitivity")
    polish_axis(ax_d, grid="x")

    for ax, label in zip(axes.flat, ["A", "B", "C", "D"], strict=True):
        panel_label(ax, label)
    save(fig, "07-multipanel-composite.png")


def render_overview() -> None:
    filenames = [
        "01-line-uncertainty.png",
        "02-scatter-fit.png",
        "03-estimate-interval.png",
        "04-distribution.png",
        "05-field-panels.png",
        "06-scientific-3d.png",
        "07-multipanel-composite.png",
    ]
    images = [Image.open(OUTPUT_DIR / name).convert("RGB") for name in filenames]
    thumb_size = (720, 480)
    margin = 34
    label_height = 34
    canvas = Image.new("RGB", (2 * thumb_size[0] + 3 * margin, 4 * (thumb_size[1] + label_height) + 5 * margin), "white")
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.load_default(size=16)
    for index, (name, source) in enumerate(zip(filenames, images, strict=True)):
        row, col = divmod(index, 2)
        source.thumbnail(thumb_size, Image.Resampling.LANCZOS)
        x = margin + col * (thumb_size[0] + margin) + (thumb_size[0] - source.width) // 2
        y = margin + row * (thumb_size[1] + label_height + margin)
        canvas.paste(source, (x, y))
        draw.text((margin + col * (thumb_size[0] + margin), y + thumb_size[1] + 8), name, fill=INK, font=font)
    canvas.save(OUTPUT_DIR / "overview.png", dpi=(160, 160))


def main() -> int:
    configure_style()
    render_line_uncertainty()
    render_scatter_fit()
    render_estimate_interval()
    render_distribution()
    render_field_panels()
    render_scientific_3d()
    render_composite()
    render_overview()
    print(f"Rendered 8 files in {OUTPUT_DIR.relative_to(WORKSPACE_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
