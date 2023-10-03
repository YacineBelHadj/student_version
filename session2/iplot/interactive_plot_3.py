from iplot.utils import *
import matplotlib.pyplot as plt
import numpy as np
from ipywidgets import interact, fixed
from matplotlib.widgets import Slider, Button
# Define initial parameters
init_m =m=1
init_k =k= 16
init_c =c= 0.1

f_init = 0.64

# Create the figure and the line that we will manipulate
fig, axes = plt.subplots(1,2)

t = np.arange(start=0,stop=100,step=0.1)
response = harmonic_response(m=m, c=c, k=k, f=f_init, t=t)

force = harmonic_force(f=f_init, t=t)


f= np.arange(0,2,0.002)
H = frequency_response_function(m=m,c=c,k=k,f=f)

line, = axes[0].plot(t,response, lw=2)

axes[0].set_xlabel('Time (s)')
axes[0].set_ylabel('x(t)')
axes[0].grid(which='both', linestyle=':')

response = harmonic_response(m=m, c=c, k=k, f=f_init, t=t)
axes[1].semilogy(f,np.abs(H))

red_dot, = axes[1].semilogy(
    f_init,
    np.abs(frequency_response_function(m=m,c=c,k=k,f=f_init)),
    marker='.',
    markersize=10,
    color='firebrick')

axes[1].set_xlabel('Frequency (Hz)')
axes[1].set_ylabel('|H(f)|')
axes[1].grid(which='both', linestyle=':')

# adjust the main plot to make room for the sliders
plt.subplots_adjust(left=0.1, bottom=0.4)

wn=calcW_n(k=k,m=m)

text_wn = plt.text(-43, 0.25, f'$\omega_n$ = {convert_pulsation(wn):.2f}Hz',
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
    response = harmonic_response(m=m, c=c, k=k, f=f_slider.val, t=t)
    val = frequency_response_function(m=m,c=c,k=k,f=f_slider.val)
    line.set_ydata(response)
    red_dot.set_ydata(np.abs(val))
    red_dot.set_xdata(f_slider.val)
    axes[0].set_xlim([80,100])
    axes[0].set_ylim([-25,25])
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
