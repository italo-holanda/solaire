import type { Thought } from "@/types";
import { Separator } from "@/components/atoms/separator";
import { preventTextOverflow } from "@/utils/formatting";
import { CategoryBadge } from "../category-badge/category-badge";
import { useGallery } from "@/hooks/use-gallery";

export function GalleryCard(props: Thought) {
  const title = props.title || props.text.slice(0, 25);

  const { isThoughtSelected, addSelectedThought, removeSelectedThought } =
    useGallery();

  return (
    <div
      role="button"
      className={`cursor-pointer bg-stone-850 hover:shadow-2xl p-3 border-1 rounded-lg ${
        isThoughtSelected(props.id)
          ? "border-amber-600"
          : "hover:border-stone-600"
      }`}
      onClick={() =>
        isThoughtSelected(props.id)
          ? removeSelectedThought(props.id)
          : addSelectedThought(props)
      }
    >
      <div className="h-70 flex flex-col gap-2 text-stone-300 text-sm justify-between">
        <h1 className="text-stone-200 leading-5.5 text-base">{title}</h1>
        <Separator />
        <p className="italic">
          "{(preventTextOverflow(props.text, 15) ?? "...").slice(0, 200)}..."
        </p>
        <Separator />
        <ul className="flex gap-1 flex-wrap">
          {props.categories.slice(0, 3).map((cat) => {
            return <CategoryBadge {...cat} />;
          })}

          {!props.categories.length && (
            <span className="text-xs py-4">No categories found</span>
          )}
        </ul>
      </div>
    </div>
  );
}
