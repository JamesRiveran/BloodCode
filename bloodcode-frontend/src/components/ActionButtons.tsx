import { Select, SelectTrigger, SelectContent, SelectItem, SelectValue } from "@/components/ui/select";
import { Button } from "@/components/ui/button";
import { useState } from "react";

interface ActionButtonsProps {
  compile: (option: string) => void;
  execute: () => void;
}

export const ActionButtons: React.FC<ActionButtonsProps> = ({ compile, execute }) => {
  const [selectedCompileOption, setSelectedCompileOption] = useState("Compilar");

  const handleCompileOptionChange = (value: string) => {
    setSelectedCompileOption(value);
    compile(value); 
  };

  return (
    <div className="flex flex-col sm:flex-row gap-2 w-full">
      <div className="w-full sm:w-auto">
        <Select onValueChange={handleCompileOptionChange}>
          <SelectTrigger className="w-full bg-red-900 text-white hover:bg-red-800">
            <SelectValue placeholder={selectedCompileOption || "Compilar"} />
          </SelectTrigger>
          <SelectContent className="bg-gray-700 text-white">
            <SelectItem className="hover:bg-red-800" value="tokens">Lista de tokens</SelectItem>
            <SelectItem className="hover:bg-red-800" value="ast">Árbol AST</SelectItem>
            <SelectItem className="hover:bg-red-800" value="compile">Compilar</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <Button
        onClick={execute}
        className="bg-red-900 hover:bg-red-950 text-white w-full sm:w-auto"
      >
        Ejecutar
      </Button>
    </div>
  );
};
