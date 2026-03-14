export type Bias = "left" | "center" | "right";

export interface NewsArticle {
  id: string;
  title: string;
  link: string;
  description: string | null;
  published: string | null;
  source: string;
  bias: Bias;
  sensationalism_score: number | null;
  sensationalism_explanation: string | null;
}

export interface NewsResponse {
  news: NewsArticle[];
}

export interface GroupArticle {
  id: string;
  title: string;
  link: string;
  description: string | null;
  published: string | null;
  source: string;
  bias: Bias;
  sensationalism_score: number | null;
  sensationalism_explanation: string | null;
}

export interface NewsGroup {
  id: string;
  created_at: string | null;
  articles: GroupArticle[];
}

export interface GroupsResponse {
  groups: NewsGroup[];
}

export interface SourceStats {
  source: string;
  bias: Bias;
  count: number;
  avg_score: number | null;
}
