import type { Publication } from "@/types";

import { Button } from "@/components/atoms/button";
import { Separator } from "@/components/atoms/separator";
import {
  CheckIcon,
  EditIcon,
  PlusIcon,
  TrashIcon,
  GripVerticalIcon,
} from "lucide-react";
import { Fragment, useState, useRef } from "react";
import { Textarea } from "@/components/atoms/textarea";
import { createPublicationContent } from "@/services/api/publications/publications";

function OutliningItem(props: {
  index: number;
  text: string;
  setText: (text: string) => void;
  deleteText: () => void;
  onDragStart: (e: React.DragEvent, index: number) => void;
  onDragOver: (e: React.DragEvent) => void;
  onDrop: (e: React.DragEvent, index: number) => void;
}) {
  const [isEditable, setIsEditable] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      const newText = textareaRef.current?.value || props.text;
      props.setText(newText);
      setIsEditable(false);
    }
  };

  const handleSave = () => {
    const newText = textareaRef.current?.value || props.text;
    props.setText(newText);
    setIsEditable(false);
  };

  return (
    <li
      className="flex flex-col justify-between gap-2 p-4 bg-stone-850 border-1 rounded-lg text-sm text-stone-200 cursor-move hover:bg-stone-900 transition-colors"
      draggable
      onDragStart={(e) => props.onDragStart(e, props.index)}
      onDragOver={props.onDragOver}
      onDrop={(e) => props.onDrop(e, props.index)}
    >
      <span className="flex justify-between items-center">
        <span className="flex items-center gap-2">
          <GripVerticalIcon className="w-4 h-4 text-stone-500" />
          <span className="text-stone-400">Block {props.index + 1}</span>
        </span>
        <div>
          <Button
            className="edit-button"
            disabled={isEditable}
            onClick={() => setIsEditable(true)}
            size="sm"
            variant="ghost"
          >
            Edit
            <EditIcon />
          </Button>
          <Button
            disabled={isEditable}
            onClick={props.deleteText}
            size="sm"
            variant="ghost"
          >
            Delete
            <TrashIcon />
          </Button>
        </div>
      </span>
      <Separator />

      {!isEditable && <span className="italic text-base">"{props.text}"</span>}

      {isEditable && (
        <div className="flex flex-col gap-2">
          <Textarea
            maxLength={200}
            ref={textareaRef}
            className="italic text-base"
            defaultValue={props.text}
            onKeyDown={handleKeyDown}
          />
          <div className="flex gap-2">
            <Button onClick={handleSave} size="sm" variant="secondary">
              Save
            </Button>
            <Button
              onClick={() => setIsEditable(false)}
              size="sm"
              variant="ghost"
            >
              Cancel
            </Button>
          </div>
        </div>
      )}
    </li>
  );
}

export function CreatePublicationOutliningForm(props: {
  publication: Publication;
  setPublication: (pub: Publication) => void;
  setIsLoading: (isLoading: boolean) => void;
  onCancel: () => void;
}) {
  const [outlining, setOutlining] = useState(props.publication.outlining);
  const [draggedIndex, setDraggedIndex] = useState<number | null>(null);
  const scrollContainerRef = useRef<HTMLUListElement>(null);

  const handleDragStart = (e: React.DragEvent, index: number) => {
    setDraggedIndex(index);
    e.dataTransfer.effectAllowed = "move";
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = "move";
  };

  const handleDrop = (e: React.DragEvent, dropIndex: number) => {
    e.preventDefault();

    if (draggedIndex === null || draggedIndex === dropIndex) {
      return;
    }

    const newOutlining = Array.from(outlining);
    const draggedItem = newOutlining[draggedIndex];

    newOutlining.splice(draggedIndex, 1);
    newOutlining.splice(dropIndex, 0, draggedItem);

    setOutlining(newOutlining);
    setDraggedIndex(null);
  };

  const handleAddNewBlock = () => {
    const newIndex = outlining.length;
    setOutlining(outlining.concat(""));

    setTimeout(() => {
      if (scrollContainerRef.current) {
        const newBlockElement = scrollContainerRef.current.children[newIndex];
        if (newBlockElement) {
          // Open in edit mode
          const editButton = newBlockElement.querySelector(
            ".edit-button"
          ) as HTMLButtonElement;
          if (editButton) {
            editButton.click();
          }
        }

        setTimeout(() => {
          // Focus on text-area input
          const textArea = newBlockElement.querySelector("textarea");
          textArea?.focus();
          textArea?.scrollIntoView({ behavior: "smooth" });
        }, 100);
      }
    }, 100);
  };

  return (
    <form onSubmit={(ev) => ev.preventDefault()}>
      <Separator className="my-2" />

      <fieldset className="flex flex-col gap-2">
        <label className="text-stone-200 mt-3">Summarize your content</label>
        <p className="text-xs text-stone-300">
          Add, remove, and edit the blocks to refine the flow of your final
          text. Drag and drop to reorder blocks.
        </p>
        <div className="flex flex-col gap-1">
          <ul
            ref={scrollContainerRef}
            className="mt-1 flex flex-col gap-2 max-h-80 overflow-y-scroll border-1 bg-stone-950 p-2 pl-4 rounded-md"
          >
            {outlining.map((text, i) => (
              <Fragment key={text}>
                <OutliningItem
                  index={i}
                  text={text}
                  setText={(text: string) => {
                    const newArr = Array.from([...outlining]);
                    newArr[i] = text;
                    setOutlining(newArr);
                  }}
                  deleteText={() => {
                    const newArr = Array.from([...outlining]);
                    newArr.splice(i, 1);
                    setOutlining(newArr);
                  }}
                  onDragStart={handleDragStart}
                  onDragOver={handleDragOver}
                  onDrop={handleDrop}
                />
              </Fragment>
            ))}
          </ul>
          <Button onClick={handleAddNewBlock} variant="secondary" size="sm">
            Add new block <PlusIcon />
          </Button>
        </div>
      </fieldset>
      <Separator className="my-2 mt-6" />

      <div className="flex justify-between items-center">
        <Button onClick={props.onCancel} size="sm" variant="ghost">
          Cancel
        </Button>
        <Button
          onClick={async () => {
            try {
              props.setIsLoading(true);
              const updatedPublication = await createPublicationContent({
                publication_id: props.publication.id,
                publication_outlining: outlining,
              });
              props.setPublication(updatedPublication);
            } catch (error) {
              console.error("Error creating publication content:", error);
            } finally {
              props.setIsLoading(false);
            }
          }}
          size="sm"
        >
          Finish
          <CheckIcon />
        </Button>
      </div>
    </form>
  );
}
