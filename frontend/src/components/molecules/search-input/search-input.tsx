import { Input } from "@/components/atoms/input";
import { SearchIcon } from "lucide-react";

export function SearchInput() {
  return (
    <div className="flex items-center">
      <div className="w-12 bg-stone-900 flex items-center justify-center border-1 border-r-0 rounded-l-md h-12">
        <SearchIcon size={20} color="#8C8C8C" />
      </div>
      <Input
        className="h-12 bg-stone-900 rounded-l-none"
        placeholder="Search"
      />
    </div>
  );
}
