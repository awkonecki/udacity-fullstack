FROM node:12-alpine
RUN apk add --no-cache build-base g++ postgresql make python3-dev py3-pip && ln -sf python3 /usr/bin/python
RUN python3 -m pip install --upgrade pip setuptools wheel
RUN pip3 install SQLAlchemy
RUN pip3 install Flask 
RUN pip3 install Flask-SQLAlchemy
# WORKDIR /app
# COPY . .
# RUN yarn install --production
# CMD ["node", "src/index.js"]