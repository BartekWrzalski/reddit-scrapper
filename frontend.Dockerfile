FROM node:20 as build

WORKDIR /app

COPY /frontend .

RUN npm install
RUN npm run build

FROM nginx:alpine

COPY --from=build /app/build /usr/share/nginx/html
COPY --from=build /app/src /usr/share/nginx/html
