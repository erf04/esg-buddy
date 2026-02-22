FROM node:22-alpine3.22 AS Install

WORKDIR /app

COPY package*.json .

RUN npm i

FROM node:22-alpine3.22 AS Build

WORKDIR /app

COPY --from=Install /app/node_modules ./node_modules
COPY --from=Install /app/package*.json ./
COPY . .
RUN npm run build

FROM nginx:stable-alpine3.23-perl AS Serve

COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf

COPY --from=Build /app/dist /usr/share/nginx/html

