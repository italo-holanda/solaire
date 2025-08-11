import { Button } from "@/components/atoms/button";
import {
  ArrowRight,
  EditIcon,
  LinkedinIcon,
  PlusIcon,
  SparklesIcon,
  TextIcon,
  TrashIcon,
  VideoIcon,
} from "lucide-react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/atoms/dialog";
import { useState } from "react";
import { Textarea } from "@/components/atoms/textarea";
import { Separator } from "@/components/atoms/separator";
import type { Publication, PublicationFormat } from "@/types";
import { createPublicationPreview } from "@/services/api";
import { useGallery } from "@/hooks/use-gallery";

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

function Step1(props: {
  publication?: Publication;
  setPublication: (pub: Publication) => void;
}) {
  const { selectedThoughts } = useGallery();

  const [selectedFormat, setSelectedFormat] =
    useState<PublicationFormat>("blog_post");

  const [guideline, setGuideline] = useState("");

  async function onSubmit() {
    const publication = await createPublicationPreview({
      publication_format: selectedFormat,
      selected_thought_ids: selectedThoughts.map((t) => t.id),
      user_guideline: guideline,
    });
    props.setPublication(publication);
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
        <Button size="sm" variant="ghost">
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

function Step2(props: {
  publication: Publication;
  setPublication: (pub: Publication) => void;
}) {
  return (
    <form onSubmit={(ev) => ev.preventDefault()}>
      <Separator className="my-2" />

      <fieldset className="flex flex-col gap-2">
        <label className="text-stone-200 mt-3">Summarize your content</label>
        <p className="text-xs text-stone-300">
          Add, remove, and edit the blocks to refine the flow of your final
          text.
        </p>
        <div className="flex flex-col gap-1">
          <ul className="mt-1 flex flex-col gap-2 max-h-80 overflow-y-scroll border-1 bg-stone-950 p-2 pl-4 rounded-md">
            {props.publication.outlining.map((o, i) => (
              <li
                className="flex flex-col justify-between gap-2 p-4 bg-stone-850 border-1 rounded-lg text-sm text-stone-200"
                key={o}
              >
                <span className="flex justify-between items-center">
                  <span className="text-stone-400">Block {i + 1}</span>
                  <div>
                    <Button size="sm" variant="ghost">
                      Edit
                      <EditIcon />
                    </Button>
                    <Button size="sm" variant="ghost">
                      Delete
                      <TrashIcon />
                    </Button>
                  </div>
                </span>
                <Separator />
                <span className="italic text-base">"{o}"</span>
              </li>
            ))}
          </ul>
          <Button variant="secondary" size="sm">
            Add new <PlusIcon />
          </Button>
        </div>
      </fieldset>
      <Separator className="my-2 mt-6" />
    </form>
  );
}

export function CreatePublicationButton() {
  const [open, setOpen] = useState(false);

  const [publication, setPublication] = useState<Publication>();

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button>
          New publication
          <SparklesIcon />
        </Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Creating your publication</DialogTitle>
        </DialogHeader>
        {!publication?.outlining && (
          <Step1 {...{ publication, setPublication }} />
        )}
        {publication?.outlining && (
          <Step2 {...{ publication, setPublication }} />
        )}
      </DialogContent>
    </Dialog>
  );
}
