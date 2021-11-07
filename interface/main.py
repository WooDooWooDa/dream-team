import numpy as np
import math
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
import matplotlib
import matplotlib.pyplot as plt
import functions as fct
matplotlib.use("TkAgg")

#plot value
y = [-10, 10]
x = [-10, 10]
posx = 0
posy = 0
a = 2
b = 4


def delete_fig_agg(fig):
    fig.forget()
    plt.close('all')


def graph():
    fct.posArray = np.array([[fct.x - posx, fct.y - posy, fct.z] for fct.x in np.arange(-1.5, 1.5, 0.2) for fct.y in np.arange(-1.5, 1.5, 0.2) for fct.z in range(1, 3)])
    fig = matplotlib.figure.Figure(figsize=(50, 30), dpi=20)
    axes = fig.add_axes([0, 0, 1, 1])

    elecprime_list = np.array([fct.champ_elecprime(vec[0], vec[1], vec[2]) for vec in fct.posArray])
    x_list = elecprime_list[:, 0]
    y_list = elecprime_list[:, 1]
    colors = elecprime_list[:, 2]
    plt.set_cmap("Oranges_r")

    axes.axhline(y=0, color='k')
    axes.axvline(x=0, color='k')
    axes.quiver(fct.posArray[:, 0], fct.posArray[:, 1], x_list, y_list, colors, units="xy")
    return fig


def create_plot():
    fig = matplotlib.figure.Figure(figsize=(4, 4), dpi=100)
    t = np.arange(x[0], x[1], .01)  # X axis
    fig.add_subplot(111).plot(t, np.sin(a * t) * b + y[1])
    return fig


def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg


sliderY = sg.Slider(range=(y[0], y[1]), default_value=(y[0] + y[1]), orientation="vertical",
                    enable_events=True, key="sliderY", expand_y=True)
sliderX = sg.Slider(range=(x[0], x[1]), default_value=(x[0] + x[1]), orientation="horizontal",
                    enable_events=True, key="sliderX", expand_x=True)

render_graph = [
    [sg.Text("Graph Render")],
    [sg.Canvas(key="-CANVAS-"), sliderY],
    [sliderX],
    [sg.HSeparator()],
    [sg.Button("Quit simulation", expand_x=True, key="Quit")]
]

sliderA = sg.Slider(range=(1, 99), orientation="horizontal", enable_events=True, key="sliderA")
sliderB = sg.Slider(range=(1, 10), orientation="horizontal", enable_events=True, key="sliderB")

options = [
    [sg.Text("V parameter :"), sliderA]
]

# Define the window layout
layout = [
    [
        sg.Column(render_graph),
        sg.VSeperator(),
        sg.Column(options),
    ]
]

# Create the form and show it without the plot
window = sg.Window(
    "Relativist Electromagnetic Field",
    layout,
    location=(0, 0),
    finalize=True
)

fig_agg = None

while True:
    if fig_agg is not None:
        delete_fig_agg(fig_agg.get_tk_widget())
    fig_agg = draw_figure(window["-CANVAS-"].TKCanvas, graph())

    posx += 0.01
    if posx >= 1:
        posx = -1
    event, values = window.read(timeout=0.01)

    if event == "sliderA" or event == "sliderX" or event == "sliderY":
        posx = values['sliderX'] / 10
        posy = values['sliderY'] / 10
        fct.V = values['sliderA'] / 100

    if event == "Quit" or event == sg.WIN_CLOSED:
        break

window.close()
