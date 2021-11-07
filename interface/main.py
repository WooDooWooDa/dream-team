import numpy as np
import math
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")

#plot value
y = [1, 10]
x = [1, 50]
a = 2
b = 4


def delete_fig_agg(fig):
    fig.forget()
    plt.close('all')


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


sliderY = sg.Slider(range=(y[0], y[1]), default_value=y[1], orientation="vertical",
                    enable_events=True, key="sliderY", expand_y=True)
sliderX = sg.Slider(range=(x[0], x[1]), default_value=x[1], orientation="horizontal",
                    enable_events=True, key="sliderX", expand_x=True)

render_graph = [
    [sg.Text("Graph Render")],
    [sg.Canvas(key="-CANVAS-"), sliderY],
    [sliderX],
    [sg.HSeparator()],
    [sg.Button("Quit simulation", expand_x=True, key="Quit")]
]

sliderA = sg.Slider(range=(1, 10), orientation="horizontal", enable_events=True, key="sliderA", )
sliderB = sg.Slider(range=(1, 10), orientation="horizontal", enable_events=True, key="sliderB")

options = [
    [sg.Text("A parameter :"), sliderA],
    [sg.Text("B parameter :"), sg.VSeperator(), sliderB]
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
    fig_agg = draw_figure(window["-CANVAS-"].TKCanvas, create_plot())

    event, values = window.read()

    if event == "sliderA" or event == "sliderB" or event == "sliderX" or event == "sliderY":
        if fig_agg is not None:
            delete_fig_agg(fig_agg.get_tk_widget())
            x[1] = values['sliderX']
            y[1] = values['sliderY']
            a = values['sliderA']
            b = values['sliderB']

    if event == "Quit" or event == sg.WIN_CLOSED:
        break

window.close()
