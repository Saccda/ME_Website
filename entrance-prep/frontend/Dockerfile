FROM node:22-alpine AS build
WORKDIR /app
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
ARG API_URL=http://api:8000
ENV API_URL=$API_URL
ENV NEXT_TELEMETRY_DISABLED=1
RUN npm run build
FROM node:22-alpine
WORKDIR /app
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
ENV API_URL=http://api:8000
COPY --from=build --chown=node:node /app ./
USER node
EXPOSE 3000
CMD ["npm", "run", "start"]
