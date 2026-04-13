# VaultFlow 🚀

An end-to-end data engineering project built to simulate
a real-world retail data pipeline from scratch.

## 🏗️ Architecture

Raw Data → PostgreSQL (Star Schema) → dbt (Transforms)
→ Airflow (Orchestration) → Analytics

## 🛠️ Tech Stack

| Layer            | Tool                     |
| ---------------- | ------------------------ |
| Database         | PostgreSQL 15            |
| Containerization | Docker                   |
| Data Generation  | Python + Faker           |
| Transformation   | dbt (coming)             |
| Orchestration    | Airflow (coming)         |
| Cloud            | AWS S3 + Athena (coming) |

## 📊 Data Model

Star schema with 5 tables:

- `fact_orders` — core transactions
- `dim_customers` — customer details
- `dim_products` — product catalog
- `dim_locations` — city/state/region
- `dim_dates` — date dimensions

## 🚀 Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/Ajay1812/VaultFlow.git
cd vaultflow
```

### 2. Start Docker containers

#### ⚠️ Important

Always run docker-compose from project root:

```bash
docker-compose -f docker/docker-compose.yml --env-file .env up -d
```

Running from inside `docker/` folder will cause `.env` not found error.

### 3. Setup Python environment

```bash
uv venv
source .venv/bin/activate
uv sync
```

### 4. Configure environment and pgamdin

```bash
cp .env.example .env
cp docker/servers.json.example docker/servers.json
# Edit servers.json with your container details
```

Edit .env with your DB credentials

### 5. Run the pipeline

```bash
python scripts/load_data.py
```

```bash
# PG Admin UI
http://localhost:8080/browser/
```

## 📁 Project Structure

```
VaultFlow/
├── dags/                    # Airflow DAGs (coming)
├── data/                    # raw data files
├── docker/
│ ├── docker-compose.yml
│ └── servers.json.example
├── models/                  # dbt models (coming)
├── notebooks/               # exploration notebooks
├── scripts/
│ └── load_data.py           # data pipeline
├── sql/
│ ├── schema.sql
│ └── test.sql
├── logs/ # gitignored
├── .env # gitignored
├── .env.example
├── pyproject.toml
└── README.md
```

## 🗺️ Roadmap

- [x] Star schema design
- [x] OOPs data pipeline
- [x] Docker setup
- [ ] dbt transformations
- [ ] Airflow orchestration
- [ ] AWS S3 integration
- [ ] Kafka streaming

## 👨‍💻 Author

Ajay — Data Engineering Journey
