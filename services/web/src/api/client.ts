import type { NewsResponse } from "./types";

const BASE_URL = (import.meta.env.VITE_API_URL as string | undefined) ?? "";

export async function fetchNews(
  signal?: AbortSignal,
  limit = 100,
): Promise<NewsResponse> {
  const res = await fetch(`${BASE_URL}/news?limit=${limit}`, { signal });
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json() as Promise<NewsResponse>;
}
