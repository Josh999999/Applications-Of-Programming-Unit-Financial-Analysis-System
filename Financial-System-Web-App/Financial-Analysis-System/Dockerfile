# Step 1: Use an official Node image to build the application
FROM node:18 AS build-stage

# Step 2: Set working directory
WORKDIR /app

# Step 3: Copy package.json and package-lock.json
COPY package*.json ./

# Step 4: Install dependencies
RUN npm install

# Step 5: Copy the rest of the application files
COPY . .

# Step 6: Build the production-ready app
RUN npm run build

# Step 7: Use an Nginx image to serve the built app
FROM nginx:alpine AS production-stage

# Step 8: Copy the build files from the build-stage to Nginx's public folder
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Step 9: Expose port 80 to access the app
EXPOSE 80

# Step 10: Start the Nginx server
CMD ["nginx", "-g", "daemon off;"]