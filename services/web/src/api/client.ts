import type { GroupsResponse, NewsResponse } from "./types";

const BASE_URL = (import.meta.env.VITE_API_URL as string | undefined) ?? "";

function newsUrl(limit: number): string {
  if (import.meta.env.PROD) return "/data/news.json";
  return `${BASE_URL}/news?limit=${limit}`;
}

function groupsUrl(limit: number): string {
  if (import.meta.env.PROD) return "/data/groups.json";
  return `${BASE_URL}/groups?limit=${limit}`;
}

export async function fetchGroups(
  signal?: AbortSignal,
  limit = 50,
): Promise<GroupsResponse> {
  const res = await fetch(groupsUrl(limit), { signal });
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json() as Promise<GroupsResponse>;
}

export async function fetchNews(
  signal?: AbortSignal,
  limit = 100,
): Promise<NewsResponse> {
  const res = await fetch(newsUrl(limit), { signal });
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json() as Promise<NewsResponse>;
}
