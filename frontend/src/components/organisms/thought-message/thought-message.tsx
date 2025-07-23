import { Button } from "@/components/atoms/button";

export function ThoughtMessage() {
  return (
    <div className="h-full bg-stone-850 border-1 rounded-lg">
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
            sometimes walking through tallinn feels like slipping between layers
            of time… cobblestones underfoot, old soviet blocks staring down at
            you, and the wind off the baltic that never really warms up, not
            even in july. it’s quiet here, even when it’s busy. like the city’s
            whispering something you’re not quite meant to hear. i drink coffee
            in cafés with names i can’t pronounce, watch the fog roll in over
            telliskivi rooftops, and wonder if i’m becoming someone new or just
            forgetting bits of who i was. the nights are long, or too short.
            depending on the season or maybe my mood. there’s this stillness
            here, like the city knows how to wait. maybe i'm learning that too.
            sometimes it’s lonely, but not the bad kind. just a space where your
            thoughts echo a little louder. like tallinn’s giving them room to
            stretch. strange comfort in that.
          </p>

          <div className="flex gap-2">
            <Button variant="ghost">Edit</Button>
            <Button variant="ghost">Delete</Button>
          </div>
        </div>
      </article>
    </div>
  );
}
