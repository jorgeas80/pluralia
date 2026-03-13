import type { NewsArticle } from "../api/types";
import { BiasIndicator } from "./BiasIndicator";
import { SensationalismBadge } from "./SensationalismBadge";

export function ArticleCard({ article }: { article: NewsArticle }) {
  return (
    <article className="bg-white rounded-lg shadow-sm border border-gray-100 p-4 hover:shadow-md transition-shadow">
      <div className="flex items-start gap-3">
        <div className="flex-1 min-w-0">
          <a
            href={article.link}
            target="_blank"
            rel="noopener noreferrer"
            className="text-gray-900 font-medium hover:text-indigo-600 transition-colors line-clamp-2"
          >
            {article.title}
          </a>
          {article.description && (
            <p className="mt-1 text-sm text-gray-500 line-clamp-2">{article.description}</p>
          )}
        </div>
      </div>
      <div className="mt-3 flex flex-wrap items-center gap-2 text-xs text-gray-400">
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
    </article>
  );
}
