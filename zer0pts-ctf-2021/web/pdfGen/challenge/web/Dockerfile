FROM node:14
WORKDIR /app

COPY ./ /app
RUN npm install --no-bin-links

EXPOSE 8443
CMD [ "npm", "start" ]

