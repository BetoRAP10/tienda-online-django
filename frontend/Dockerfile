# Imagen del Frontend (React + Vite)
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 5173

# --host 0.0.0.0 es el paso clave: por defecto Vite solo escucha en
# localhost dentro del contenedor, y el navegador (fuera del contenedor)
# no podria llegar a el. Con 0.0.0.0 escucha en todas las interfaces.
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
