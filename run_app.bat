@echo off
REM Mene repoon juureen
cd /d "%~dp0"

REM Päivitä koodi
git pull origin main

REM Varmista riippuvuudet (vain ensimmäisellä kerralla voit kommentoida pois)
pip install -r requirements.txt

REM Käynnistä streamlit
streamlit run app.py

pause

