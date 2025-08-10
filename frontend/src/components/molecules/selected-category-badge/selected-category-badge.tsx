import { Badge } from "@/components/atoms/badge";
import { useNavigation } from "@/hooks/use-navigation";
import type { Category } from "@/types";

export function SelectedCategoryBadge(props: Category) {
  const { params, setParams } = useNavigation();

  function handleClick() {
    const currentCategories = params.categories ?? [];
    const filteredCategories = currentCategories.filter(category => category.id !== props.id);
    
    setParams({
      ...params,
      categories: filteredCategories,
    });
  }

  return (
    <Badge
      onClick={handleClick}
      role="button"
      variant="outline"
      className="cursor-pointer hover:bg-red-900/20 hover:border-red-500"
    >
      <div
        style={{ backgroundColor: props.color }}
        className="min-h-2 h-2 max-h-2 min-w-2 w-2 max-w-2 rounded-full"
      />
      <span className="text-xs text-stone-300">{props.name}</span>
    </Badge>
  );
} 