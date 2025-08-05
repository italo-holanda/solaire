import { Button } from "@/components/atoms/button";
import { Textarea } from "@/components/atoms/textarea";
import { useUpdateThought } from "@/hooks/use-thoughts";
import { preventTextOverflow } from "@/utils/formatting";
import { SquarePenIcon } from "lucide-react";
import { useState } from "react";

type EditThoughtProps = {
  thoughtId: string;
  initialText: string;
  onClose: () => void;
};

export function EditThought(props: EditThoughtProps) {
  const [currentText, setCurrentText] = useState(props.initialText);

  const updateHook = useUpdateThought();

  const isLengthValid =
    currentText.trim().length > 100 && currentText.length < 900;

  const handleSubmit = async () => {
    if (!currentText.trim()) return;

    try {
      await updateHook.mutateAsync({
        text: currentText.trim(),
        thought_id: props.thoughtId,
      });
    } catch (error) {
      console.error("Failed to update thought:", error);
    } finally {
      props.onClose();
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (currentText.length < 100 || currentText.length > 1000) return;
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="flex flex-col gap-3 w-full">
      <Textarea
        onChange={(e) => setCurrentText(e.target.value)}
        onKeyDown={handleKeyDown}
        className="resize-none"
        value={currentText}
        disabled={updateHook.isPending}
        enterKeyHint="send"
      />

      <div className="flex items-center justify-between">
        <div className="text-xs">
          <span
            className={(() => {
              if (currentText.length > 100 && currentText.length < 900)
                return "text-green-400";
              if (currentText.length > 900 && currentText.length < 1000)
                return "text-amber-400";
              return "text-red-400";
            })()}
          >
            {currentText.length}
          </span>
          <span className="text-stone-400">/1000 chars</span>
        </div>

        <div className="flex gap-2">
          <Button onClick={props.onClose} variant="ghost" size="sm">
            Cancel
          </Button>
          <Button
            onClick={handleSubmit}
            disabled={!isLengthValid}
            variant={isLengthValid ? "default" : "ghost"}
            size="sm"
          >
            Update
          </Button>
        </div>
      </div>
    </div>
  );
}
