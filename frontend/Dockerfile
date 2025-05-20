# Stage 1: Build React app
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# Stage 2: Serve with nginx
FROM nginx:alpine

# Copy built React files to nginx's web directory
COPY --from=builder /app/dist /usr/share/nginx/html

# Stage 2 – Nginx to serve built files
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
