import { Separator } from "@/components/atoms/separator";
import { CategoryList } from "@/components/molecules/category-list/category-list";
import { RecentThoughts } from "@/components/molecules/recent-thoughts/recent-thoughts";

export function RightMenu() {
  return (
    <aside className="bg-stone-950 h-full w-xs xl:min-w-xs p-2 border-l-1 rounded-r-md">
      <div className="h-20 flex items-center justify-center">
        <code className="text-xs text-stone-500">v1.0 (DEMO)</code>
      </div>

      <Separator />

      <div className="py-8 px-4 flex flex-col gap-2">
        <span className="text-xs text-stone-300">Last thoughts</span>
        <RecentThoughts />
      </div>

      <div className="px-4 flex flex-col gap-2">
        <span className="text-xs text-stone-300">Categories</span>
        <CategoryList />
      </div>
    </aside>
  );
}
