# 📦 Orders Microservice

## 📝 Overview

TBD

## Technology

- **Python 3.12** - Runtime environment
- **Flask** - Lightweight web framework for building the REST API
- **AWS Elastic Beanstalk** - Cloud deployment platform for hosting the microservice

## Usage

### Requirements

- Python 3.12
- AWS CLI configured with valid credentials
- AWS Elastic Beanstalk CLI (`eb`) installed and configured

### Running locally

1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python application.py
   ```

4. Test the endpoint:

    TBD

### Deployment

Run the deployment script to deploy the microservice to AWS Elastic Beanstalk:

```bash
./deploy.sh
```

The script will automatically:
- Initialize Elastic Beanstalk (if not already initialized)
- Create the environment (if not already created)
- Deploy the application

### Terminating

Run the destroy script to terminate the AWS Elastic Beanstalk environment:

```bash
./destroy.sh
```

## ✍ Author

Dominik Cebula

- https://dominikcebula.com/
- https://blog.dominikcebula.com/
- https://www.udemy.com/user/dominik-cebula/
