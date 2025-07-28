import { Separator } from "@/components/atoms/separator";

export function RightMenu() {
  return (
    <aside className="bg-stone-950 h-full w-xs xl:min-w-xs p-2 border-l-1 rounded-r-md">
      <div className="h-20 flex items-center justify-center">
        <code className="text-xs text-stone-500">v1.0 (DEMO)</code>
      </div>

      <Separator />

      <div className="py-8 px-2"></div>
    </aside>
  );
}
