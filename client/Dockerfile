FROM node:20-alpine as build

WORKDIR /app

COPY package.json /app/package.json

RUN npm install

COPY . /app

EXPOSE 5173

RUN npm run build

FROM nginx:stable-alpine

COPY --from=build /app/dist /usr/share/nginx/html
COPY --from=build /app/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 3000

CMD [ "nginx", "-g", "daemon off;" ]