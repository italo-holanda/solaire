import { Badge } from "@/components/atoms/badge";

type CategoryBadgeProps = {
  name: string;
  color: string;
};

export function CategoryBadge(props: CategoryBadgeProps) {
  return (
    <Badge variant="outline">
      <div
        style={{ backgroundColor: props.color }}
        className="min-h-2 h-2 max-h-2 min-w-2 w-2 max-w-2 rounded-full"
      />
      <span className="text-xs text-stone-300">{props.name}</span>
    </Badge>
  );
}
