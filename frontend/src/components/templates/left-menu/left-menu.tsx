import { Separator } from "@/components/atoms/separator";

import { SquarePlusIcon } from "lucide-react";
import { LayoutGridIcon } from "lucide-react";

import { Button } from "@/components/atoms/button";
import { SearchInput } from "@/components/molecules/search-input/search-input";
import { useNavigation } from "@/hooks/use-navigation";

export function LeftMenu() {
  const navigationHook = useNavigation();

  return (
    <aside className="bg-stone-950 h-full w-xs xl:min-w-xs p-2 border-r-1 rounded-l-md">
      <div className="h-20 flex items-center justify-center">
        <img src="/solaire.svg" height={39} width={140} />
      </div>

      <Separator />

      <div className="py-8 px-2">
        <SearchInput />

        <div className="py-7 flex flex-col gap-2">
          <span className="text-xs text-stone-300">Menu</span>
          <nav className="flex flex-col gap-3">
            <Button
              onClick={() => {
                navigationHook.setCurrentView("history");
                navigationHook.setParams({
                  searchTerms: "",
                  categories: undefined,
                });
              }}
              size="lg"
              variant={
                navigationHook.currentView === "history" ? "nav" : "navGhost"
              }
            >
              <SquarePlusIcon />
              New thought
            </Button>
            <Button
              onClick={() => navigationHook.setCurrentView("gallery")}
              size="lg"
              variant={
                navigationHook.currentView === "gallery" ? "nav" : "navGhost"
              }
            >
              <LayoutGridIcon />
              Gallery of thoughts
            </Button>
          </nav>
        </div>
      </div>
    </aside>
  );
}
