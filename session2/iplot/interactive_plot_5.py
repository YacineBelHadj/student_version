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

f= np.arange(0,2,0.002)
H = frequency_response_function(m=init_m,k=init_k,c=init_c,f=f)

wn=calcW_n(k=init_k,m=init_m)
axes[0].semilogy(f,np.abs(H), lw=2, color='lightgray')

line, = axes[0].semilogy(f,np.abs(H), lw=2, color='steelblue')

axes[0].set_xlabel('Frequency (Hz)')
axes[0].set_ylabel('|H(f)|')
axes[0].grid(which='both', linestyle=':')

axes[1].plot(f,np.angle(H,deg=True), color='lightgray')

line2, = axes[1].plot(f,np.angle(H,deg=True), color='steelblue')

axes[1].set_xlabel('Frequency (Hz)')
axes[1].set_ylabel('angle(H(f))')
axes[1].grid(which='both', linestyle=':')

linev1 = axes[0].axvline(convert_pulsation(wn), color='firebrick', linestyle=':')
linev2 = axes[1].axvline(convert_pulsation(wn), color='firebrick', linestyle=':')

# adjust the main plot to make room for the sliders
plt.subplots_adjust(left=0.25, bottom=0.4)

wn=calcW_n(k=init_k,m=init_m)
Xi=calcXi(c=init_c,k=init_k,m=init_m)
wd= wn*np.sqrt(1-Xi**2)

text_wn = plt.text(-43, 0.25, f'$\omega_n$ = {wn:.2f}',
        style ='italic',
        fontsize = 10,
        bbox ={'facecolor':'green',
            'alpha':0.6, 'pad':2})

text_Xi = plt.text(-43, 0.2, f'$ \\xi $ = {Xi*100:.2f}%',
        style ='italic',
        fontsize = 10,
        bbox ={'facecolor':'green',
            'alpha':0.6, 'pad':2})

text_wd = plt.text(-43, 0.15, f'$ \omega_d $ = {wd:.2f}',
        style ='italic',
        fontsize = 10,
        bbox ={'facecolor':'green',
            'alpha':0.6, 'pad':2})

axmass = plt.axes([0.25, 0.1, 0.65, 0.03])
m_slider = Slider(
    ax=axmass,
    label='Mass (kg)',
    valmin=0.1,
    valmax=30,
    valinit=init_m,
)
axstifness=plt.axes([0.25, 0.15, 0.65, 0.03])
k_slider = Slider(
    ax=axstifness,
    label="Stifness (N/m)",
    valmin=0,
    valmax=20,
    valinit=init_k,
)
axc = plt.axes([0.25, 0.2, 0.65, 0.03])
c_slider = Slider(
    ax=axc,
    label="damping (N/(m*s))",
    valmin=0.01,
    valmax=1,
    valinit=init_c,
)



# The function to be called anytime a slider's value changes
def update(fixed):
    h =frequency_response_function(m=m_slider.val,k=k_slider.val,c=c_slider.val,f=f)
    
    line.set_ydata(np.abs(h))
    line2.set_ydata(np.angle(h, deg=True))

    Xi=calcXi(c=c_slider.val,k=k_slider.val,m=m_slider.val)
    wn=calcW_n(k=k_slider.val,m=m_slider.val)
    wd= calcW_d(xi=Xi, w_n=wn)
    
    linev2.set_xdata(convert_pulsation(wd))
    linev1.set_xdata(convert_pulsation(wd))


    text_wn.set_text(f'$\omega_n$ = {convert_pulsation(wn):.2f}Hz')
    text_Xi.set_text(f'$ \\xi $ = {Xi*100:.2f}%')
    text_wd.set_text(f'$ \omega_d $ = {convert_pulsation(wd):.2f}Hz')
    
   
    fig.canvas.draw_idle()

# register the update function with each slider
m_slider.on_changed(update)
k_slider.on_changed(update)
c_slider.on_changed(update)


# Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', hovercolor='0.975')


def reset(event):
    m_slider.reset()
    k_slider.reset()
    c_slider.reset()
button.on_clicked(reset)

w = interact(update(fixed))