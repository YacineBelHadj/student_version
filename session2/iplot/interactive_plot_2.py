import numpy as np
from iplot.utils import *
import matplotlib.pyplot as plt
from ipywidgets import interact, fixed
from matplotlib.widgets import Slider, Button




# Define initial parameters
init_m =1
init_k = 16
init_c = 0.1

f_init = 0.64

# Create the figure and the line that we will manipulate
fig, ax = plt.subplots(2,1, sharex=True)

t = np.arange(start=0,stop=100,step=0.02)
f = harmonic_force(f=f_init, t=t)
response = harmonic_response(m=init_m, c=init_c, k=init_k, f=f_init, t=t)
line, = ax[1].plot(t,response, lw=2)
line_f, = ax[0].plot(t,f, lw=2)

ax[0].set_ylabel('f(t)')
ax[0].grid(which='both', linestyle=':')


ax[1].set_xlabel('Time (s)')
ax[1].set_ylabel('x(t)')
ax[1].grid(which='both', linestyle=':')

# adjust the main plot to make room for the sliders
plt.subplots_adjust(left=0.25, bottom=0.3)

wn=calcW_n(k=init_k,m=init_m)

text_wn = plt.text(-43, 0.25, f'f = {convert_pulsation(wn):.2f}Hz',
        style ='italic',
        fontsize = 10,
        bbox ={'facecolor':'green',
            'alpha':0.6, 'pad':2})

    

axmass = plt.axes([0.25, 0.1, 0.65, 0.03])
f_slider = Slider(
    ax=axmass,
    label='f (Hz)',
    valmin=0.1,
    valmax=2,
    valinit=init_m,
)



# The function to be called anytime a slider's value changes
def update(fixed):
    response = harmonic_response(m=init_m, c=init_c, k=init_k, f=f_slider.val, t=t)
    f = harmonic_force(f=f_slider.val, t=t)

    ax[1].relim()
    ax[1].autoscale_view()

    line.set_ydata(response)
    line_f.set_ydata(f)

    fig.canvas.draw_idle()

# register the update function with each slider
f_slider.on_changed(update)


# Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', hovercolor='0.975')


def reset(event):
    f_slider.reset()
button.on_clicked(reset)

w = interact(update(fixed))