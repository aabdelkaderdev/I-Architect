<!-- Source: https://docs.streamlit.io/knowledge-base/dependencies/install-package-not-pypi-conda-available-github -->

Are you trying to deploy your app to [Streamlit Community Cloud](/deploy/streamlit-community-cloud), but don't know how to specify a [Python dependency](/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies#add-python-dependencies) in your requirements file that is available on a public GitHub repo but not any package index like PyPI or Conda? If so, continue reading to find out how!

Let's suppose you want to install `SomePackage` and its Python dependencies from GitHub, a hosting service for the popular version control system (VCS) Git. And suppose `SomePackage` is found at the the following URL: `https://github.com/SomePackage.git`.

pip (via `requirements.txt`) [supports](https://pip.pypa.io/en/stable/topics/vcs-support/) installing from GitHub. This support requires a working executable to be available (for Git). It is used through a URL prefix: `git+`.

To install `SomePackage`, innclude the following in your `requirements.txt` file:

```
git+https://github.com/SomePackage#egg=SomePackage
```

You can even specify a "git ref" such as branch name, a commit hash or a tag name, as shown in the examples below.

Install `SomePackage` by specifying a branch name such as `main`, `master`, `develop`, etc, in `requirements.txt`:

```
git+https://github.com/SomePackage.git@main#egg=SomePackage
```

Install `SomePackage` by specifying a commit hash in `requirements.txt`:

```
git+https://github.com/SomePackage.git@eb40b4ff6f7c5c1e4366cgfg0671291bge918#egg=SomePackage
```

Install `SomePackage` by specifying a tag in `requirements.txt`:

```
git+https://github.com/SomePackage.git@v1.1.0#egg=SomePackage
```

It is currently **not possible** to install private packages from private GitHub repos using the URI form:

```
git+https://{token}@github.com/user/project.git@{version}
```

where `version` is a tag, a branch, or a commit. And `token` is a personal access token with read only permissions. Streamlit Community Cloud only supports installing public packages from public GitHub repos.

[*arrow\_back*Previous: Installing dependencies](/knowledge-base/dependencies)[*arrow\_forward*Next: ImportError libGL.so.1 cannot open shared object file No such file or directory](/knowledge-base/dependencies/libgl)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI