# Streamlit on Heroku

This project is intended to help you tie together some important concepts and
technologies from the 12-day course, including Git, Streamlit, JSON, Pandas,
Requests, Heroku, and Bokeh for visualization.

The repository contains a basic template for a Streamlit configuration that will
work on Heroku.

A [finished example](https://streamlit-12day-example.herokuapp.com/) that demonstrates some basic functionality.

## Step 1: Setup and deploy
- Git clone the existing template repository.
- `Procfile`, `requirements.txt`, and `setup.py` contain some default settings. If you want, you can change the email address in `setup.py` to your own, but it won't affect anything in the app.

- Create Heroku application with `heroku create <app_name>` or leave blank to
  auto-generate a name.

- Deploy to Heroku: `git push heroku master`
- You should be able to see your site at `https://<app_name>.herokuapp.com`
- A useful reference is the Heroku [quickstart guide](https://devcenter.heroku.com/articles/getting-started-with-python-o).

## Step 2: Get data from API and put it in pandas
- Use the `requests` library to grab some data from a public API. This will
  often be in JSON format, in which case `simplejson` will be useful.
- Build in some interactivity by having the user submit a form which determines which data is requested.
- Create a `pandas` dataframe with the data.

## Step 3: Plot pandas data
- Create an interactive plot from the dataframe. Some recommended libraries: Altair, Bokeh, and Plotly.
- Altair provides a simple interface for creating linked and layered plots. They can even be exported and embedded in static HTML (and remain fully interactive!) See the [documentation](https://altair-viz.github.io/)
  and be sure to check out the example gallery.
- Bokeh can be used in a wide range of applications, from simple charts to extensive dashboards with sophisticated backends. It's the most fully-featured library of these three, but you won't be using it for anything complicated in the Milestone Project. Here you can find the Bokeh [documentation](http://bokeh.pydata.org/en/latest/docs/user_guide/embed.html)
  and some [examples](https://github.com/bokeh/bokeh/tree/master/examples/embed).
- Plotly provides a range of APIs in their library. Plotly express, for instance, can be used to create commonly used plots. The Graph Objects API affords more customization, but is more complicated to use. Here is the [documentation](https://plotly.com/python/plotly-express/#gallery) for Plotly Express.
