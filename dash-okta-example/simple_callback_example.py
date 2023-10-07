import argparse

from dash import Dash
from dash import Input
from dash import Output
from dash import dcc
from dash import html

from dash_okta import require_login_for_dash

app = Dash(__name__)

app.layout = html.Div([
    html.H6("Change the value in the text box to see callbacks in action!"),
    html.Div([
        "Input: ",
        dcc.Input(id='my-input', value='initial value', type='text')
    ]),
    html.Br(),
    html.Div(id='my-output'),
])

@app.callback(
    Output(component_id='my-output', component_property='children'),
    Input(component_id='my-input', component_property='value')
)
def update_output_div(input_value):
    # NOTE
    # - this is a modified version of:
    #   https://dash.plotly.com/basic-callbacks#simple-interactive-dash-app
    return html.Div([
        html.Div(f'Output from server: {input_value}'),
    ])

def main(argv=None):
    """
    Start the example app with the development server.
    """
    parser = argparse.ArgumentParser(
        description = main.__doc__,
    )
    parser.add_argument(
        '--login',
        action = 'store_true',
        help = 'Add login redirect.',
    )
    args = parser.parse_args(argv)

    if args.login:
        require_login_for_dash(app, 'SECRET KEY FROM CONFIG!')

    app.run(debug=True)

if __name__ == '__main__':
    main()
