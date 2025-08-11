import { Separator } from "@/components/atoms/separator";
import { CreatePublicationButton } from "@/components/organisms/create-publication-button/create-publication-button";
import { GalleryCard } from "@/components/molecules/gallery-card/gallery-card";
import { useGallery } from "@/hooks/use-gallery";
import { useThoughts } from "@/hooks/use-thoughts";

export function ThoughtGallery() {
  const { data } = useThoughts();
  const { selectedThoughts } = useGallery();

  return (
    <main className="p-2 w-full relative h-full flex flex-col">
      <div className="font-medium p-4 h-20 flex items-center">
        Your recorded thoughts
      </div>
      <Separator />
      <div className="px-6 mx-auto flex flex-col flex-1 min-h-0 w-full">
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

      {!!selectedThoughts.length && (
        <div className="shadow-2xl p-3 border-1 bg-stone-950 rounded-lg flex items-center justify-between">
          <span className="text-sm text-stone-200">{selectedThoughts.length} thoughts selected</span>
          <CreatePublicationButton />
        </div>
      )}
    </main>
  );
}
