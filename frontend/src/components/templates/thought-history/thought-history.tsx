import { Separator } from "@/components/atoms/separator";
import { ThoughtInput } from "@/components/molecules/thought-input/thought-input";
import { ThoughtMessage } from "@/components/organisms/thought-message/thought-message";

export function ThoughtHistory() {
  return (
    <main className="p-2 w-full relative h-full flex flex-col">
      <div className="font-medium p-4 h-20 flex items-center">
        Record a new thought
      </div>
      <Separator />

      <div className="max-w-2xl px-6 mx-auto flex flex-col flex-1 min-h-0">
        <div className="pl-4 flex-1 min-h-0 flex flex-col overflow-scroll">
          {/* Creates a top gap  */}
          <div className="min-h-8 w-full">
            <span className="text-transparent">...</span>
          </div>

          <ThoughtMessage />

          {/* Creates a botton gap  */}
          <div className="min-h-55 w-full">
            <span className="text-transparent">...</span>
          </div>
        </div>

        <div className="absolute bottom-0 left-0 w-full">
          <div className="mx-auto flex flex-col items-center gap-3 w-2xl p-6">
            <ThoughtInput />
            <span className="text-sm text-stone-500">
              Your thought will be automatically analyzed by Solaire.
            </span>
          </div>
        </div>
      </div>
    </main>
  );
}
