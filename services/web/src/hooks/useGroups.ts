import { useCallback, useEffect, useState } from "react";
import { fetchGroups } from "../api/client";
import type { NewsGroup } from "../api/types";

interface UseGroupsResult {
  groups: NewsGroup[];
  loading: boolean;
  error: string | null;
  refresh: () => void;
}

export function useGroups(): UseGroupsResult {
  const [groups, setGroups] = useState<NewsGroup[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [tick, setTick] = useState(0);

  const refresh = useCallback(() => setTick((t) => t + 1), []);

  useEffect(() => {
    const controller = new AbortController();
    setLoading(true);
    setError(null);

    fetchGroups(controller.signal)
      .then((data) => {
        setGroups(data.groups);
        setLoading(false);
      })
      .catch((err: unknown) => {
        if (err instanceof Error && err.name === "AbortError") return;
        setError(err instanceof Error ? err.message : "Error desconocido");
        setLoading(false);
      });

    return () => controller.abort();
  }, [tick]);

  return { groups, loading, error, refresh };
}
