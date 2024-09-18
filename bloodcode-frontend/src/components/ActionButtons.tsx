import { Button } from "@/components/ui/button";

interface ActionButtonsProps {
  compile: () => void;
  execute: () => void;
}

export const ActionButtons: React.FC<ActionButtonsProps> = ({ compile, execute }) => {
  return (
    <div className="flex flex-col sm:flex-row gap-2 w-full">
        <Button onClick={compile} className="bg-red-700 hover:bg-red-800 text-white w-full sm:w-auto">
            Compilar
        </Button>
        <Button onClick={execute} className="bg-red-900 hover:bg-red-950 text-white w-full sm:w-auto">
            Ejecutar
        </Button>
    </div>

  );
};
