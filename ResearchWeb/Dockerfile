# Node image
FROM node:14

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Build app
RUN npm run build

# Install serve
RUN npm install -g serve

# Start server
CMD [ "serve", "-s", "dist" ]
