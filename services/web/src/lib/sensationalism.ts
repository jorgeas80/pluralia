export type SensationalismLevel = "none" | "low" | "medium" | "high";

export function scoreToLevel(score: number | null): SensationalismLevel {
  if (score === null) return "none";
  if (score <= 0.33) return "low";
  if (score <= 0.66) return "medium";
  return "high";
}

export const levelStyles: Record<SensationalismLevel, string> = {
  none: "bg-gray-100 text-gray-500",
  low: "bg-green-100 text-green-700",
  medium: "bg-amber-100 text-amber-700",
  high: "bg-red-100 text-red-700",
};

export const levelLabel: Record<SensationalismLevel, string> = {
  none: "—",
  low: "bajo",
  medium: "medio",
  high: "alto",
};
