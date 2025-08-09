import { LeftMenu } from "./components/templates/left-menu/left-menu";
import { RightMenu } from "./components/templates/right-menu/right-menu";
import { ThoughtGallery } from "./components/templates/thought-gallery/thought-gallery";
import { ThoughtHistory } from "./components/templates/thought-history/thought-history";
import { useNavigation } from "./hooks/use-navigation";

export default function App() {
  const { currentView } = useNavigation();

  return (
    <div className="bg-black h-screen p-2">
      <div className="bg-stone-900 rounded-lg border-1 border-stone-800 flex h-full justify-between">
        <LeftMenu />
        {(() => {
          if (currentView === "gallery") return <ThoughtGallery />;
          if (currentView === "history") return <ThoughtHistory />;
        })()}
        <RightMenu />
      </div>
    </div>
  );
}
