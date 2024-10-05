# In-Town App
A convenient way to notify family and friends that you are around.

## Architecture
The app uses streamlit for the presentation layer (UI). This is due two 3 main reasons:
1. contains all relevant elements and provides slick look out of the box
2. allows to focus on the logic rather than styling issues
3. I'm not a FE wizard

## Local setup
Set up virtual environments with dependencies:
```bash
python -m venv .venv
pip install --upgrade pip
pip install -r requirements.txt
```

To run the app, enter the following into your terminal:
```bash
streamlit run main.py
```