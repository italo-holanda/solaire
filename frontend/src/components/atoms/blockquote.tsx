type BlockquoteProps = {
  text: string;
};

export function Blockquote(props: BlockquoteProps) {
  return (
    <blockquote>
      <p className="text-sm p-1 px-2 border-1 rounded-sm cursor-pointer italic underline text-stone-300 hover:text-stone-200">"{props.text}"</p>
    </blockquote>
  );
}
