import { useMemo } from "react";
import type { NewsArticle, SourceStats } from "../api/types";

export function useSourceStats(articles: NewsArticle[]): SourceStats[] {
  return useMemo(() => {
    const map = new Map<string, { bias: string; scores: number[]; count: number }>();

    for (const a of articles) {
      const existing = map.get(a.source);
      if (existing) {
        existing.count++;
        if (a.sensationalism_score !== null) {
          existing.scores.push(a.sensationalism_score);
        }
      } else {
        map.set(a.source, {
          bias: a.bias,
          count: 1,
          scores: a.sensationalism_score !== null ? [a.sensationalism_score] : [],
        });
      }
    }

    return Array.from(map.entries()).map(([source, data]) => ({
      source,
      bias: data.bias as SourceStats["bias"],
      count: data.count,
      avg_score:
        data.scores.length > 0
          ? data.scores.reduce((s, v) => s + v, 0) / data.scores.length
          : null,
    }));
  }, [articles]);
}
