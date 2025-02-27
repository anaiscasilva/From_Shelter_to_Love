# ----------------------------------
#          INSTALL & TEST
# ----------------------------------
install_requirements:
	@pip install -r requirements.txt

check_code:
	@flake8 scripts/* From_Shelter_to_Love/*.py

black:
	@black scripts/* From_Shelter_to_Love/*.py

test:
	@coverage run -m pytest tests/*.py
	@coverage report -m --omit="${VIRTUAL_ENV}/lib/python*"

ftest:
	@Write me

clean:
	@rm -f */version.txt
	@rm -f .coverage
	@rm -fr */__pycache__ */*.pyc __pycache__
	@rm -fr build dist
	@rm -fr From_Shelter_to_Love-*.dist-info
	@rm -fr From_Shelter_to_Love.egg-info

install:
	@pip install . -U

all: clean install test black check_code

count_lines:
	@find ./ -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./scripts -name '*-*' -exec  wc -l {} \; | sort -n| awk \
		        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./tests -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''

# ----------------------------------
#      UPLOAD PACKAGE TO PYPI
# ----------------------------------
PYPI_USERNAME=<AUTHOR>
build:
	@python setup.py sdist bdist_wheel

pypi_test:
	@twine upload -r testpypi dist/* -u $(PYPI_USERNAME)

pypi:
	@twine upload dist/* -u $(PYPI_USERNAME)


# ----------------------------------
#         HEROKU COMMANDS
# ----------------------------------

streamlit:
	-@streamlit run app.py

heroku_login:
	-@heroku login

APP_NAME = from-shelter-to-love

heroku_create_app:
	-@heroku create ${APP_NAME}

deploy_heroku:
	-@git push heroku master
	-@heroku ps:scale web=1

# ----------------------------------
#         API COMMANDS
# ----------------------------------

run_api:
	uvicorn api.fast:app --reload  # load web server with code autoreload

# ----------------------------------
#         Bucket in GCP
# ----------------------------------

# project id - replace with your GCP project id
PROJECT_ID=from-shelter-to-love-682

# bucket name - replace with your GCP bucket name
BUCKET_NAME=from-shelter-to-love-682-silva-roth-matos 

# choose your region from https://cloud.google.com/storage/docs/locations#available_locations
REGION=europe-west1

set_project:
	@gcloud config set project ${PROJECT_ID}

create_bucket:
	@gsutil mb -l ${REGION} -p ${PROJECT_ID} gs://${BUCKET_NAME}


##### Package params  - - - - - - - - - - - - - - - - - - -

PACKAGE_NAME=From_Shelter_to_Love
FILENAME=trainer

run_locally:
	@python -m ${PACKAGE_NAME}.${FILENAME}