interface SourceFilterProps {
  sources: string[];
  selected: string | null;
  onSelect: (source: string | null) => void;
}

export function SourceFilter({ sources, selected, onSelect }: SourceFilterProps) {
  return (
    <div className="flex flex-wrap gap-2">
      <button
        onClick={() => onSelect(null)}
        className={`px-3 py-1 rounded-full text-sm font-medium transition-colors ${
          selected === null
            ? "bg-indigo-600 text-white"
            : "bg-gray-100 text-gray-600 hover:bg-gray-200"
        }`}
      >
        Todas
      </button>
      {sources.map((s) => (
        <button
          key={s}
          onClick={() => onSelect(s)}
          className={`px-3 py-1 rounded-full text-sm font-medium transition-colors ${
            selected === s
              ? "bg-indigo-600 text-white"
              : "bg-gray-100 text-gray-600 hover:bg-gray-200"
          }`}
        >
          {s}
        </button>
      ))}
    </div>
  );
}
