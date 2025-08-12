import { Button } from "@/components/atoms/button";
import { Separator } from "@/components/atoms/separator";
import { Textarea } from "@/components/atoms/textarea";
import type { Publication } from "@/types";
import { DownloadIcon } from "lucide-react";

export function CreatePublicationContent(props: {
  publication: Publication;
  onCancel: () => void;
}) {
  const handleDownload = () => {
    const content = props.publication.content;
    const title = props.publication.title || "publication";
    const filename = `${title.replace(/[^a-z0-9]/gi, "-").toLowerCase()}.md`;

    const blob = new Blob([content], { type: "text/markdown" });
    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="flex flex-col gap-3">
      <Separator />

      <div className="flex flex-col gap-1">
        <label className="text-stone-200">
          Your content has been generated
        </label>
        <p className="text-sm text-stone-300">
          You can download the Markdown file and publish it on your website.
        </p>
      </div>
      <Textarea
        className="h-70 resize-none"
        value={props.publication.content}
        readOnly
      />

      <Separator />

      <div className="flex justify-between items-center">
        <Button onClick={props.onCancel} size="sm" variant="ghost">
          Cancel
        </Button>
        <Button onClick={handleDownload} size="sm">
          Download .MD file
          <DownloadIcon />
        </Button>
      </div>
    </div>
  );
}
