import { Button } from "@/components/atoms/button";
import { CategoryBadge } from "@/components/molecules/category-badge/category-badge";
import { Blockquote } from "@/components/atoms/blockquote";
import { ChevronDownIcon } from "lucide-react";
import { useState } from "react";
import type { Thought } from "@/types";
import { useRelatedThoughts } from "@/hooks/use-related-thoughts";

/**
 *
 * Breaks the text line every 25 chars if no white-space
 * found
 */
function preventTextOverflow(text: string) {
  const words = text.split(" ");
  const result: string[] = [];
  let currentLine = "";

  for (const word of words) {
    if (currentLine.length + word.length <= 25) {
      currentLine += (currentLine ? " " : "") + word;
    } else {
      if (currentLine) {
        result.push(currentLine);
      }
      if (word.length > 25) {
        for (let i = 0; i < word.length; i += 25) {
          result.push(word.slice(i, i + 25));
        }
        currentLine = "";
      } else {
        currentLine = word;
      }
    }
  }

  if (currentLine) {
    result.push(currentLine);
  }

  return result.join("\n");
}

export function ThoughtMessage(props: Thought) {
  const [isExpanded, setIsExpanded] = useState(false);

  const relateds = useRelatedThoughts({
    thoughtId: isExpanded ? props.id : undefined,
  });

  return (
    <>
      <div className="bg-stone-850 border-1 rounded-lg">
        <article className="p-6 flex gap-3">
          <figure className="flex flex-col items-center gap-2 w-10">
            <img
              className="bg-amber-400 rounded-full"
              width={32}
              src="/user.svg"
              alt="user"
            />
            <legend className="text-xs text-stone-500">
              <span>
                {props.created_at.toLocaleDateString("en-US", {
                  month: "short",
                })}
              </span>
              ,<span>{props.created_at.getDay()}</span>
            </legend>
          </figure>

          <div className="flex flex-col gap-2">
            <p className="text-base/6.5 text-stone-200 break-words">
              {preventTextOverflow(props.text)}
            </p>

            <div className="flex justify-between">
              <div className="flex gap-2">
                <Button variant="ghost">Edit</Button>
                <Button variant="ghost">Delete</Button>
              </div>

              <Button
                onClick={() => setIsExpanded((p) => !p)}
                variant={isExpanded ? "outline" : "ghost"}
              >
                <ChevronDownIcon />
              </Button>
            </div>
          </div>
        </article>
      </div>

      {isExpanded && (
        <div className="bg-stone-950 border-1 border-t-transparent rounded-b-lg">
          <article className="p-6 flex gap-3">
            <figure className="flex flex-col items-center gap-2 min-w-10">
              <img width={32} src="/solaire-ico.svg" alt="user" />
            </figure>

            <div className="flex flex-col gap-2">
              <h1>{props.title}</h1>

              <p className="text-stone-300">{props.summary}</p>

              <div className="flex flex-col gap-1">
                <h2 className="text-sm text-stone-400">Categories</h2>
                <ul className="flex flex-wrap gap-1">
                  {props.categories.map((category) => (
                    <CategoryBadge
                      color={category.color ?? "green"}
                      name={category.name}
                    />
                  ))}
                </ul>
              </div>

              <div className="flex flex-col gap-2">
                <h2 className="text-sm text-stone-400">Related to</h2>
                <ul className="flex flex-wrap gap-2">
                  {relateds.data?.map((related) => (
                    <li key={related.id}>
                      <Blockquote text={related.title} />
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </article>
        </div>
      )}
    </>
  );
}
