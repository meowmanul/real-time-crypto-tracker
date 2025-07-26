FROM node:latest AS build
WORKDIR /app

# Копируем зависимости и ставим их
COPY package*.json ./
RUN npm ci

# Копируем весь код и собираем
COPY . .
RUN npm run build

# 2) Стэ́дия запуска — nginx на отдачу статических файлов
FROM nginx:stable-perl
# Убираем дефолтный конфиг nginx, если нужно
RUN rm /etc/nginx/conf.d/default.conf
# Копируем свой конфиг
COPY nginx.conf /etc/nginx/conf.d
# Копируем готовый билд
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
