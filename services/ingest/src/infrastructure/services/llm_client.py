import json
import logging
from typing import Tuple, Dict, Any

from openai import AsyncOpenAI
from libs.domain.services.analysis_service import NewsAnalyzer

logger = logging.getLogger(__name__)

SENSATIONALISM_PROMPT = """
Rol: Eres un lingüista experto en análisis político y detección de sesgos.

Objetivo: Calcular el "Índice de Sensacionalismo" (IS) basado en la densidad de adjetivación subjetiva por unidad de información.

Instrucciones:
1. Segmentación de Hechos (Denominador): Identifica "Unidades de Aserción" (hechos verificables, datos, citas directas). Cuenta total = H.
2. Extracción de Adjetivos (Numerador):
   - Tipo A (Funcionales): Descriptivos, técnicos (ej: "pública", "anual"). Valor = 0.
   - Tipo B (Valorativos/Emocionales): Juicios de valor, carga emocional (ej: "preocupante", "brutal", "vergonzoso"). Valor = 1. Cuenta total = A_sub.
3. Cálculo: IS = A_sub / H. (Si H=0, IS=0).
4. Normalización: Escala 0-1. IS > 0.5 es saturación.

Analiza el siguiente texto (Titular + Descripción):
Titulo: {title}
Descripción: {description}

Formato de Salida (JSON estricto):
{{
  "hechos_count": int,
  "adjetivos_subjetivos": [lista de strings],
  "explicacion_breve": "string justificando",
  "indice_sensacionalismo": float (0.0 - 1.0)
}}
"""

class OpenAINewsAnalyzer(NewsAnalyzer):
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model

    async def analyze_sensationalism(self, title: str, content: str) -> Tuple[float, str, Dict]:
        try:
            prompt = SENSATIONALISM_PROMPT.format(title=title, description=content)

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that outputs JSON."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.0
            )

            content_str = response.choices[0].message.content
            if not content_str:
                return 0.0, "No response from LLM", {}

            data = json.loads(content_str)

            score = float(data.get("indice_sensacionalismo", 0.0))
            explanation = data.get("explicacion_breve", "")
            metadata = {
                "hechos_count": data.get("hechos_count"),
                "adjetivos_subjetivos": data.get("adjetivos_subjetivos")
            }

            return score, explanation, metadata

        except Exception as e:
            logger.error(f"Error analyzing sensationalism: {e}")
            return 0.0, f"Error: {str(e)}", {}
