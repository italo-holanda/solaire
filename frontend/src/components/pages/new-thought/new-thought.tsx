import { Separator } from "@/components/atoms/separator";
import { ThoughtInput } from "@/components/molecules/thought-input/thought-input";

export function NewThought() {
  return (
    <div className="p-2 w-full relative">
      <div className="font-medium p-4 h-20 flex items-center">
        Record a new thought
      </div>
      <Separator />

      <div className="p-4">
        <div className="h-full"></div>

        <div className="p-6 flex flex-col items-center gap-3 absolute bottom-0 left-0 w-full">
          <ThoughtInput />
          <span className="text-sm text-stone-500">
            Your thought will be automatically analyzed by Solaire.
          </span>
        </div>
      </div>
    </div>
  );
}
