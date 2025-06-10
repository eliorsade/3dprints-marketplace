# ── frontend/Dockerfile ──

############################
## Stage 1: Build Vue App ##
############################
FROM node:18-alpine AS builder
WORKDIR /usr/src/app

# 1) Copy package.json (and package-lock.json if you have it)
COPY package.json ./
# (if you have a lockfile, uncomment:
# COPY package-lock.json ./ )

RUN npm install

# 2) Copy the entire 'public/' directory (so that index.html + images/ end up at /usr/src/app/public)
COPY public ./public

# 3) Copy all your source code and config files
#    - Vite expects index.html at project root, so we'll move public/index.html up one level in the next step
COPY src ./src
COPY vite.config.js ./
COPY tailwind.config.js ./
COPY postcss.config.js ./

# 4) Move index.html from public/ → project root (where Vite looks for it)
RUN mv public/index.html ./index.html

# Now the directory structure inside the builder is:
# /usr/src/app/
# ├─ index.html
# ├─ package.json
# ├─ vite.config.js
# ├─ tailwind.config.js
# ├─ postcss.config.js
# ├─ public/
# │   └─ images/  ← (Vite will copy this entire folder into dist/)
# └─ src/        ← (all your Vue source files)

# 5) Run the production build
RUN npm run build
# → Vite will read index.html, src/, tailwind.config.js, and copy everything under public/
#    into /usr/src/app/dist/, including public/images/*.jpg

################################
## Stage 2: Serve via Nginx   ##
################################
FROM nginx:stable-alpine

# 6) Copy built files from the previous stage into Nginx’s html folder
COPY --from=builder /usr/src/app/dist /usr/share/nginx/html

# 7) Copy your Nginx config that proxies /api → backend:5000
COPY default.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

# (Nginx’s default CMD is fine; no need to override)

