# Contributing
To contribute, feel free to fork the project, make changes and create a Pull Request into the master branch of
this repository.

To get the dependencies for developing chord-extractor simply run
```commandline
pip install -r requirements.txt
```
bearing in mind as well the prerequisite tasks listed in the Install section of README.md.

In order to have a successful PR, the Github Actions build and tests need to pass. There are a couple of integration
tests at the moment which also measure performance of running extraction on a batch of files
with vs without multiprocessing. To run the test, and to see the outputs from any 3rd party processes run:

```commandline
python -m pytest --capture=no --log-cli-level=INFO
```