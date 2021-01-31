# Create a sankey using ploty
# Inputs are a df, a list of columns to use from that df, and optionally a col to take values from. Otherwise defaults to count

@TODO: Look at ability to amend/tailor colour

import plotly.graph_objects as go
import numpy as np
import pandas as pd

def cols_to_source_target(cols):
    sources = cols[:-1]
    targets = cols[1:]
    return sources, targets

def create_sankey_indices(df, sources, targets):
    """
    Create labels and dict to map needed to build sankey from inputs
    Must be given as a list of df cols
    """
    sankey_labs = []
    all = list(set(sources + targets))
    for col in all:
        col_uniques = list(df[col].unique())
        sankey_labs += col_uniques
    labels_dict = {}
    count = 0
    for lab in sankey_labs:
        labels_dict[lab] = count
        count += 1
    return sankey_labs, labels_dict


def make_lists(df, sources, targets, labels_dict, values='count'):
    """Create list of indices used to plot sankey.
    takes a basic count / frequency as default.
    Specify values to use as values otherwise e.g. costs/transactions
    """

    all_len = len(sources)

    out_sources = []
    for source in sources:
        source = df[source].tolist()
        out_sources += source

    out_targets = []
    for target in targets:
        target = df[target].tolist()
        out_targets += target

    source_indices = []
    target_indices = []
    for i, j in zip(out_sources, out_targets):
        ind = labels_dict[i]
        source_indices.append(ind)
        ind = labels_dict[j]
        target_indices.append(ind)
    if values == 'count':
        value = len(source_indices) * [all_len]
    else:
        value = df[values].tolist()
        value *= all_len
    return source_indices, target_indices, value


def plot_sankey(sankey_labels, source_ind, target_ind, value, title):
    """Plot sankey with valid inputs"""
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="grey", width=0.5),
            label=sankey_labels,
            color="blue",
        ),
        link=dict(
            source=source_ind,  # indices correspond to labels, eg A1, A2, A1, B1, ...
            target=target_ind,
            value=value,
            color="green"
        ))
    ])

    fig.update_layout(title_text=title, font_size=25)
    fig.show()


def generate_sankey(df, cols, values='count', title='Sankey Plot'):
    """end-to-end sankey creation"""
    sources, targets = cols_to_source_target(cols)
    sankey_labs, labels_dict = create_sankey_indices(df, sources, targets)
    source_indices, target_indices, value = make_lists(df, sources, targets, labels_dict, values)
    plot_sankey(sankey_labs, source_indices, target_indices, value, title=title)
    
    
    
# Example usage:

source_data = r'filename.csv'
df = pd.read_csv(source_data)
df.date = pd.to_datetime(df.date)
df_ind = df.index

columns = ['sender_country', 'sender_currency', 'recipient_network']
generate_sankey(df, columns, values='sender_amt', title='Sankey Plot')
