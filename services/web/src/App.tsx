import { useMemo, useState } from "react";
import { useGroups } from "./hooks/useGroups";
import { useNews } from "./hooks/useNews";
import { useSourceStats } from "./hooks/useSourceStats";
import { Header } from "./components/Header";
import { SourceFilter } from "./components/SourceFilter";
import { ArticleCard } from "./components/ArticleCard";
import { GroupCard } from "./components/GroupCard";
import { SourceStatsView } from "./components/SourceStatsView";
import { AlgorithmView } from "./components/AlgorithmView";

type View = "news" | "groups" | "sources" | "algorithm";

export function App() {
  const [view, setView] = useState<View>("news");
  const [selectedSource, setSelectedSource] = useState<string | null>(null);

  const { articles, loading, error, refresh } = useNews();
  const { groups, loading: groupsLoading, error: groupsError, refresh: refreshGroups } = useGroups();
  const stats = useSourceStats(articles);

  const sources = useMemo(
    () => Array.from(new Set(articles.map((a) => a.source))).sort(),
    [articles],
  );

  const filtered = useMemo(
    () =>
      selectedSource === null
        ? articles
        : articles.filter((a) => a.source === selectedSource),
    [articles, selectedSource],
  );

  return (
    <div className="min-h-screen bg-gray-50">
      <Header view={view} onViewChange={setView} />

      <main className="max-w-5xl mx-auto px-4 py-6">
        {loading && (
          <p className="text-center text-gray-500 py-16">Cargando noticias…</p>
        )}

        {error && (
          <div className="text-center py-16">
            <p className="text-red-500 mb-4">{error}</p>
            <button
              onClick={refresh}
              className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
            >
              Reintentar
            </button>
          </div>
        )}

        {!loading && !error && view === "news" && (
          <>
            <div className="mb-4 flex items-center justify-between gap-4">
              <SourceFilter
                sources={sources}
                selected={selectedSource}
                onSelect={setSelectedSource}
              />
              <button
                onClick={refresh}
                className="text-sm text-gray-400 hover:text-indigo-600 transition-colors shrink-0"
              >
                Actualizar
              </button>
            </div>

            {filtered.length === 0 ? (
              <p className="text-center text-gray-400 py-16">Sin resultados.</p>
            ) : (
              <div className="grid gap-3">
                {filtered.map((a) => (
                  <ArticleCard key={a.id} article={a} />
                ))}
              </div>
            )}
          </>
        )}

        {view === "groups" && groupsLoading && (
          <p className="text-center text-gray-500 py-16">Cargando clusters…</p>
        )}

        {view === "groups" && groupsError && (
          <div className="text-center py-16">
            <p className="text-red-500 mb-4">{groupsError}</p>
            <button
              onClick={refreshGroups}
              className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
            >
              Reintentar
            </button>
          </div>
        )}

        {!groupsLoading && !groupsError && view === "groups" && (
          <>
            <div className="mb-4 flex items-center justify-between">
              <p className="text-sm text-gray-400">
                {groups.length} {groups.length === 1 ? "tema" : "temas"} con cobertura múltiple
              </p>
              <button
                onClick={refreshGroups}
                className="text-sm text-gray-400 hover:text-indigo-600 transition-colors"
              >
                Actualizar
              </button>
            </div>
            {groups.length === 0 ? (
              <p className="text-center text-gray-400 py-16">
                Aún no hay noticias agrupadas. Ejecuta el ingest primero.
              </p>
            ) : (
              <div className="grid gap-3">
                {groups.map((g) => (
                  <GroupCard key={g.id} group={g} />
                ))}
              </div>
            )}
          </>
        )}

        {!loading && !error && view === "sources" && (
          <SourceStatsView stats={stats} />
        )}

        {view === "algorithm" && <AlgorithmView />}
      </main>
    </div>
  );
}
