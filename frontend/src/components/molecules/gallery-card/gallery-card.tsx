import type { Thought } from "@/types";
import { Separator } from "@/components/atoms/separator";
import { preventTextOverflow } from "@/utils/formatting";
import { CategoryBadge } from "../category-badge/category-badge";

export function GalleryCard(props: Thought) {
  const title = props.title || props.text.slice(0, 25);

  return (
    <div role="button" className="cursor-pointer bg-stone-850 hover:shadow-2xl hover:border-stone-600 p-3 border-1 rounded-lg">
      <div className="h-65 flex flex-col gap-2 text-stone-300 text-sm justify-between">
        <h1 className="text-stone-200 leading-5.5 text-base">{title}</h1>
        <Separator />
        <p className="italic">
          "{(preventTextOverflow(props.text, 15) ?? "...").slice(0, 200)}..."
        </p>
        <Separator />
        <ul className="flex gap-1 flex-wrap">
          {props.categories.slice(0, 3).map((cat) => {
            const safeName = cat.name.length <= 8 ? cat.name : cat.name.slice(0, 5) + '...'

            return (
              <CategoryBadge
                color={cat.color ?? "green"}
                name={safeName}
              />
            );
          })}

          {!props.categories.length && (
            <span className="text-xs py-4">No categories found</span>
          )}
        </ul>
      </div>
    </div>
  );
}
