import { levelStyles } from "../lib/sensationalism";

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section className="bg-white rounded-lg shadow-sm border border-gray-100 p-6">
      <h2 className="text-lg font-semibold text-gray-800 mb-3">{title}</h2>
      {children}
    </section>
  );
}

function Badge({ className, children }: { className: string; children: React.ReactNode }) {
  return (
    <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${className}`}>
      {children}
    </span>
  );
}

export function AlgorithmView() {
  return (
    <div className="grid gap-6">
      <Section title="¿Qué es el Índice de Sensacionalismo?">
        <p className="text-gray-600 text-sm leading-relaxed">
          Cada noticia recibe un <strong>Índice de Sensacionalismo (IS)</strong> entre 0 y 1 que mide
          la proporción de lenguaje valorativo o emocional respecto al contenido informativo verificable.
          Un IS alto indica que el titular usa más juicios de valor que hechos concretos.
        </p>
      </Section>

      <Section title="Cómo se calcula">
        <ol className="text-sm text-gray-600 space-y-3 leading-relaxed list-none">
          <li className="flex gap-3">
            <span className="font-bold text-indigo-600 shrink-0">1.</span>
            <span>
              <strong>Unidades de Aserción (H)</strong> — se identifican los hechos verificables,
              datos objetivos y citas directas del titular y descripción.
            </span>
          </li>
          <li className="flex gap-3">
            <span className="font-bold text-indigo-600 shrink-0">2.</span>
            <span>
              <strong>Adjetivos subjetivos (A)</strong> — se extraen los adjetivos valorativos o
              emocionales (ej: "brutal", "vergonzoso", "preocupante"). Los adjetivos técnicos o
              descriptivos neutros (ej: "pública", "anual") no cuentan.
            </span>
          </li>
          <li className="flex gap-3">
            <span className="font-bold text-indigo-600 shrink-0">3.</span>
            <span>
              <strong>Fórmula:</strong>
              <code className="ml-2 px-2 py-0.5 bg-gray-100 rounded text-gray-700 font-mono text-xs">
                IS = A / (A + H)
              </code>
              <span className="ml-2 text-gray-500">
                — si A y H son 0, IS = 0.
              </span>
            </span>
          </li>
        </ol>
      </Section>

      <Section title="Código de colores">
        <div className="grid grid-cols-2 gap-3 sm:grid-cols-4 text-sm">
          {[
            { label: "Sin datos", range: "—", style: levelStyles.none },
            { label: "Bajo", range: "0 – 33%", style: levelStyles.low },
            { label: "Medio", range: "34 – 66%", style: levelStyles.medium },
            { label: "Alto", range: "67 – 100%", style: levelStyles.high },
          ].map(({ label, range, style }) => (
            <div key={label} className="flex flex-col items-center gap-2 p-3 rounded-lg bg-gray-50">
              <Badge className={style}>{label}</Badge>
              <span className="text-xs text-gray-500">{range}</span>
            </div>
          ))}
        </div>
      </Section>

      <Section title="Tecnología utilizada">
        <ul className="text-sm text-gray-600 space-y-2">
          <li>
            <strong>Modelo:</strong> GPT-4o mini (OpenAI) con temperatura 0 para máxima
            consistencia en los resultados.
          </li>
          <li>
            <strong>Entrada:</strong> Titular + descripción extraídos del feed RSS de cada medio.
            No se accede al texto completo del artículo.
          </li>
          <li>
            <strong>Salida:</strong> JSON estructurado con el índice, la lista de adjetivos
            subjetivos detectados y una explicación breve — visible al pasar el cursor por
            encima del badge en cada noticia.
          </li>
          <li>
            <strong>Frecuencia:</strong> El análisis se ejecuta automáticamente dos veces al día
            (8h y 18h UTC) para todas las noticias nuevas.
          </li>
        </ul>
      </Section>

      <Section title="Limitaciones">
        <ul className="text-sm text-gray-600 space-y-2 list-disc list-inside">
          <li>El análisis se basa solo en el titular y la descripción del RSS, no en el artículo completo.</li>
          <li>El modelo puede cometer errores en titulares muy cortos o con contexto ambiguo.</li>
          <li>El índice mide sensacionalismo lingüístico, no veracidad ni sesgo político.</li>
          <li>Medios con estilo más directo pueden obtener sistemáticamente puntuaciones más bajas.</li>
        </ul>
      </Section>
    </div>
  );
}
