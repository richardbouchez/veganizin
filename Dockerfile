# Build Stage
FROM node:18-alpine AS build

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Production Stage
FROM node:18-alpine

WORKDIR /app
COPY package*.json ./
# Only install production dependencies
RUN npm install --only=production

# Copy built assets from build stage
COPY --from=build /app/dist ./dist
# Copy backend server
COPY server.js .

EXPOSE 8080
ENV PORT=8080

CMD ["node", "server.js"]
