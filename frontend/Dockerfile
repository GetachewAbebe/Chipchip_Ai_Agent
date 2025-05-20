# Stage 1: Build React frontend
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Serve with NGINX
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html

# ✅ Paste the COPY line here only if you have this file
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
