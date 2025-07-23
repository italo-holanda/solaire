import { Separator } from "@/components/atoms/separator";

import { SquarePlusIcon } from "lucide-react";
import { LayoutGridIcon } from "lucide-react";

import { Button } from "@/components/atoms/button";
import { SearchInput } from "@/components/molecules/search-input/search-input";

export function LeftMenu() {
  return (
    <aside className="bg-stone-950 h-screen w-xs xl:min-w-xs p-2 border-r-1 border-stone-800">
      <div className="h-20 flex items-center justify-center">
        <img src="/solaire.svg" height={39} width={140} />
      </div>

      <Separator />

      <div className="py-8 px-2">
        <SearchInput />

        <div className="py-7 flex flex-col gap-2">
          <span className="text-xs text-stone-300">Menu</span>
          <nav className="flex flex-col gap-3">
            <Button size="lg" variant="nav">
              <SquarePlusIcon />
              New thought
            </Button>
            <Button size="lg" variant="navGhost">
              <LayoutGridIcon />
              Gallery of thoughts
            </Button>
          </nav>
        </div>
      </div>
    </aside>
  );
}
