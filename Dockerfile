# client build
FROM node AS client-build

WORKDIR /client
COPY ./client/package*.json ./
RUN npm install
COPY ./client ./

ENV VITE_API_ENDPOINT=''

RUN npm run build

# server build
FROM python:3.10-buster AS server-build

WORKDIR /usr/share/printestimater
COPY ./server /usr/share/printestimater/

RUN python3 -m pip install --upgrade pip && \
    pip3 install -r requirements.txt

# copy client app files to flask
COPY --from=client-build /client/dist /usr/share/printestimater/src/static

# default sqlite db file
ENV SQLITE_CONNECTIONSTRING='print-estimater.db'
RUN touch ${SQLITE_CONNECTIONSTRING}

EXPOSE 15686
CMD [ "gunicorn", "--bind", "0.0.0.0:15686", "src.application:create_app()"]