import React, { useState } from "react";
import { Select, SelectTrigger, SelectContent, SelectItem, SelectValue } from "@/components/ui/select";
import { Button } from "@/components/ui/button";

interface ActionButtonsProps {
  compile: (option: string) => void;
  execute: (userInput?: string) => void;
}

export const ActionButtons: React.FC<ActionButtonsProps> = ({ compile, execute }) => {
  const [selectedCompileOption, setSelectedCompileOption] = useState("Compilar");
  const [userInput, setUserInput] = useState("");
  const [isPromptActive, setIsPromptActive] = useState(false);

  const handleCompileOptionChange = (value: string) => {
    setSelectedCompileOption(value);
    compile(value);
  };

  const handleUserInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setUserInput(e.target.value);
  };

  const handleUserInputSubmit = async () => {
    if (userInput) {
      await execute(userInput);
      setIsPromptActive(false);
    }
  };

  return (
    <div className="flex flex-col sm:flex-row gap-2 w-full">
      <div className="w-full sm:w-auto">
        <Select onValueChange={handleCompileOptionChange}>
          <SelectTrigger className="w-full bg-color-gray-800 text-gray-100 border-gray-700 hover:bg-primary focus:outline-none">
            <SelectValue placeholder={selectedCompileOption || "Compilar"} />
          </SelectTrigger>
          <SelectContent className="bg-color-gray-800 text-gray-100 border-gray-700">
            <SelectItem className="hover:bg-primary" value="tokens">Lista de tokens</SelectItem>
            <SelectItem className="hover:bg-primary" value="ast">Árbol AST</SelectItem>
            <SelectItem className="hover:bg-primary" value="compile">Compilar</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <Button
        onClick={() => execute()}
        className="bg-buttonColor hover:bg-primary text-gray-100 w-full sm:w-auto"
      >
        Ejecutar
      </Button>

      {isPromptActive && (
        <div className="flex flex-col mt-2 w-full sm:w-auto">
          <input
            type="text"
            value={userInput}
            onChange={handleUserInputChange}
            className="bg-color-gray-800 text-gray-100 border-gray-700 p-2"
            placeholder="Ingrese el dato requerido..."
          />
          <Button onClick={handleUserInputSubmit} className="mt-2 bg-buttonColor hover:bg-primary">
            Enviar
          </Button>
        </div>
      )}
    </div>
  );
};
