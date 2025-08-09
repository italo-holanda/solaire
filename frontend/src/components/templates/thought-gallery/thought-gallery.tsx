import { Separator } from "@/components/atoms/separator";
import { GalleryCard } from "@/components/molecules/gallery-card/gallery-card";
import { useNavigation } from "@/hooks/use-navigation";
import { useThoughts } from "@/hooks/use-thoughts";

export function ThoughtGallery() {
  const { data } = useThoughts();
  const { params } = useNavigation();

  return (
    <main className="p-2 w-full relative h-full flex flex-col">
      <div className="font-medium p-4 h-20 flex items-center">
        Your recorded thoughts
      </div>
      <Separator />
      <div className="px-6 mx-auto flex flex-col flex-1 min-h-0 w-full">
        {params.searchTerms && (
          <div className="shadow-xl p-1 px-3 border rounded-xl mt-4 text-sm text-stone-300">
            Results for "{params.searchTerms}"
          </div>
        )}

        <ul className="flex flex-wrap justify-center gap-3 overflow-y-scroll">
          <div className="w-full mt-6" />
          {data?.map((thought) => (
            <li className="max-w-70" key={thought.id}>
              <GalleryCard {...thought} />
            </li>
          ))}
          <div className="w-full mt-6" />
        </ul>
      </div>
    </main>
  );
}
