# ─────────────────────────────────────────────
# Stage 1: Builder — Seed the knowledge base
# ─────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY knowledge_source/ /knowledge_source/
COPY seed_knowledge_base.py .

# Run seeding at build time → produces /chroma_data
RUN python seed_knowledge_base.py

# ─────────────────────────────────────────────
# Stage 2: Runtime — Serve the pre-built index
# ─────────────────────────────────────────────
FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir chromadb==1.5.5

# Copy the pre-built vector index from the builder stage
COPY --from=builder /chroma_data /chroma_data

EXPOSE 8000

CMD ["chroma", "run", "--host", "0.0.0.0", "--port", "8000", "--path", "/chroma_data"]
