import type { SourceStats } from "../api/types";
import { BiasIndicator } from "./BiasIndicator";
import { scoreToLevel, levelStyles, levelLabel } from "../lib/sensationalism";

export function SourceStatsView({ stats }: { stats: SourceStats[] }) {
  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm text-left">
        <thead>
          <tr className="border-b border-gray-200 text-gray-500 text-xs uppercase tracking-wider">
            <th className="pb-2 pr-4">Fuente</th>
            <th className="pb-2 pr-4">Sesgo</th>
            <th className="pb-2 pr-4 text-right">Artículos</th>
            <th className="pb-2 text-right">Sensacionalismo medio</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-100">
          {stats.map((s) => {
            const level = scoreToLevel(s.avg_score);
            const pct =
              s.avg_score !== null ? `${Math.round(s.avg_score * 100)}%` : "—";
            return (
              <tr key={s.source} className="hover:bg-gray-50">
                <td className="py-2 pr-4 font-medium text-gray-800">{s.source}</td>
                <td className="py-2 pr-4">
                  <BiasIndicator bias={s.bias} />
                </td>
                <td className="py-2 pr-4 text-right text-gray-600">{s.count}</td>
                <td className="py-2 text-right">
                  <span
                    className={`px-2 py-0.5 rounded-full text-xs font-medium ${levelStyles[level]}`}
                  >
                    {pct !== "—" ? `${pct} · ${levelLabel[level]}` : levelLabel[level]}
                  </span>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
