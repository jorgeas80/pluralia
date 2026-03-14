type View = "news" | "groups" | "sources";

interface HeaderProps {
  view: View;
  onViewChange: (v: View) => void;
}

export function Header({ view, onViewChange }: HeaderProps) {
  const tab = (v: View, label: string) => (
    <button
      onClick={() => onViewChange(v)}
      className={`px-4 py-2 text-sm font-medium rounded-t-lg transition-colors ${
        view === v
          ? "bg-white text-indigo-600 border-b-2 border-indigo-600"
          : "text-gray-500 hover:text-gray-700"
      }`}
    >
      {label}
    </button>
  );

  return (
    <header className="bg-indigo-700 text-white shadow">
      <div className="max-w-5xl mx-auto px-4 pt-4">
        <h1 className="text-2xl font-bold mb-3">Pluralia</h1>
        <nav className="flex gap-1">
          {tab("news", "Noticias")}
          {tab("groups", "Clusters")}
          {tab("sources", "Fuentes")}
        </nav>
      </div>
    </header>
  );
}
