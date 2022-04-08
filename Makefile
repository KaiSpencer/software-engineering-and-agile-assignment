format:
	djhtml -i ./templates/**/*.html ./templates/*.html && \
	black .

dev:
	python3 app.py

.PHONY: format dev