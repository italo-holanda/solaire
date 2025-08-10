import { useThoughts } from "@/hooks/use-thoughts";
import { CategoryBadge } from "../category-badge/category-badge";
import { useMemo } from "react";

export function CategoryList() {
  const { data } = useThoughts();

  const categoires = useMemo(() => {
    return data?.flatMap((th) => th.categories) ?? [];
  }, [data]);

  return (
    <ul className="flex flex-col gap-2 overflow-y-scroll max-h-60 bg-stone-900 p-3 border-1 rounded-lg">
      {categoires.map((cat) => (
        <li key={cat.id}>
          <CategoryBadge color={cat.color ?? "green"} name={cat.name} />
        </li>
      ))}
    </ul>
  );
}
