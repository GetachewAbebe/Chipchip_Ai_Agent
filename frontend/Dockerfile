FROM node:18

WORKDIR /app
COPY package.json ./
COPY vite.config.js ./
RUN npm install react react-dom vite @vitejs/plugin-react react-chartjs-2 chart.js --legacy-peer-deps
COPY . .
CMD ["npm", "run", "dev"]