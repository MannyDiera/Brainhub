import hashlib
from urllib.parse import parse_qs, urlparse

def extraer_video_id_youtube(url: str) -> str | None:
    parsed = urlparse(url.strip())
    host = parsed.netloc.lower().removeprefix("www.")

    if host in {"youtube.com", "m.youtube.com", "music.youtube.com"}:
        if parsed.path == "/watch":
            return parse_qs(parsed.query).get("v", [None])[0]
        partes = [p for p in parsed.path.split("/") if p]
        if len(partes) >= 2 and partes[0] in {"shorts", "embed", "live"}:
            return partes[1]

    if host == "youtu.be":
        return parsed.path.strip("/").split("/")[0] or None

    return None

def extraer_id_github(url: str) -> str | None:
    parsed = urlparse(url.strip())
    host = parsed.netloc.lower().removeprefix("www.")
    
    if host != "github.com":
        return None
    
    path = parsed.path.strip("/")
    partes = path.split("/")
    
    # Debe tener al menos usuario/repo
    if len(partes) >= 2:
        return f"github:{partes[0]}/{partes[1]}"
    
    return None

def generar_content_id(url: str) -> str:
    # 1. YouTube
    video_id = extraer_video_id_youtube(url)
    if video_id:
        return f"youtube:{video_id}"
    
    # 2. GitHub
    github_id = extraer_id_github(url)
    if github_id:
        return github_id
    
    # 3. URL genérica: hash
    digest = hashlib.sha256(url.strip().encode("utf-8")).hexdigest()[:16]
    return f"url:{digest}"

def generar_hash(texto: str) -> str:
    if not texto:
        return ''
    texto_normalizado = ' '.join(texto.split()).strip().lower()
    return hashlib.sha256(texto_normalizado.encode()).hexdigest()[:16]

def normalizar_url(url: str) -> str:
    return url
