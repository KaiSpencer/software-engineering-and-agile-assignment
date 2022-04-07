format:
	djhtml -i ./incident_management/templates/**/*.html ./incident_management/templates/*.html

dev:
	python3 incident_management/app.py

.PHONY: format dev