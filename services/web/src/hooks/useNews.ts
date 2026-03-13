import { useCallback, useEffect, useState } from "react";
import { fetchNews } from "../api/client";
import type { NewsArticle } from "../api/types";

interface UseNewsResult {
  articles: NewsArticle[];
  loading: boolean;
  error: string | null;
  refresh: () => void;
}

export function useNews(): UseNewsResult {
  const [articles, setArticles] = useState<NewsArticle[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [tick, setTick] = useState(0);

  const refresh = useCallback(() => setTick((t) => t + 1), []);

  useEffect(() => {
    const controller = new AbortController();
    setLoading(true);
    setError(null);

    fetchNews(controller.signal)
      .then((data) => {
        setArticles(data.news);
        setLoading(false);
      })
      .catch((err: unknown) => {
        if (err instanceof Error && err.name === "AbortError") return;
        setError(err instanceof Error ? err.message : "Error desconocido");
        setLoading(false);
      });

    return () => controller.abort();
  }, [tick]);

  return { articles, loading, error, refresh };
}
