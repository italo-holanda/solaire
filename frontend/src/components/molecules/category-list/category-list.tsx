import { useThoughts } from "@/hooks/use-thoughts";
import { CategoryBadge } from "../category-badge/category-badge";
import { useMemo } from "react";

export function CategoryList() {
  const { data } = useThoughts();

  const categories = useMemo(() => {
    const allCategories = data?.flatMap((th) => th.categories) ?? [];
    const uniqueCategories = allCategories.filter((cat, index, self) => 
      index === self.findIndex((c) => c.id === cat.id)
    );
    return uniqueCategories;
  }, [data]);

  return (
    <ul className="flex flex-wrap gap-1 overflow-y-scroll max-h-60 bg-stone-900 p-3 border-1 rounded-lg overflow-x-hidden">
      {categories.map((cat) => (
        <li key={cat.id}>
          <CategoryBadge {...cat} />
        </li>
      ))}
    </ul>
  );
}
