FROM node:20.9.0-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy only package.json and package-lock.json for dependency installation
COPY package.json package-lock.json ./

# Install npm dependencies
RUN npm install

# Copy the rest of the application code to the working directory
COPY . .

# Expose the Vite development server port
EXPOSE 5002

# Start the Vite development server
CMD ["npm", "run", "dev"]
