# NEXUS AI — Configuración multimodelo 0.9

El backend admite varios proveedores y modelos desde la variable privada `NEXUS_PROVIDERS_JSON` en Render.

Integraciones contempladas: OpenAI, Anthropic/Claude, Google/Gemini, xAI/Grok, DeepSeek, Mistral, Cohere, Alibaba/Qwen, Moonshot/Kimi, Z.ai/GLM, Baidu/ERNIE, ByteDance/Doubao, NVIDIA NIM, Amazon Bedrock, Azure AI Foundry, OpenRouter, Together AI, Groq, Fireworks, Cerebras, SambaNova, Hugging Face Inference, Cloudflare Workers AI y Ollama.

El directorio no significa que estén conectadas automáticamente ni que incluya literalmente todas las IA del mundo. Solo funcionan los proveedores que se configuren con credenciales válidas y modelos actualmente disponibles. Se soportan adaptadores `openai` (API compatible), `anthropic` y `gemini`.

Ejemplo de estructura (usar credenciales y IDs reales en Render; nunca guardar claves en Godot o en la APK):

```json
[
  {
    "id": "openrouter",
    "name": "OpenRouter",
    "kind": "openai",
    "base_url": "https://openrouter.ai/api/v1",
    "api_key": "CLAVE_PRIVADA",
    "models": [{"id": "ID_REAL_DEL_MODELO", "name": "Nombre del modelo"}]
  },
  {
    "id": "anthropic",
    "name": "Anthropic",
    "kind": "anthropic",
    "base_url": "https://api.anthropic.com/v1",
    "api_key": "CLAVE_PRIVADA",
    "models": [{"id": "ID_REAL_DEL_MODELO", "name": "Claude"}]
  },
  {
    "id": "google",
    "name": "Google Gemini",
    "kind": "gemini",
    "base_url": "https://generativelanguage.googleapis.com/v1beta",
    "api_key": "CLAVE_PRIVADA",
    "models": [{"id": "ID_REAL_DEL_MODELO", "name": "Gemini"}]
  }
]
```

Rutas: `GET /api/models`, `GET /api/providers`, `GET /api/status`, `POST /api/chat`. El chat acepta `messages` y opcionalmente `provider` + `model`.

Algunos proveedores cobran por uso. No configurar facturación ni compartir claves sin autorización del titular adulto de la cuenta. El backend no ejecuta código ni acciones externas.
