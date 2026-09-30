"""Inference back-ends. Both receive the same system prompt, user prompt, JSON
schema, temperature and seed, and return (text, seconds, tokens)."""

import time

import requests


class Ollama:
    """Same call as production (/api/generate with a JSON schema)."""

    def __init__(self, model: str, url: str = "http://127.0.0.1:11434", options: dict | None = None):
        self.model, self.url, self.extra = model, url.rstrip("/"), dict(options or {})

    def generate(self, system, prompt, seed, schema, temperature, num_predict, num_ctx):
        payload = {"model": self.model, "system": system, "prompt": prompt, "stream": False, "format": schema,
                   "options": {"temperature": temperature, "seed": seed, "num_predict": num_predict,
                               "num_ctx": num_ctx}}
        if "think" in self.extra:  # thinking models: off, for speed and a comparable answer format
            payload["think"] = self.extra["think"]
        t0 = time.monotonic()
        resp = requests.post(f"{self.url}/api/generate", json=payload, timeout=900)
        if resp.status_code == 400 and "think" in payload and "think" in resp.text.lower():
            payload.pop("think")  # model without a thinking mode
            resp = requests.post(f"{self.url}/api/generate", json=payload, timeout=900)
        resp.raise_for_status()
        data = resp.json()
        return data.get("response", ""), time.monotonic() - t0, data.get("eval_count")

    def info(self) -> dict:
        out = {}
        try:
            out["server_version"] = requests.get(f"{self.url}/api/version", timeout=10).json().get("version")
            for t in requests.get(f"{self.url}/api/tags", timeout=10).json().get("models", []):
                if self.model in (t.get("name"), t.get("model")):
                    out["digest"] = t.get("digest")
                    out["size_bytes"] = t.get("size")
                    out["details"] = t.get("details")
        except requests.RequestException:
            pass
        return out


class LlamaCpp:
    """llama.cpp's llama-server, OpenAI-compatible endpoint with a JSON-schema constraint."""

    def __init__(self, model: str, url: str = "http://127.0.0.1:8080", options: dict | None = None):
        self.model, self.url, self.extra = model, url.rstrip("/"), dict(options or {})

    def generate(self, system, prompt, seed, schema, temperature, num_predict, num_ctx):
        payload = {
            "model": self.model,
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": prompt}],
            "temperature": temperature, "seed": seed, "max_tokens": num_predict,
            "response_format": {"type": "json_schema", "json_schema": {"name": "answer", "schema": schema}},
        }
        if "chat_template_kwargs" in self.extra:  # e.g. {"enable_thinking": false}
            payload["chat_template_kwargs"] = self.extra["chat_template_kwargs"]
        t0 = time.monotonic()
        resp = requests.post(f"{self.url}/v1/chat/completions", json=payload, timeout=900)
        resp.raise_for_status()
        data = resp.json()
        tokens = (data.get("usage") or {}).get("completion_tokens")
        return data["choices"][0]["message"]["content"], time.monotonic() - t0, tokens

    def info(self) -> dict:
        try:
            props = requests.get(f"{self.url}/props", timeout=10).json()
            return {"server_version": props.get("build_info"), "model_path": props.get("model_path")}
        except requests.RequestException:
            return {}


def make(entry: dict):
    cls = {"ollama": Ollama, "llamacpp": LlamaCpp, "llamacpp-prism": LlamaCpp}[entry["backend"]]
    return cls(entry["model"], options=entry.get("options"))
