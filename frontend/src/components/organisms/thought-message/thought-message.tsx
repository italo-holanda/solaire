import { Button } from "@/components/atoms/button";
import { CategoryBadge } from "@/components/molecules/category-badge/category-badge";
import { Blockquote } from "@/components/atoms/blockquote";
import { ChevronDownIcon } from "lucide-react";
import { useState } from "react";

export function ThoughtMessage() {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <>
      <div className="bg-stone-850 border-1 rounded-lg">
        <article className="p-6 flex gap-3">
          <figure className="flex flex-col items-center gap-2 w-10">
            <img
              className="bg-amber-400 rounded-full"
              width={32}
              src="/user.svg"
              alt="user"
            />
            <legend className="text-xs text-stone-500">16/07</legend>
          </figure>

          <div className="flex flex-col gap-2">
            <p className="text-base/6.5 text-stone-200">
              sometimes walking through tallinn feels like slipping between
              layers of time… cobblestones underfoot, old soviet blocks staring
              down at you, and the wind off the baltic that never really warms
              up, not even in july. it’s quiet here, even when it’s busy. like
              the city’s whispering something you’re not quite meant to hear. i
              drink coffee in cafés with names i can’t pronounce, watch the fog
              roll in over telliskivi rooftops, and wonder if i’m becoming
              someone new or just forgetting bits of who i was. the nights are
              long, or too short. depending on the season or maybe my mood.
              there’s this stillness here, like the city knows how to wait.
              maybe i'm learning that too. sometimes it’s lonely, but not the
              bad kind. just a space where your thoughts echo a little louder.
              like tallinn’s giving them room to stretch. strange comfort in
              that.
            </p>

            <div className="flex justify-between">
              <div className="flex gap-2">
                <Button variant="ghost">Edit</Button>
                <Button variant="ghost">Delete</Button>
              </div>

              <Button
                onClick={() => setIsExpanded((p) => !p)}
                variant={isExpanded ? "outline" : "ghost"}
              >
                <ChevronDownIcon />
              </Button>
            </div>
          </div>
        </article>
      </div>

      {isExpanded && (
        <div className="bg-stone-950 border-1 border-t-transparent rounded-b-lg">
          <article className="p-6 flex gap-3">
            <figure className="flex flex-col items-center gap-2 min-w-10">
              <img width={32} src="/solaire-ico.svg" alt="user" />
            </figure>

            <div className="flex flex-col gap-2">
              <h1>
                Finding Stillness and Identity in the Quiet Streets of Tallinn
              </h1>

              <p className="text-stone-300">
                Your thought seems like it’s walking slowly through the quiet
                streets of Tallinn—where old stones remember too much and the
                wind carries pieces of something you can’t quite name. Time
                bends here, folding history into your everyday steps, and
                suddenly you’re not sure if you’re lost or just finally slowing
                down.
              </p>

              <div className="flex flex-col gap-1">
                <h2 className="text-sm text-stone-400">Categories</h2>
                <ul className="flex gap-1">
                  <li>
                    <CategoryBadge name="travel" color="#8C6CFF" />
                  </li>
                  <li>
                    <CategoryBadge name="art" color="#FF6C6C" />
                  </li>
                  <li>
                    <CategoryBadge name="history" color="#FF6CF0" />
                  </li>
                </ul>
              </div>

              <div className="flex flex-col gap-2">
                <h2 className="text-sm text-stone-400">Related to</h2>
                <ul className="flex flex-wrap gap-2">
                  <li>
                    <Blockquote text="My last weekend in Tallinn" />
                  </li>

                  <li>
                    <Blockquote text="The dark forests of Estonia" />
                  </li>

                  <li>
                    <Blockquote text="Exploring coffee tastes in the Baltics" />
                  </li>
                </ul>
              </div>
            </div>
          </article>
        </div>
      )}
    </>
  );
}
