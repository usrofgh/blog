<p align="center">
  <img src="https://i.ibb.co/GWNQnFB/DALL-E-2024-10-26-18-31-50-A-minimalist-logo-for-an-internet-blog-project-with-the-text-Blog-in-a-mo.webp?raw=true" width="400" alt="logo"/>
</p>

---

![](https://img.shields.io/badge/fastapi-109989?style=for-the-badge&logo=FASTAPI&logoColor=white)
![](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=JSON%20web%20tokens&logoColor=white)
![](https://img.shields.io/badge/Pydantic-e92063?style=for-the-badge&logo=Pydantic)
![](https://img.shields.io/badge/sqladmin-12311a?style=for-the-badge&logo=sqladmin)

![](https://img.shields.io/badge/SQLAlchemy-798577?style=for-the-badge&logo=sqlalchemy)
![](https://img.shields.io/badge/alembic-ffffff?style=for-the-badge&logo=alembic)
![](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![](https://img.shields.io/badge/pytest-f7f7f7?style=for-the-badge&logo=pytest)
![](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)

![](https://img.shields.io/badge/ChatGPT-74aa9c?style=for-the-badge&logo=openai&logoColor=white)
![](https://img.shields.io/badge/Sentry-black?style=for-the-badge&logo=Sentry&logoColor=#362D59)
![](https://img.shields.io/badge/poetry-0088dd?style=for-the-badge&logo=poetry)
![](https://img.shields.io/badge/Arq%20(instead%20of%20celery)%20-49781a?style=for-the-badge&logo=arq)

---



[![⚙️ CI process](https://github.com/usrofgh/blog/actions/workflows/cicd.yml/badge.svg)](https://github.com/usrofgh/blog/actions/workflows/cicd.yml)
[![GitHub release](https://img.shields.io/github/release/usrofgh/blog.svg)](https://GitHub.com/usrofgh/blog/releases/)
![](https://img.shields.io/badge/Test%20counts-32-fefjl?logo=pytest)
 
## 📋 Table of Contents

1. 🐳 [Docker](#docker)
2. 💯 [Tests](#tests)



# <a name="docker">🐳 Docker</a>
It uses a multi-stage build to optimize the image size

Put .env to root of the project
```bash
git clone https://github.com/usrofgh/blog
cd blog
docker compose up
```


## Swagger docs http://127.0.0.1:8081/v1/docs

![Scenarios](https://i.ibb.co/wJ6LdLc/Untitled.png)

## CRM http://127.0.0.1:8081/admin

![Scenarios](https://i.ibb.co/QmVmxsY/Untitled.png)


# <a name="tests">💯 Tests</a>
To run the tests, place the .env.test file in the root directory of the project

PSQL creds must be valid and the server must be started (locally or via docker)
Run tests (from root of the project):
```bash
  pytest
```