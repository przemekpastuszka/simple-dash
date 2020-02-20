# Simple Plotly Dash [![Build Status](https://travis-ci.com/rtshadow/Simple-Plotly-Dash.svg?branch=master)](https://travis-ci.com/rtshadow/Simple-Plotly-Dash)

Simple Plotly Dash is a library that simplifies building applications with [Plotly Dash](https://github.com/plotly/dash) by allowing you to attach data directly to the layout and creating all the necessary callback functions under the hood.

## Simplest example - using Input object in the layout
Let's create an app with single `Input` component, that renders back whatever the user has typed in.

```python
from simpledash.callbacks import setup_callbacks

app.layout = html.Div([
    dash_core_components.Input(id='data-input', className='row'),
    
    # with Simple Plotly Dash you can use a dash dependency object directly in the layout
    # it will be replaced by actual `input_box.value` and updated every time it changes
    html.Div(dash.dependencies.Input('data-input', 'value'), className='row', id='output-div')
])

setup_callbacks(app)  # this will scan the layout and create all necessary callback functions
```

As you can see, no callbacks were explicitly defined and the code is clean and simple.

What happened? The `setup_callbacks` method has scanned the app's layout, found all occurrences of `dash.dependencies.Input` and created a callback functions for them.

## More complex example - data functions with `data_provider` decorator
We would like to have two Inputs (named A and B) and let user decide which one is going to be used
for rendering the output value. This choice will be done via dropdown.

```python
import dash_core_components as dcc
from dash.dependencies import Input
from simpledash.data.data_providers import data_provider

input_a = dcc.Input(id='data-input-a', value="")
input_b = dcc.Input(id='data-input-b', value="")
input_chooser = dcc.Dropdown(id='input-chooser', options=options_from(['A', 'B']))

# use a `data_provider` annotation to indicate, that the method provides data based on inputs
# inputs used by function are declared as arguments to the decorator
# and are later on passed to the function as arguments
@data_provider(Input('data-input-a', 'value'), Input('data-input-b', 'value'), Input('input-chooser', 'value'))
def output_value(input_a_value, input_b_value, input_chooser_value):
    if input_chooser_value == "A":
        return input_a_value
    if input_chooser_value == "B":
        return input_b_value
    return ""


app.layout = html.Div([
    html.Div(["A: ", input_a], className='row'),
    html.Div(["B: ", input_b], className='row'),
    html.Div(["Which one to show? ", input_chooser], className='row'),
    html.Br(),
        # you simply use `data_provider` instance in the layout (as in previous example)
        html.Div(["Here's the output: ", output_value], className='row', id='output'),
        # but you can also run some simple operations on `data_provider`, like `upper()`
        html.Div(["Also in uppercase!: ", output_value.upper()], className='row', id='output-upper')
])

setup_callbacks(app)
```
This time we have used `data_provider` decorator to declare the function that is able to provide data based on inputs. Note, that this is a plain python function, so you should be able to do any operation on inputs, regardless of the complexity.

Interesting thing we see in the example is `output_value.upper()`. This is just a syntax sugar 
that Simple Plotly Dash gives you - instead of writing another `data_provider` to do the uppercasing, 
we can call the method directly on `output_value` (and this will create new `data_provider` under the hood for you).

Please note that the set of operations you are able to do on `data_provider` instance are limited to:
* accessing the property (`output_value.xyz`)
* accessing the item by index (`output_value['xyz']`)
* calling the method (`output_value.xyz("param")`) 