# VaultFlow 🚀

An end-to-end data engineering project simulating a real-world retail pipeline.

---
<img width="1920" height="1080" alt="1776342899592966893" src="https://github.com/user-attachments/assets/29b19486-e7e0-4eba-bf55-5a93866af85f" />

## 🏗️ Architecture

```bash
Raw Data → PostgreSQL → dbt → Airflow → AWS S3 → Analytics
```

---

## 🛠️ Tech Stack

| Layer            | Tool            | Status |
| ---------------- | --------------- | ------ |
| Database         | PostgreSQL 15   | ✅     |
| Containerization | Docker          | ✅     |
| Data Generation  | Python + Faker  | ✅     |
| Transformation   | dbt             | ✅     |
| Orchestration    | Airflow         | ✅     |
| Cloud            | AWS S3 + Athena | 🔄     |
| Streaming        | Kafka           | 🔄     |

---

## 🚀 Quick Start

### 1. Clone & setup

```bash
git clone https://github.com/Ajay1812/VaultFlow.git
cd VaultFlow
cp .env.example .env          # fill in credentials
cp docker/servers.json.example docker/servers.json
```

### 2. Start containers

```bash
# Always run from project root!
# docker-compose -f docker/docker-compose.yml --env-file .env down
# docker-compose -f docker/docker-compose.yml build --no-cache
docker-compose -f docker/docker-compose.yml --env-file .env up -d
```

### 3. Python environment

```bash
uv venv && source .venv/bin/activate
uv sync
```

### 4. Load data

```bash
python scripts/load_data.py
```

### 5. Run dbt

```bash
uv run dbt run       # build models
uv run dbt test      # run 14 data quality tests
```

### 6. View docs & lineage

```bash
uv run dbt docs generate
uv run dbt docs serve --port 9000
# open http://localhost:9000
```

### 7. pgAdmin UI

```bash
http://localhost:8080
```

### 7. Airflow UI

```bash
http://localhost:8081
```

---

## 📊 Data Model

**Fact Table:** `fact_orders`

**Dimensions:** `dim_customers` | `dim_products` | `dim_dates` | `dim_locations`

---

## 📁 Project Structure

| Folder            | Purpose                      |
| ----------------- | ---------------------------- |
| `docker/`         | Docker + pgAdmin config      |
| `models/staging/` | Bronze layer — raw views     |
| `models/marts/`   | Gold layer — business tables |
| `scripts/`        | OOPs data pipeline           |
| `sql/`            | Schema + queries             |
| `tests/`          | Custom dbt tests             |
| `dags/`           | Airflow DAGs (coming)        |

---

## 🗺️ Roadmap

- [x] Star schema design
- [x] OOPs data pipeline + logging
- [x] Docker setup
- [x] dbt models + tests + lineage
- [x] Airflow orchestration
- [ ] AWS S3 + Athena
- [ ] Kafka streaming
- [ ] Terraform IaC

---

## 👨‍💻 Author

**Ajay** — Data Engineering
