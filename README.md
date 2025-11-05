# 🧙 Wizard School Enrollment - Saga Pattern Simulation

This project simulates the **Saga Pattern** for a wizard school enrollment process using four microservices. The architecture follows a centralized **orchestrator** model to coordinate the distributed transaction.

When a student enrolls, the orchestrator coordinates three steps:
1.  **Validate Wand**: Confirms the student has a valid wand.
2.  **Assign House**: Assigns the student to a school house (this step can fail randomly).
3.  **Deliver Owl**: Sends a welcome owl with the admission letter.

If any step fails, the orchestrator triggers compensating transactions to undo the previous steps.

---

## 🚀 Microservices Overview

| Service         | Language | Port | Description                                      |
|-----------------|----------|------|--------------------------------------------------|
| `orchestrator`  | Python   | 5000 | Coordinates the enrollment flow (Saga logic).    |
| `wand-service`  | Python   | 5001 | Validates and revokes a student's wand.          |
| `house-service` | Node.js  | 5002 | Assigns a house (with random failure simulation).|
| `owl-service`   | Python   | 5003 | Delivers and revokes the welcome owl.            |

---

## 🧱 Technologies Used

- Python + Flask
- Node.js + Express
- Docker
- **Kubernetes**

---

## ⚙️ Running with Kubernetes (Minikube)

These instructions assume you have `docker` and `minikube` installed.

### 1. Start Minikube

```bash
minikube start
```

### 2. Build Docker Images

In the project's root directory, build the image for each service:

```bash
docker build -t wand-service:latest ./wand-service
docker build -t house-service:latest ./house-service
docker build -t owl-service:latest ./owl-service
docker build -t orchestrator:latest ./orchestrator
```

### 3. Load Images into Minikube

Make the local images available to the Minikube cluster:

```bash
minikube image load wand-service:latest
minikube image load house-service:latest
minikube image load owl-service:latest
minikube image load orchestrator:latest
```

### 4. Deploy to Kubernetes

Apply all the Kubernetes manifests from the `k8s` directory:

```bash
kubectl apply -f k8s/
```

Check that all pods are running:

```bash
kubectl get pods
# NAME                                       READY   STATUS    RESTARTS   AGE
# house-deployment-xxxxxxxxxx-xxxxx        1/1     Running   0          15s
# orchestrator-deployment-xxxxxxxxxx-xxxxx   1/1     Running   0          15s
# owl-deployment-xxxxxxxxxx-xxxxx          1/1     Running   0          15s
# wand-deployment-xxxxxxxxxx-xxxxx         1/1     Running   0          15s
```

### 5. Test the Enrollment Saga

First, get the URL for the orchestrator service:

```bash
minikube service orchestrator-service
```

This command will print the URL (e.g., `http://127.0.0.1:54321`) and may open it in your browser. Use this URL to send a `POST` request.

**Example with `curl`:**

```bash
# Replace <URL> with the one from the previous command
curl -X POST <URL>/enroll -H "Content-Type: application/json" -d '{"student": "harry_potter"}'
```

- **On success**, you'll get a `200 OK` with `{"status":"success", ...}`.
- **On failure** (the house assignment fails randomly), you'll get a `500 Internal Server Error` with `{"status":"failed", ...}`. Check the orchestrator's logs (`kubectl logs deploy/orchestrator-deployment`) to see the compensation logic in action.

### 6. Cleanup

To delete all the created resources:

```bash
kubectl delete -f k8s/
```
