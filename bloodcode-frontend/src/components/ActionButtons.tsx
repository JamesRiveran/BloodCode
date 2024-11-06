import React, { useState } from "react";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
} from "@/components/ui/dropdown-menu";

interface ActionButtonsProps {
  compile: (option: string) => void;
  execute: (userInput?: string) => void;
}

export const ActionButtons: React.FC<ActionButtonsProps> = ({ compile, execute }) => {
  const [userInput, setUserInput] = useState("");
  const [isPromptActive, setIsPromptActive] = useState(false);

  const handleCompileOptionChange = (value: string) => {
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
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="outline" className="w-full">
              Opciones de compilación
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent className="bg-color-gray-800 text-gray-100 border-gray-700">
            <DropdownMenuItem onClick={() => handleCompileOptionChange("tokens")} className="hover:bg-secondary">
              Lista de tokens
            </DropdownMenuItem>
            <DropdownMenuItem onClick={() => handleCompileOptionChange("ast")} className="hover:bg-secondary">
              Árbol AST
            </DropdownMenuItem>
            <DropdownMenuItem onClick={() => handleCompileOptionChange("compile")} className="hover:bg-secondary">
              Compilar
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
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
