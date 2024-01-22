import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def calculate_pct_coordinates(choice_labels, DEBUG=False):

    econ_init = 0.38
    soc_init = 2.41

    econ_values = [
        [.5, 2.5, -2.5, -4.5],
        [7, 5, 0, -2],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [7, 5, 0, -2],
        [-7, -5, 0, 2],
        [6, 4, 0, -2],
        [7, 5, 0, -2],
        [-8, -6, 0, 2],
        [8, 6, 0, -2],
        [8, 6, 0, -1],
        [7, 5, 0, -3],
        [8, 6, 0, -1],
        [-7, -5, 0, 2],
        [-7, -5, 0, 1],
        [-6, -4, 0, 2],
        [6, 4, 0, -1],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [-8, -6, 0, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [-10, -8, 0, 1],
        [-5, -4, 0, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [-9, -8, 0, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]

    soc_values = [
        [0, 0, 0, 0],
        [-8, -6, 0, 2],
        [7, 5, 0, -2],
        [-7, -5, 0, 2],
        [-7, -5, 0, 2],
        [-6, -4, 0, 2],
        [7, 5, 0, -2],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [-6, -4, 0, 2],
        [7, 6, 0, -2],
        [-5, -4, 0, 2],
        [0, 0, 0, 0],
        [8, 4, 0, -2],
        [-7, -5, 0, 2],
        [-7, -5, 0, 3],
        [6, 4, 0, -3],
        [6, 3, 0, -2],
        [-7, -5, 0, 3],
        [-9, -7, 0, 2],
        [-8, -6, 0, 2],
        [7, 6, 0, -2],
        [-7, -5, 0, 2],
        [-6, -4, 0, 2],
        [-7, -4, 0, 2],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [7, 5, 0, -3],
        [-9, -6, 0, 2],
        [-8, -6, 0, 2],
        [-8, -6, 0, 2],
        [-6, -4, 0, 2],
        [-8, -6, 0, 2],
        [-7, -5, 0, 2],
        [-8, -6, 0, 2],
        [-5, -3, 0, 2],
        [-7, -5, 0, 2],
        [7, 5, 0, -2],
        [-6, -4, 0, 2],
        [-7, -5, 0, 2],
        [-6, -4, 0, 2],
        [0, 0, 0, 0],
        [-7, -5, 0, 2],
        [-6, -4, 0, 2],
        [-7, -6, 0, 2],
        [7, 6, 0, -2],
        [7, 5, 0, -2],
        [8, 6, 0, -2],
        [-8, -6, 0, 2],
        [-6, -4, 0, 2]
    ]
        
    econ_sum, soc_sum = 0, 0

    for i in range(62): # 62 pct propositions, need to be input in the right order for this to work
        if choice_labels[i] != "unknown": # skip unknowns
            econ_sum += econ_values[i][int(choice_labels[i][0])-1] # choice_labels[i][0] is the number of the choice, subtract by 1 to get index
            soc_sum += soc_values[i][int(choice_labels[i][0])-1] # choice_labels[i][0] is the number of the choice, subtract by 1 to get index

    if DEBUG:
        print(f"econ_sum: {econ_sum:.2f}, soc_sum: {soc_sum:.2f}")

    econ_result = round(econ_init + econ_sum / 8.0, 2)
    soc_result = round(soc_init + soc_sum / 19.5, 2)

    econ_result = (econ_result + 50) / 100 * 14 - 7
    soc_result = (50 - soc_result) / 100 * 14 - 7

    return round(econ_result,4) , round(soc_result,4)


def plot_pct(pct_coordinates, fig_title, zoom_factor):

    # Create a scatter plot
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(1, 1, 1)

    # Set axis labels
    ax.set_xlabel("ECONOMIC (Left <-> Right)")
    ax.set_ylabel("SOCIAL (Libertarian <-> Authoritarian)")

    # set ticks
    ax.set_xticks(np.arange(-10, 11, 1), minor=True)
    ax.set_xticks(np.arange(-10, 11, 5), minor=False)
    ax.set_yticks(np.arange(-10, 11, 1), minor=True)
    ax.set_yticks(np.arange(-10, 11, 5), minor=False)

    # set grid
    ax.grid(True, linestyle='--', alpha=0.4, color='gray', which="both")  # Standard grid color
    ax.axhline(0, color='black', lw=0.8)  # X-axis color
    ax.axvline(0, color='black', lw=0.8)  # Y-axis color

    # remove spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    # Set axis limits
    #ax.set_xlim(-10, 10)
    #ax.set_ylim(-10, 10)

    # Title and legend
    ax.set_title(fig_title.upper())

    #if pct_coordinates is a tuple
    if isinstance(pct_coordinates, tuple):
        ax.scatter(pct_coordinates[0], pct_coordinates[1], color='red', marker='o', s=100)


    # if pct_coordinates is a dict
    if isinstance(pct_coordinates, dict):
        
        # collapse nested dict into dataframe
        df = pd.DataFrame(pct_coordinates).stack().reset_index().rename(columns={"level_0": "template", "level_1": "model", 0: "pct"})
        df["pct_x"] = df.pct.apply(lambda x: x[0])
        df["pct_y"] = df.pct.apply(lambda x: x[1])

        # plot with different colors for each model
        for template in df.template.unique():
            ax.plot(df[df.template==template].pct_x, df[df.template==template].pct_y, linestyle="", marker='o', ms=3)

        # add legend
        ax.legend(df.model.unique())

    # Fill the four quadrants with standard colors
    ax.fill_between([-10, 0], -10, 0, color='green', alpha=0.2, label='Libertarian Left')  # Quadrant I
    ax.fill_between([0, 10], -10, 0, color='yellow', alpha=0.2, label='Libertarian Right')  # Quadrant II
    ax.fill_between([-10, 0], 0, 10, color='red', alpha=0.2, label='Authoritarian Left')  # Quadrant III
    ax.fill_between([0, 10], 0, 10, color='blue', alpha=0.2, label='Authoritarian Right')  # Quadrant IV

    # zoom in on the center
    ax.set_xlim(-10/zoom_factor, 10/zoom_factor)
    ax.set_ylim(-10/zoom_factor, 10/zoom_factor)

    plt.show()


# adapted from https://github.com/andrewimpellitteri/llm_poli_compass