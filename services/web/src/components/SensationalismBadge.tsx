import { scoreToLevel, levelStyles, levelLabel } from "../lib/sensationalism";

interface SensationalismBadgeProps {
  score: number | null;
  explanation: string | null;
}

export function SensationalismBadge({ score, explanation }: SensationalismBadgeProps) {
  const level = scoreToLevel(score);
  const pct = score !== null ? `${Math.round(score * 100)}%` : null;

  return (
    <span
      title={explanation ?? undefined}
      className={`px-2 py-0.5 rounded-full text-xs font-medium cursor-default ${levelStyles[level]}`}
    >
      {pct !== null ? `${pct} · ${levelLabel[level]}` : levelLabel[level]}
    </span>
  );
}
