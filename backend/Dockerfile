# Use an official Python runtime as a parent image
FROM python:3.11

ARG environment
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV environment ${environment}


# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt

COPY entrypoint.sh ./

RUN apt-get update \
    && apt-get install -y --no-install-recommends dialog \
    && apt-get install -y --no-install-recommends openssh-server \
    && echo "root:Docker!" | chpasswd \
    && chmod u+x ./entrypoint.sh
COPY sshd_config /etc/ssh/


# Expose the port Django runs on
EXPOSE 80 2222
ENTRYPOINT [ "./entrypoint.sh" ] 
