## Requirements

Before running the project, make sure you have the following installed:

- Python 3.10.2 (or compatible version)

To use the voice recognition functionality, you'll need the Vosk model version 0.22. Download the appropriate model from [Vosk models page](https://alphacephei.com/vosk/models) and place it in the `models/` directory.

### Python Libraries

You can install the required Python libraries by running the following in your venv (virtual environment) create one if you havent yet:

```bash
pip install -r requirements.txt

.\venv\Scripts\activate
//open a seperate terminal for each
rasa run
rasa run actions
py main.py

then press voice activation, make sure the mic works
and then you can use any of the commands listed in domain as intents
```
