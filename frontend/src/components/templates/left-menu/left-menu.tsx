import { Separator } from "@/components/atoms/separator";

export function LeftMenu() {
  return (
    <aside className="bg-stone-950 h-screen w-xs p-2 border-r-1 border-stone-800">
      <div className="p-3 flex items-center justify-center">
        <img src="/solaire.svg" height={39} width={140} />
      </div>

      <Separator />
    </aside>
  );
}
