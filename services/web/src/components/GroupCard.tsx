import type { NewsGroup, Bias } from "../api/types";
import { BiasIndicator } from "./BiasIndicator";
import { SensationalismBadge } from "./SensationalismBadge";

const biasOrder: Bias[] = ["left", "center", "right"];

const biasColors: Record<Bias, string> = {
  left: "bg-blue-400",
  center: "bg-gray-400",
  right: "bg-orange-400",
};

export function GroupCard({ group }: { group: NewsGroup }) {
  const sorted = [...group.articles].sort(
    (a, b) => biasOrder.indexOf(a.bias) - biasOrder.indexOf(b.bias),
  );

  const biasCounts = sorted.reduce<Record<Bias, number>>(
    (acc, a) => ({ ...acc, [a.bias]: (acc[a.bias] ?? 0) + 1 }),
    { left: 0, center: 0, right: 0 },
  );

  const total = group.articles.length;

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-100 p-4">
      {/* Header: bias bar + source count */}
      <div className="flex items-center gap-3 mb-3">
        <div className="flex flex-1 h-2 rounded-full overflow-hidden gap-px">
          {biasOrder.map((bias) =>
            biasCounts[bias] > 0 ? (
              <div
                key={bias}
                className={`${biasColors[bias]} transition-all`}
                style={{ width: `${(biasCounts[bias] / total) * 100}%` }}
              />
            ) : null,
          )}
        </div>
        <span className="text-xs text-gray-400 shrink-0">
          {total} {total === 1 ? "fuente" : "fuentes"}
        </span>
      </div>

      {/* Article list */}
      <div className="divide-y divide-gray-50">
        {sorted.map((article) => (
          <div key={article.id} className="py-2 first:pt-0 last:pb-0">
            <a
              href={article.link}
              target="_blank"
              rel="noopener noreferrer"
              className="text-sm text-gray-800 font-medium hover:text-indigo-600 transition-colors line-clamp-2"
            >
              {article.title}
            </a>
            <div className="mt-1 flex flex-wrap items-center gap-2 text-xs text-gray-400">
              <span className="font-medium text-gray-600">{article.source}</span>
              {article.published && (
                <span>{new Date(article.published).toLocaleDateString("es-ES")}</span>
              )}
              <BiasIndicator bias={article.bias} />
              <SensationalismBadge
                score={article.sensationalism_score}
                explanation={article.sensationalism_explanation}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
