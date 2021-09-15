
# write some code to build your image

FROM python:3.8.6-buster

COPY api /api
COPY From_Shelter_to_Love /From_Shelter_to_Love
#COPY catsmodelcats.joblib /catsmodel.joblib
#COPY dogsmodeldogs.joblib /dogsmodel.joblib
COPY requirements.txt /requirements.txt
#COPY /home/isa/code/anaiscasilva/gcp/from-shelter-to-love-682.json /credentials.json
#COPY from-shelter-to-love-682.json /credentials.json

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD uvicorn api.fast:app --host 0.0.0.0 --port $PORT