# SpringEcomAI — Python LangChain Version

Exact Python equivalent of the Spring Boot SpringEcomAI app.  
Built with **FastAPI + LangChain + ChromaDB + SQLite + OpenAI**.

---

## Project Structure

```
SpringEcomAI-Python/
├── main.py                     ← FastAPI app entry point
├── database.py                 ← SQLAlchemy setup (SQLite)
├── models.py                   ← DB models (Product, Order, OrderItem)
├── schemas.py                  ← Pydantic request/response schemas
├── requirements.txt
├── .env                        ← Your API keys (create from .env.example)
├── config/
│   └── vector_store.py         ← ChromaDB + OpenAI Embeddings setup
├── services/
│   ├── ai_image_service.py     ← DALL-E 3 image generation
│   ├── product_service.py      ← Product CRUD + AI description + Smart Search
│   ├── order_service.py        ← Order placement + vector indexing
│   └── chatbot_service.py      ← RAG chatbot with chat memory
└── routers/
    ├── products.py             ← /api/products endpoints
    ├── orders.py               ← /api/orders endpoints
    └── chatbot.py              ← /api/chat endpoints
```

---

## Spring Boot → Python Mapping

| Spring Boot              | Python Equivalent              |
|--------------------------|-------------------------------|
| `@RestController`        | `APIRouter` (FastAPI)          |
| `@Service`               | Python service module          |
| `JpaRepository`          | SQLAlchemy + SessionLocal      |
| `ChatClient`             | `ChatOpenAI` (LangChain)       |
| `VectorStore (MariaDB)`  | `Chroma` (ChromaDB)            |
| `EmbeddingModel`         | `OpenAIEmbeddings`             |
| `ImageModel (DALL-E 3)`  | `openai.images.generate()`     |
| `MessageWindowChatMemory`| In-memory list (last 20 msgs)  |
| `application.properties` | `.env` file                    |

---

## Setup Steps

### 1. Clone / copy this project

```bash
cd SpringEcomAI-Python
```

### 2. Create virtual environment

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

Or with `uv` (faster):
```bash
uv venv
source .venv/bin/activate   # Mac/Linux
.venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
# or with uv:
uv pip install -r requirements.txt
```

### 4. Create your `.env` file

```bash
cp .env.example .env
```

Open `.env` and add your key:
```
OPENAI_API_KEY=sk-...your-key-here...
```

### 5. Run the server

```bash
uvicorn main:app --reload
```

Server runs at: **http://localhost:8000**  
Swagger docs at: **http://localhost:8000/docs**

---

## API Endpoints

All endpoints match the Spring Boot app exactly.

### Products

| Method | Endpoint                          | Description                  |
|--------|-----------------------------------|------------------------------|
| GET    | `/api/products`                   | Get all products              |
| GET    | `/api/product/{id}`               | Get product by ID             |
| GET    | `/api/product/{id}/image`         | Get product image             |
| POST   | `/api/product`                    | Add product (multipart/form)  |
| PUT    | `/api/product/{id}`               | Update product                |
| DELETE | `/api/product/{id}`               | Delete product                |
| POST   | `/api/product/generate-description` | AI generate description     |
| POST   | `/api/product/generate-image`     | AI generate image (DALL-E 3)  |
| GET    | `/api/products/smart-search`      | Semantic search               |

### Orders

| Method | Endpoint            | Description       |
|--------|---------------------|-------------------|
| POST   | `/api/orders/place` | Place a new order |
| GET    | `/api/orders`       | Get all orders    |

### Chatbot

| Method | Endpoint        | Description              |
|--------|-----------------|--------------------------|
| GET    | `/api/chat/ask` | Ask the RAG chatbot      |

---

## Example Requests

### Add a Product (Postman / curl)

```
POST /api/product
Content-Type: multipart/form-data

product: {"name":"iPhone 15","description":"Latest iPhone","brand":"Apple","price":79999,"category":"Smartphones","product_available":true,"stock_quantity":50}
imageFile: (optional image file)
```

### Place an Order

```json
POST /api/orders/place
{
  "customer_name": "Navin Reddy",
  "email": "navin@telusko.com",
  "items": [
    { "product_id": 1, "quantity": 2 }
  ]
}
```

### Smart Search

```
GET /api/products/smart-search?query=wireless headphones under 5000
```

### Chat

```
GET /api/chat/ask?message=Do you have any laptops in stock?
```

---

## How It Works (Same as Spring Boot)

1. **Add Product** → Saved to SQLite + embedded into ChromaDB vector store
2. **Smart Search** → Query embedded → ChromaDB similarity search → LLM extracts product IDs → DB fetch
3. **Place Order** → Stock reduced → Product vector doc updated → Order indexed in vector store
4. **Chatbot** → User query → ChromaDB similarity search → LLM answers with RAG context + memory
5. **Generate Description** → GPT-4o generates a 250-char product description
6. **Generate Image** → DALL-E 3 generates professional product photo

---

## Notes

- SQLite file `ecom_ai.db` is auto-created on first run.
- ChromaDB data is persisted in `./chroma_db/` folder.
- Chat memory is in-memory (resets on server restart) — matches Spring Boot behavior.
