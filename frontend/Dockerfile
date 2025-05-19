FROM node:18

WORKDIR /app

COPY package.json ./
COPY vite.config.js ./
RUN npm install react react-dom vite @vitejs/plugin-react --legacy-peer-deps

COPY . .

EXPOSE 5173
CMD ["npm", "run", "dev"]
