---

### 1. Deploy the app on a traditional VM

To deploy the basic application on a traditional virtual environment I’ve chosen for a containerised approach. Specifically, I’ll be using docker to achieve said deployment. 

Docker is in my eyes the best approach with it being lightweight, easily manageable and extendable. With docker images you can create small deployments which are easily manageable and have a small footprint when it comes to needed resources whilst using and storing them. I’m more familiar with containerised deployments via Docker too, which is why it has my preference.

---

### 2. Look into the application code and make adjustments that you think are necessary

We’re starting off with a basic Flask config that has almost no security implementations what so ever. Since it’s been a while since I’ve read up on the most recent security implementations I’ll use sources like OWASP to create a baseline Flask configuration that is safe with todays standards:

- [**A01:2021-Broken Access Control**](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)
- [**A02:2021-Cryptographic Failures**](https://owasp.org/Top10/A02_2021-Cryptographic_Failures/)
- [**A03:2021-Injection**](https://owasp.org/Top10/A03_2021-Injection/)
- [**A04:2021-Insecure Design**](https://owasp.org/Top10/A04_2021-Insecure_Design/)
- [**A05:2021-Security Misconfiguration**](https://owasp.org/Top10/A05_2021-Security_Misconfiguration/)
- [**A06:2021-Vulnerable and Outdated Components**](https://owasp.org/Top10/A06_2021-Vulnerable_and_Outdated_Components/)
- [**A07:2021-Identification and Authentication Failures**](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/)
- [**A08:2021-Software and Data Integrity Failures**](https://owasp.org/Top10/A08_2021-Software_and_Data_Integrity_Failures/)
- [**A09:2021-Security Logging and Monitoring Failures**](https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/)
- [**A10:2021-Server-Side Request Forgery**](https://owasp.org/Top10/A10_2021-Server-Side_Request_Forgery_%28SSRF%29/)

From top to bottom:

- Added security features such as; CSRF tokens, password encryption
- Added usage of environment variables
- Added user session management, authentication and access control
- Improved database management by implementing SQL-Alchemy
- Added user register functionality

Since this is a small web application with not that many endpoints and functionalities some security implementations were not added. If the project had more resources or endpoints to take care of I would’ve added better structure and readability by refactoring functions into separate files and by using blueprints to load everything from __init__. Things like HTTPS, a Flask Talisman for CSP and HTTPS-only and clickjacking were not added since this project is being served over HTTP.

---

### Deploy the app on a Kubernetes environment

To run the new Flask webserver in a Kubernetes environment, run:

```bash
minikube start
```

Create the resource (pod) by applying the current configuration:

```bash
kubectl apply -f app/srechallenge.yaml 
```

Start a pod that serves the Flask website:

```bash
minikube service flask-service
```
