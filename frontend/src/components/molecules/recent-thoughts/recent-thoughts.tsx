import { useThoughts } from "@/hooks/use-thoughts";

export function RecentThoughts() {
  const { data } = useThoughts();
  return (
    <ul className="flex flex-col gap-3">
      {data
        ?.filter((t) => !!t.title)
        ?.slice(0, 5)
        ?.map((thought) => (
          <li className="border-b text-sm italic text-stone-300" key={thought.id}>"{thought.title}"</li>
        ))}
    </ul>
  );
}
