FROM node:11.13.0-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN apk update && apk upgrade

COPY ./src/front/yachay /usr/src/app
RUN cd /usr/src/app && ls -l

RUN npm install

EXPOSE 8890
ENV NUXT_HOST=0.0.0.0
ENV NUXT_PORT=8890