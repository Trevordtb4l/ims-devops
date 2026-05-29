from locust import HttpUser, task, between

class IMSUser(HttpUser):
    wait_time = between(1, 3)
    token = None

    def on_start(self):
        response = self.client.post("/api/v1/auth/login/", json={
            "username": "trevorandeh@gmail.com",
            "password": "password123"
        })
        if response.status_code == 200:
            self.token = response.json().get("access")

    @task(3)
    def get_logbooks(self):
        if self.token:
            self.client.get("/api/v1/logbooks/", headers={
                "Authorization": f"Bearer {self.token}"
            })

    @task(2)
    def get_internships(self):
        if self.token:
            self.client.get("/api/v1/internships/", headers={
                "Authorization": f"Bearer {self.token}"
            })

    @task(1)
    def get_students(self):
        if self.token:
            self.client.get("/api/v1/students/", headers={
                "Authorization": f"Bearer {self.token}"
            })
