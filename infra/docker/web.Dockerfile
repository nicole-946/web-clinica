FROM node:20-alpine

WORKDIR /app

COPY apps/web/package.json apps/web/package-lock.json* ./
RUN npm install

COPY apps/web .

ENV NEXT_TELEMETRY_DISABLED=1
EXPOSE 3000

CMD ["npm", "run", "dev"]
