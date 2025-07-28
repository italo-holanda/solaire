import { LeftMenu } from "./components/templates/left-menu/left-menu";
import { RightMenu } from "./components/templates/right-menu/right-menu";
import { ThoughtHistory } from "./components/templates/thought-history/thought-history";

export default function App() {
  return (
    <div className="bg-black h-screen p-2">
      <div className="bg-stone-900 rounded-lg border-1 border-stone-800 flex h-full justify-between">
        <LeftMenu />
        <ThoughtHistory />
        <RightMenu />
      </div>
    </div>
  );
}
