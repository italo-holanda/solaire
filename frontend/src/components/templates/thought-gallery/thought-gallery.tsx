import { useThoughts } from "@/hooks/use-thoughts";

export function ThoughtGallery() {
  const { data } = useThoughts();

  return (
    <ul>
      {data?.map((thought) => (
        <li key={thought.id}>{thought.title}</li>
      ))}
    </ul>
  );
}
