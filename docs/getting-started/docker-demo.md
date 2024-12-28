# Docker Demo

The easiest way to evaluate Poweradmin without actually connecting to PowerDNS is to use a Docker image.

## Steps to Evaluate Poweradmin Using Docker

1. **Get the Source**
   - Download the release file or use git to clone the repository.

2. **Change to the Directory**
   - Navigate to the directory where the files are located.

3. **Build the Docker Image**
   - Run the following command to build the Docker image:
     ```sh
     docker build --no-cache -t poweradmin .
     ```

4. **Run the Docker Container**
   - Execute the following command to run the Docker container:
     ```sh
     docker run -d --name poweradmin -p 8080:80 poweradmin
     ```

5. **Access Poweradmin**
   - Open your browser and go to [http://localhost:8080](http://localhost:8080).

6. **Login**
   - Use the following credentials to log in:
     - **Username**: admin
     - **Password**: testadmin

> **Note**: This installation uses SQLite to store all the data.