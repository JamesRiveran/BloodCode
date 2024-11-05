import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSub,
  DropdownMenuSubTrigger,
  DropdownMenuSubContent,
} from "@/components/ui/dropdown-menu";
import type { CodeOptions } from "./CodeGenerator";
import React from "react";

interface CodeOptionsProps {
  handleOptionChange: (option: CodeOptions) => void;
}

export const CodeOptionsComponent: React.FC<CodeOptionsProps> = ({
  handleOptionChange,
}) => {
  const handleOptionClick = (value: CodeOptions) => {
    handleOptionChange(value);
  };

  return (
    <div className="flex items-center gap-4 px-4 py-2">
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button variant="outline" className="w-full">
            Opciones de Código
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent className="bg-color-gray-800 border border-gray-700 text-gray-100 w-56 mt-2">
          <DropdownMenuSub>
            <DropdownMenuSubTrigger className="flex justify-between items-center w-full text-left px-4 py-2 hover:bg-secondary-dark focus:bg-secondary group">
              Bucles
            </DropdownMenuSubTrigger>
            <DropdownMenuSubContent className="bg-color-gray-800 text-gray-100 border-gray-700">
              <DropdownMenuItem onClick={() => handleOptionClick("whileSyntax")} className="hover:bg-secondary focus:bg-secondary">
                Ciclo While
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => handleOptionClick("forSyntax")} className="hover:bg-secondary focus:bg-secondary">
                Ciclo For
              </DropdownMenuItem>
            </DropdownMenuSubContent>
          </DropdownMenuSub>

          <DropdownMenuSub>
            <DropdownMenuSubTrigger className="flex justify-between items-center w-full text-left px-4 py-2 hover:bg-secondary-dark focus:bg-secondary group">
              Sintaxis
            </DropdownMenuSubTrigger>
            <DropdownMenuSubContent className="bg-color-gray-800 text-gray-100 border-gray-700">
              <DropdownMenuItem onClick={() => handleOptionClick("controlSyntax")} className="hover:bg-secondary focus:bg-secondary">
                Condicional
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => handleOptionClick("functionSyntax")} className="hover:bg-secondary focus:bg-secondary">
                Funciones
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => handleOptionClick("operationSyntax")} className="hover:bg-secondary focus:bg-secondary">
                Operaciones
              </DropdownMenuItem>
            </DropdownMenuSubContent>
          </DropdownMenuSub>

          <DropdownMenuSub>
            <DropdownMenuSubTrigger className="flex justify-between items-center w-full text-left px-4 py-2 hover:bg-secondary-dark focus:bg-secondary group">
              Semántica
            </DropdownMenuSubTrigger>
            <DropdownMenuSubContent className="bg-color-gray-800 text-gray-100 border-gray-700">
              <DropdownMenuItem onClick={() => handleOptionClick("semantics")} className="hover:bg-secondary focus:bg-secondary">
                Semántica General
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => handleOptionClick("pemdas")} className="hover:bg-secondary focus:bg-secondary">
                PEMDAS
              </DropdownMenuItem>
            </DropdownMenuSubContent>
          </DropdownMenuSub>

          <DropdownMenuSub>
            <DropdownMenuSubTrigger className="flex justify-between items-center w-full text-left px-4 py-2 hover:bg-secondary-dark focus:bg-secondary group">
              Tipos de Datos
            </DropdownMenuSubTrigger>
            <DropdownMenuSubContent className="bg-color-gray-800 text-gray-100 border-gray-700">
              <DropdownMenuItem onClick={() => handleOptionClick("dataTypes")} className="hover:bg-secondary focus:bg-secondary">
                Tipos Simples
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => handleOptionClick("vectorsSyntax")} className="hover:bg-secondary focus:bg-secondary">
                Vectores
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => handleOptionClick("arraysSyntax")} className="hover:bg-secondary focus:bg-secondary">
                Matrices
              </DropdownMenuItem>
            </DropdownMenuSubContent>
          </DropdownMenuSub>

          <DropdownMenuSub>
            <DropdownMenuSubTrigger className="flex justify-between items-center w-full text-left px-4 py-2 hover:bg-secondary-dark focus:bg-secondary group">
              Entrada/Salida
            </DropdownMenuSubTrigger>
            <DropdownMenuSubContent className="bg-color-gray-800 text-gray-100 border-gray-700">
              <DropdownMenuItem onClick={() => handleOptionClick("dataEntry")} className="hover:bg-secondary focus:bg-secondary">
                Entrada de Datos
              </DropdownMenuItem>
            </DropdownMenuSubContent>
          </DropdownMenuSub>
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  );
};
