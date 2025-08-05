import { useState } from "react";
import { Textarea } from "@/components/atoms/textarea";
import { useCreateThought, useThoughts } from "@/hooks/use-thoughts";

export function ThoughtInput() {
  const [text, setText] = useState("");
  const createThought = useCreateThought();
  const { refetch } = useThoughts();

  const handleSubmit = async () => {
    if (!text.trim()) return;

    try {
      await createThought.mutateAsync({ text: text.trim() });
      refetch();
    } catch (error) {
      console.error("Failed to create thought:", error);
    } finally {
      setText("");
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (text.length < 100 || text.length > 1000) return;
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="w-full flex flex-col gap-1">
      <Textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Register your thought..."
        className="p-6 h-40 bg-stone-900 shadow-lg rounded-xl resize-none"
        disabled={createThought.isPending}
        enterKeyHint="send"
      />
      <div className="flex justify-between text-xs p-2 px-4 bg-stone-950 border-1 border-border rounded-2xl">
        <span className="text-stone-500">Size of your thought</span>

        <div>
          <span
            className={(() => {
              if (text.length > 100 && text.length < 900)
                return "text-green-400";
              if (text.length > 900 && text.length < 1000)
                return "text-amber-400";
              return "text-red-400";
            })()}
          >
            {text.length}
          </span>
          <span className="text-stone-400">/1000 chars</span>
        </div>
      </div>
    </div>
  );
}
