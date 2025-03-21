# Use a lightweight Python base image
FROM python:3.12.9-slim

# Create a non-root user
RUN useradd -m appuser

# Set the working directory inside the container
WORKDIR /app

# Update package lists
RUN apt-get update -y

RUN apt-get install -y gnupg software-properties-common wget

# Define Terraform version
ENV TERRAFORM_VERSION=v1.10.1

# Add HashiCorp GPG key and repository
RUN apt-get update -y && \ 
    apt-get install -y --no-install-recommends gnupg wget 
RUN wget -O - https://apt.releases.hashicorp.com/gpg | gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg 
RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" > /etc/apt/sources.list.d/hashicorp.list

# Update package lists and install Terraform
RUN  apt-get update && \
    apt-get install -y --no-install-recommends terraform && \
    apt-get clean && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Change ownership of the application directory to the non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

CMD ["python", "run.py"]