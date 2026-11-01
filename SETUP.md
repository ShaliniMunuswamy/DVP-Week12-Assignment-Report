# Setup Guide (Jenkins + SonarQube + Docker)

## 1. Infrastructure (one Ubuntu VM / EC2, t3.medium+, open ports 8080, 9000, 5000)
```bash
sudo apt update && sudo apt install -y docker.io openjdk-17-jdk python3-venv curl git
sudo systemctl enable --now docker

# SonarQube
docker run -d --name sonarqube -p 9000:9000 sonarqube:lts-community

# Jenkins (install per jenkins.io docs), then:
sudo usermod -aG docker jenkins && sudo systemctl restart jenkins
```
SonarQube: http://<host>:9000 (admin/admin, change password).

## 2. SonarQube
1. My Account > Security > Generate token (type: User/Global). Copy it.
2. Administration > Configuration > Webhooks > Create:
   URL `http://<jenkins-host>:8080/sonarqube-webhook/` (needed for the quality gate).
3. Quality Gates: use "Sonar way" (or create a stricter one) and set as default.

## 3. Jenkins plugins
GitHub, Pipeline, SonarQube Scanner, Docker Pipeline, Credentials Binding,
Role-based Authorization Strategy.

## 4. Jenkins configuration
- Credentials > Global:
  - `dockerhub-creds` (Username with password: DockerHub user + access token)
  - `sonar-token` (Secret text: SonarQube token)
- Manage Jenkins > System > SonarQube servers: Name `SonarQube`,
  URL `http://<host>:9000`, token credential `sonar-token`.
- Manage Jenkins > Tools > SonarQube Scanner: Name `SonarScanner`, install automatically.
- New Item > Pipeline > "Pipeline script from SCM" > Git repo URL, branch `main`.
  Tick "GitHub hook trigger for GITScm polling".

## 5. GitHub webhook
Repo > Settings > Webhooks > Add: `http://<jenkins-host>:8080/github-webhook/`,
content type `application/json`, event "Just the push event".

## 6. Role-based security
1. Manage Jenkins > Security > Authorization: "Role-Based Strategy".
2. Manage Jenkins > Users > Create user `devuser`.
3. Manage Jenkins > Manage and Assign Roles > Manage Roles:
   - Global role `developer`: Overall/Read, Job/Read, Job/Build, Job/Workspace
   - Global role `admin`: all permissions
4. Assign Roles: `devuser` -> developer, your admin user -> admin.
5. Log in as `devuser` to verify (no Manage Jenkins option).

## 7. Screenshots to capture
1. SonarQube project dashboard showing "Passed" quality gate.
2. DockerHub repository > Tags showing the pushed image.
3. Jenkins "Manage and Assign Roles" page showing the user and role assignment
   (also helpful: Manage Users list).
