from tkinter.filedialog import askdirectory
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from scipy import signal
import pandas as pd
import argparse
import math

import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__),'../annotator/src'))
from visualization import behavior_colors, draw_box

### SCRIPT PARAMETERS ###
arena = {
    'xmin'      : -0.15,
    'ymin'      : 0,
    'width'     : 0.3,
    'height'    : 0.5,
}

shelter = {
    'xmin'      : -0.15,
    'ymin'      : 0,
    'width'     : 0.160,
    'height'    : 0.120,
}


parser = argparse.ArgumentParser()
parser.add_argument( '--phenotype', required = True )
parser.add_argument( '--figname-modifier', type = str, default = '' )

if __name__ == '__main__':
    args = parser.parse_args()
        
    ### LOAD THE DATA ###
    trajectories_folder = askdirectory( title = "Select folder containing path annotations" )    

    ### PRE-PROCESS THE DATA ###
    animals = []    
    tmax = 1
    for trajectory_file in os.listdir(trajectories_folder):
        trajectory_info = trajectory_file[:-4].split('-')
        phenotype_ = trajectory_info[0]
        sex = trajectory_info[1]
        animal = trajectory_info[2]
        trial = int(trajectory_info[-2].strip('t'))
        if trial > tmax:
            tmax = trial
        
        if phenotype_ == args.phenotype:
            if animal not in animals:
                if sex == 'M':
                    animals.insert(0,animal)
                elif sex == 'F':
                    animals.append(animal)

    trials = [t for t in range(1,tmax+1)] 

    ### VISUALIZE THE DATA ###
    fig, axes = plt.subplots(len(animals),len(trials),squeeze=False,figsize=(len(trials)*1.5,len(animals)*2.5))
    for a,animal in enumerate(animals):
        for t,trial in enumerate(trials):
            for trajectory_file in os.listdir(trajectories_folder):
                if (f'-{animal}-' in trajectory_file) & (f'-t{trial}-' in trajectory_file):
                    tdf = pd.read_csv(os.path.join(trajectories_folder,trajectory_file))
                    trajectory_info = trajectory_file[:-4].split('-')
                    sex = trajectory_info[1]
                    outcome = trajectory_info[5].lower()
                    
                    axes[a,t].plot(tdf['c-xpos'],tdf['c-ypos'],color=behavior_colors[outcome],linewidth=1.5,alpha=0.5)
            if t == 0:
                axes[a,0].set_title(animal)
            
            if a == 0:
                if t == 0:
                    axes[0,t].set_title(f'{animal}, Trial {t+1}')
                else:
                    axes[0,t].set_title(f'Trial {t+1}')

    for ax in axes.ravel():
        draw_box(ax,arena)
        ax.set_xlim(-0.20,0.20)
        ax.set_ylim(0.55,-0.05)
        shelter_patch = plt.Rectangle((shelter['xmin'], shelter['ymin']), shelter['width'], shelter['height'],facecolor=behavior_colors['hide'], alpha=0.5)
        ax.add_patch(shelter_patch)
        ax.set_axis_off()    
    fig.tight_layout()

    ### SAVE THE FIGURE(S) ###
    print('Figures are saved in: analysis-scripts/figs')
    plt.savefig(f'figs/all-trial-paths-{args.phenotype}-{args.figname_modifier}.pdf', format='pdf')
    plt.show()