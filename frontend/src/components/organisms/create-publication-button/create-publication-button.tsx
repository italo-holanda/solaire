import { Button } from "@/components/atoms/button";
import { SparklesIcon } from "lucide-react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/atoms/dialog";
import { useState } from "react";
import type { Publication } from "@/types";
import { CreatePublicationOutliningForm } from "./create-publication-outlining-form";
import { CreatePublicationFormatForm } from "./create-publication-format-form";
import { Spinner } from "@/components/atoms/spinner";
import { CreatePublicationContent } from "./create-publication-content";

export function CreatePublicationButton() {
  const [open, setOpen] = useState(false);

  const [publication, setPublication] = useState<Publication>();

  const [isLoading, setIsLoading] = useState(false);

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
        {(() => {
          if (isLoading)
            return (
              <div className="bg-stone-950 rounded-lg flex items-center justify-center py-4 gap-1 w-full">
                <Spinner size="sm" />
                <span className="text-sm text-stone-400">Loading...</span>
              </div>
            );

          if (!publication?.outlining)
            return (
              <CreatePublicationFormatForm
                {...{ publication, setPublication, setIsLoading }}
              />
            );

          if (!publication.content)
            return (
              <CreatePublicationOutliningForm
                {...{ publication, setPublication, setIsLoading }}
              />
            );

          return <CreatePublicationContent publication={publication} />;
        })()}
      </DialogContent>
    </Dialog>
  );
}
