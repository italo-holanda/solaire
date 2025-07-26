import { LeftMenu } from "./components/templates/left-menu/left-menu";
import { RightMenu } from "./components/templates/right-menu/right-menu";
import { ThoughtHistory } from "./components/templates/thought-history/thought-history";

export default function App() {
  return (
    <div className="bg-stone-900 h-screen">
      <div className="flex h-full justify-between">
        <LeftMenu />
        <ThoughtHistory />
        <RightMenu />
      </div>
    </div>
  );
}
