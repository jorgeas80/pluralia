import type { Bias } from "../api/types";

const styles: Record<Bias, string> = {
  left: "bg-blue-100 text-blue-700",
  center: "bg-gray-100 text-gray-600",
  right: "bg-orange-100 text-orange-700",
};

const labels: Record<Bias, string> = {
  left: "izquierda",
  center: "centro",
  right: "derecha",
};

export function BiasIndicator({ bias }: { bias: Bias }) {
  return (
    <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${styles[bias]}`}>
      {labels[bias]}
    </span>
  );
}
