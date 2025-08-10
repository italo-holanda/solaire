import { Badge } from "@/components/atoms/badge";
import { useNavigation } from "@/hooks/use-navigation";
import type { Category } from "@/types";

export function CategoryBadge(props: Category) {
  const { params, setParams, getParams, setCurrentView } = useNavigation();

  function handleClick() {
    const currentCategories = getParams().categories ?? [];
    const categoryExists = currentCategories.some(category => category.id === props.id);
    
    if (!categoryExists) {
      setParams({
        ...params,
        categories: currentCategories.concat(props),
      });
    }
    setCurrentView("gallery");
  }

  return (
    <Badge
      onClick={handleClick}
      role="button"
      variant="outline"
      className="cursor-pointer"
    >
      <div
        style={{ backgroundColor: props.color }}
        className="min-h-2 h-2 max-h-2 min-w-2 w-2 max-w-2 rounded-full"
      />
      <span className="text-xs text-stone-300">{props.name}</span>
    </Badge>
  );
}
