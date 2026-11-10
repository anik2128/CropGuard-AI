import json
import os
import time
import math

from rich.console import Console, Group
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich.live import Live

from irrigation_ai import analyse_irrigation


console = Console()

SENSOR_FILE = "sensor_data.json"

# Preliminary calibration values
DRY_REFERENCE = 4045
MOIST_REFERENCE = 2122


# ==========================================
# CROP SELECTION
# ==========================================

def get_crop_name():

    console.print(
        Panel(
            "[bold green]CROPGUARD AI[/bold green] "
            "[cyan]| SMART AGRICULTURE SYSTEM[/cyan]\n"
            "[yellow]LIVE HARDWARE MODE[/yellow]",
            border_style="green",
            padding=(0, 1)
        )
    )

    return input("Crop Name: ").strip()


# ==========================================
# READ ESP32 SENSOR DATA
# ==========================================

def read_sensor_data():

    if not os.path.exists(SENSOR_FILE):
        return None

    try:
        with open(SENSOR_FILE, "r") as file:
            data = json.load(file)

        if time.time() - data.get("timestamp", 0) > 8:
            return None

        return data

    except (OSError, json.JSONDecodeError, TypeError):
        return None


# ==========================================
# VALIDATE SENSOR VALUES
# ==========================================

def valid_number(value):

    try:
        number = float(value)

        if math.isfinite(number):
            return number

    except (ValueError, TypeError):
        pass

    return None


# ==========================================
# SOIL MOISTURE ESTIMATION
# ==========================================

def estimate_moisture(raw_value):

    percentage = (
        (DRY_REFERENCE - raw_value)
        / (DRY_REFERENCE - MOIST_REFERENCE)
    ) * 100

    return round(max(0, min(100, percentage)), 1)


# ==========================================
# ENVIRONMENTAL RISK
# ==========================================

def calculate_environmental_risk(data):

    temperature = data["air_temperature"]
    humidity = data["humidity"]

    score = 0

    if temperature >= 35:
        score += 30

    if humidity >= 80:
        score += 40

    elif humidity >= 70:
        score += 20

    score = min(score, 100)

    if score >= 60:
        level = "HIGH"

    elif score >= 30:
        level = "MODERATE"

    else:
        level = "LOW"

    return score, level


# ==========================================
# COMPACT DASHBOARD
# ==========================================

def make_dashboard(crop_name, data):

    if data is None:

        return Panel(
            "[bold red]ESP32 OFFLINE[/bold red]\n"
            "Waiting for sensor data...",
            title="CROP GUARD AI",
            border_style="red",
            padding=(0, 1)
        )

    air = valid_number(data.get("air_temperature"))
    hum = valid_number(data.get("humidity"))
    soil_temp = valid_number(data.get("soil_temperature"))
    raw = valid_number(data.get("soil_moisture_raw"))

    moisture = (
        estimate_moisture(raw)
        if raw is not None else None
    )

    # ----------------------------------
    # ENVIRONMENT PANEL
    # ----------------------------------

    env = Table.grid(padding=(0, 1))
    env.add_column(style="cyan")
    env.add_column(style="bold green")

    env.add_row(
        "Air",
        f"{air:.1f} C" if air is not None else "ERR"
    )

    env.add_row(
        "Humidity",
        f"{hum:.1f} %" if hum is not None else "ERR"
    )

    env.add_row(
        "Soil Temp",
        f"{soil_temp:.1f} C"
        if soil_temp is not None else "ERR"
    )

    env.add_row(
        "Moisture",
        f"{moisture:.1f} %"
        if moisture is not None else "ERR"
    )

    env.add_row(
        "ADC",
        str(int(raw)) if raw is not None else "ERR"
    )

    env_panel = Panel(
        env,
        title="[cyan]ENVIRONMENT[/cyan]",
        border_style="cyan",
        padding=(0, 1)
    )

    # ----------------------------------
    # SOIL INTELLIGENCE
    # ----------------------------------

    soil = Table.grid(padding=(0, 1))
    soil.add_column(style="cyan")
    soil.add_column(style="yellow")

    soil.add_row("pH", "N/A")
    soil.add_row("Nitrogen", "N/A")
    soil.add_row("Phosphorus", "N/A")
    soil.add_row("Potassium", "N/A")
    soil.add_row("Organic C", "N/A")

    soil_panel = Panel(
        soil,
        title="[green]SOIL INTELLIGENCE[/green]",
        border_style="green",
        padding=(0, 1)
    )

    # ----------------------------------
    # CROP SUITABILITY
    # ----------------------------------

    crop_panel = Panel(
        f"[yellow]{crop_name or 'General Analysis'}[/yellow]\n"
        "[red]ANALYSIS LIMITED[/red]\n"
        "[dim]pH and NPK unavailable[/dim]",
        title="[magenta]CROP SUITABILITY[/magenta]",
        border_style="magenta",
        padding=(0, 1)
    )

    # ----------------------------------
    # IRRIGATION
    # ----------------------------------

    if moisture is not None:

        irrigation = analyse_irrigation({
            "soil_moisture": moisture
        })

        irrigation_text = (
            f"[yellow]{irrigation['status']}[/yellow]\n"
            f"Priority: {irrigation['priority']}\n"
            f"{irrigation['action']}"
        )

    else:

        irrigation_text = "Waiting for sensor"

    irrigation_panel = Panel(
        irrigation_text,
        title="[cyan]SMART IRRIGATION[/cyan]",
        border_style="blue",
        padding=(0, 1)
    )

    # ----------------------------------
    # ENVIRONMENTAL RISK
    # ----------------------------------

    if air is not None and hum is not None:

        score, level = calculate_environmental_risk({
            "air_temperature": air,
            "humidity": hum
        })

        risk_text = (
            f"[yellow]{level}[/yellow] "
            f"{score}/100"
        )

    else:

        risk_text = "Waiting for readings"

    risk_panel = Panel(
        risk_text,
        title="[yellow]ENVIRONMENTAL RISK[/yellow]",
        border_style="yellow",
        padding=(0, 1)
    )

    # ----------------------------------
    # SYSTEM STATUS
    # ----------------------------------

    status_panel = Panel(
        "[green]ESP32: ONLINE[/green]\n"
        "[green]USB: ACTIVE[/green]\n"
        "[green]SENSORS: LIVE[/green]",
        title="SYSTEM STATUS",
        border_style="green",
        padding=(0, 1)
    )

    # ----------------------------------
    # HEADER
    # ----------------------------------

    header = Panel(
        "[bold green]C R O P G U A R D   A I[/bold green] "
        "[cyan]| LIVE SYSTEM[/cyan]",
        border_style="green",
        padding=(0, 1)
    )

    # ----------------------------------
    # FINAL COMPACT LAYOUT
    # ----------------------------------

    return Group(
        header,

        Columns(
            [env_panel, soil_panel],
            equal=True,
            expand=True
        ),

        Columns(
            [crop_panel, irrigation_panel],
            equal=True,
            expand=True
        ),

        Columns(
            [risk_panel, status_panel],
            equal=True,
            expand=True
        )
    )


# ==========================================
# MAIN APPLICATION
# ==========================================

def dashboard():

    crop_name = get_crop_name()

    console.print(
        "\n[bold cyan]Initializing CropGuard AI...[/bold cyan]"
    )

    time.sleep(1)

    try:

        with Live(
            console=console,
            refresh_per_second=2,
            screen=False
        ) as live:

            while True:

                data = read_sensor_data()

                dashboard_view = make_dashboard(
                    crop_name,
                    data
                )

                live.update(dashboard_view)

                time.sleep(1)

    except KeyboardInterrupt:

        console.print(
            "\n[bold yellow]CROPGUARD AI SHUTDOWN[/bold yellow]"
        )


# ==========================================
# START APPLICATION
# ==========================================

if __name__ == "__main__":
    dashboard()