import type { Publication, PublicationFormat } from "@/types";

import { Separator } from "@/components/atoms/separator";
import { useGallery } from "@/hooks/use-gallery";
import { createPublicationPreview } from "@/services/api";
import { useState } from "react";
import { ArrowRight, LinkedinIcon, TextIcon, VideoIcon } from "lucide-react";
import { Textarea } from "@/components/atoms/textarea";
import { Button } from "@/components/atoms/button";

const FORMATS = [
  {
    name: "Blog post",
    icon: TextIcon,
    id: "blog_post" as PublicationFormat,
  },
  {
    name: "LinkedIn post",
    icon: LinkedinIcon,
    id: "linkedin_post" as PublicationFormat,
  },
  {
    name: "Long video",
    icon: VideoIcon,
    id: "long_video" as PublicationFormat,
  },
  {
    name: "Short video",
    icon: VideoIcon,
    id: "short_video" as PublicationFormat,
  },
];

export function CreatePublicationFormatForm(props: {
  publication?: Publication;
  setPublication: (pub: Publication) => void;
  setIsLoading: (isLoading: boolean) => void;
  onCancel: () => void;
}) {
  const { selectedThoughts } = useGallery();

  const [selectedFormat, setSelectedFormat] =
    useState<PublicationFormat>("blog_post");

  const [guideline, setGuideline] = useState("");

  async function onSubmit() {
    try {
      props.setIsLoading(true);
      const publication = await createPublicationPreview({
        publication_format: selectedFormat,
        selected_thought_ids: selectedThoughts.map((t) => t.id),
        user_guideline: guideline,
      });
      props.setPublication(publication);
    } catch {
      // @TODO
    } finally {
      props.setIsLoading(false);
    }
  }

  return (
    <form
      className="flex flex-col gap-5"
      onSubmit={(ev) => ev.preventDefault()}
    >
      <Separator className="my-2" />

      <fieldset className="flex flex-col gap-2">
        <label className="text-stone-300">Choose your publication format</label>
        <ul className="flex justify-center gap-3">
          {FORMATS.map((Format) => (
            <li
              key={Format.id}
              role="button"
              onClick={() => setSelectedFormat(Format.id)}
              className={`bg-stone-850 cursor-pointer w-25 h-20 border-1 rounded-lg flex flex-col items-center justify-center gap-2 text-stone-300 ${
                selectedFormat === Format.id
                  ? "border-amber-600"
                  : "hover:bg-stone-900"
              }`}
            >
              <div className="text-xs p-2 bg-stone-950 rounded-md">
                <Format.icon size={16} />
              </div>
              <span className="text-xs text-center">{Format.name}</span>
            </li>
          ))}
        </ul>
      </fieldset>

      <fieldset className="flex flex-col gap-2">
        <label className="text-stone-300">
          Determine the style of your publication
        </label>
        <Textarea
          value={guideline}
          onChange={(ev) => setGuideline(ev.target.value)}
          maxLength={1000}
          placeholder="My publication should have an informal and relaxed tone of voice. It should relate Solaire's story to the life of an ordinary professional in the context of today's world."
          className="h-30 resize-none"
        />
      </fieldset>

      <Separator />

      <div className="flex justify-between items-center">
        <Button onClick={props.onCancel} size="sm" variant="ghost">
          Cancel
        </Button>
        <Button onClick={onSubmit} size="sm">
          Next
          <ArrowRight />
        </Button>
      </div>
    </form>
  );
}
