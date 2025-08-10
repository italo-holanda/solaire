import { Button } from "@/components/atoms/button";
import { CategoryBadge } from "@/components/molecules/category-badge/category-badge";
import { useNavigation } from "@/hooks/use-navigation";
import { TrashIcon } from "lucide-react";

export function SelectedFilters() {
  const { params, setParams } = useNavigation();

  const hasFilters = !!params.categories?.length || params.searchTerms;

  if (!hasFilters)
    return <div className="text-stone-400 text-sm">No filters selected</div>;

  return (
    <div className="flex flex-col gap-1">
      <div className="flex flex-col gap-3 overflow-y-scroll max-h-60 bg-stone-900 p-3 border-1 rounded-lg">
        {params.searchTerms && (
          <div className="flex flex-col text-sm">
            <span className="text-xs text-stone-300">Searching for:</span>{" "}
            <i className="text-stone-200">"{params.searchTerms}"</i>
          </div>
        )}

        {!!params.categories?.length && (
          <ul className="flex gap-1 flex-wrap">
            <span className="text-xs text-stone-300">Selected categories:</span>
            {params.categories.map((cat) => (
              <CategoryBadge key={cat.id} {...cat} />
            ))}
          </ul>
        )}
      </div>
      <Button
        variant="outline"
        onClick={() => setParams({ searchTerms: "", categories: [] })}
        size="xs"
      >
        <TrashIcon />
        Clean all filters
      </Button>
    </div>
  );
}
