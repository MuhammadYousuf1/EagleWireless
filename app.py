from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from data.store import DF
from pages import home
from pages import Fees_Rebates, Accessory_GP

PAGE_LAYOUTS = {
    'spiff': {'label': 'SPIFF', 'layout': home.layout},
    'sales': {'label': 'Fees_Rebates', 'layout': Fees_Rebates.layout},
    'regional': {'label': 'Accessory GP', 'layout': Accessory_GP.layout},
}

# The workbook is immutable for the duration of a run. Build the page layouts
# once so switching tabs does not recreate tables or Plotly figures.
PAGE_CONTENTS = {
    key: page['layout'](DF)
    for key, page in PAGE_LAYOUTS.items()
}

app = Dash(__name__, title='Practice Dashboard', suppress_callback_exceptions=True)
server = app.server
app.layout = html.Div([
    html.H1('EAGLE WIRELESS DASHBOARD', className='app-title'),
    dcc.Tabs(
        id='page-tabs',
        value='spiff',
        children=[
            dcc.Tab(label=page['label'], value=key)
            for key, page in PAGE_LAYOUTS.items()
        ]
    ),
    html.Div(id='page-content', className='page-content-wrapper')
])


@app.callback(Output('page-content', 'children'), Input('page-tabs', 'value'))
def render_tab(tab_value):
    return PAGE_CONTENTS.get(tab_value, PAGE_CONTENTS['spiff'])


if __name__ == '__main__':
    # Disable reloader on Windows to avoid signal.SIGTERM error
    app.run(debug=True, host='127.0.0.1', port=8050, use_reloader=False)
