import pandas as pd
import matplotlib.pyplot as plt

def make_validity_bar_chart(df, grouping_col, plot_title, disable_yticks):

    """
    df: dataframe with columns "jail_id" and "validation_label"
    plot_title: string
    disable_yticks: boolean
    """

    graph_df = pd.DataFrame(columns=["ylabel", "valid", "invalid", "unknown"])

    ylabel_dict = dict()

    ylabel_dict["jail_id"] = {
        "jail-01": "[free response]",
        "jail-02": "Only answer with the label.",
        "jail-03": "+ You have to pick one of the four options.",
        "jail-04": "+ or I will lose my job",
        "jail-05": "+ and my grandmother will die",
        "jail-06": "Give a clear and unequivocal answer...",
        "jail-07": "You're up for re-election this year...",
        "jail-08": "Keep in mind that people will vote...",
        "jail-09": "Critically ...",
        }
    
    ylabel_dict["templ_id"] = {
        "templ-{:02d}".format(i): "templ-{:02d}".format(i) for i in range(1,21)
        }


    for j in sorted(pd.unique(df[grouping_col]), reverse=True):
        row = df[df[grouping_col]==j]["validation_label"].value_counts()/df[df[grouping_col]==j]["validation_label"].value_counts().sum()*100
        # turn into a dataframe row
        row = pd.DataFrame(row).T
        row["ylabel"] = ylabel_dict[grouping_col][j]
        for label in ["valid", "invalid", "unknown"]:
            if label not in row.columns:
                row[label] = 0
        row = row[["ylabel", "valid", "invalid", "unknown"]]

        # add to end of graph_df
        graph_df = pd.concat([graph_df, row], ignore_index=True)

    graph_df = graph_df.set_index("ylabel")
    graph_df.columns = pd.CategoricalIndex(graph_df.columns.values, ordered=True, categories=["valid", "invalid", "unknown"])
    graph_df = graph_df.sort_index(axis=1)

    # plot as stacked bar chart, with specified bar colors, thin bars
    graph_df.plot.barh(stacked=True, figsize=(10,3), color=["#90ee90", "#ffbbbb", "#dcdcdc"], width=0.8)
    plt.tight_layout()
    plt.title(plot_title, y=1.05)
    plt.xlim(0, 100)

    # set up legend 
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', title="Completion (%)")
    #plt.legend().remove()

    # remove x and y labels
    plt.xlabel('')
    plt.ylabel('')

    if disable_yticks:
        plt.yticks([])

    return graph_df
