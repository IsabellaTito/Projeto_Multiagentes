.PHONY: app

APP_PATH := src/app.py
STREAMLIT_FLAGS := --server.runOnSave true

init:
	./resources/scripts/init.sh

app:
	PYTHONPATH=./src/ uv run streamlit run $(APP_PATH) $(STREAMLIT_FLAGS)