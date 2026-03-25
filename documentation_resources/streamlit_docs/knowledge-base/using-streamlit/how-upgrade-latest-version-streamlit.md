<!-- Source: https://docs.streamlit.io/knowledge-base/using-streamlit/how-upgrade-latest-version-streamlit -->

We recommend upgrading to the latest official release of Streamlit so you have access to the newest, cutting-edge features. If you haven't installed Streamlit yet, please read our [Installation guide](/get-started/installation). It helps you set up your virtual environment and walks you through installing Streamlit on Windows, macOS, and Linux. Regardless of which package management tool and OS you're using, we recommend running the commands on this page in a virtual environment.

If you've previously installed Streamlit and want to upgrade to the latest version, here's how to do it based on your dependency manager.

Streamlit's officially-supported environment manager for macOS and Linux is [Pipenv](https://pypi.org/project/pipenv/).

1. Navigate to the project folder containing your Pipenv environment:

```
cd myproject
```

2. Activate that environment, upgrade Streamlit, and verify you have the latest version:

```
pipenv shell
pip install --upgrade streamlit
streamlit version
```

Or if you want to use an easily-reproducible environment, replace `pip` with `pipenv`every time you install or update a package:

```
pipenv update streamlit
pipenv run streamlit version
```

1. Activate the conda environment where Streamlit is installed:

```
conda activate $ENVIRONMENT_NAME
```

Be sure to replace`$ENVIRONMENT_NAME` ☝️ with the name your conda environment!

2. Update Streamlit within the active conda environment and verify you have the latest version:

```
conda update -c conda-forge streamlit -y
streamlit version
```

In order to get the latest version of Streamlit with [Poetry](https://python-poetry.org/) and verify you have the latest version, run:

```
poetry update streamlit
streamlit version
```

[*arrow\_back*Previous: How to download a Pandas DataFrame as a CSV?](/knowledge-base/using-streamlit/how-download-pandas-dataframe-csv)[*arrow\_forward*Next: How to insert elements out of order?](/knowledge-base/using-streamlit/insert-elements-out-of-order)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI