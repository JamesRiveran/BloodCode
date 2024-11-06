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
              <DropdownMenuItem onClick={() => handleOptionClick("nestedLoops")} className="hover:bg-secondary focus:bg-secondary">
                Bucles Anidados
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
              <DropdownMenuItem onClick={() => handleOptionClick("conditionalSyntax")} className="hover:bg-secondary focus:bg-secondary">
                Sintaxis Condicional Avanzada
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => handleOptionClick("switchCaseEmulation")} className="hover:bg-secondary focus:bg-secondary">
                Emulación Switch-Case
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
              <DropdownMenuItem onClick={() => handleOptionClick("stringConcatenation")} className="hover:bg-secondary focus:bg-secondary">
                Concatenación de Cadenas
              </DropdownMenuItem>
            </DropdownMenuSubContent>
          </DropdownMenuSub>

          <DropdownMenuSub>
            <DropdownMenuSubTrigger className="flex justify-between items-center w-full text-left px-4 py-2 hover:bg-secondary-dark focus:bg-secondary group">
              Operaciones Avanzadas
            </DropdownMenuSubTrigger>
            <DropdownMenuSubContent className="bg-color-gray-800 text-gray-100 border-gray-700">
              <DropdownMenuItem onClick={() => handleOptionClick("semantics")} className="hover:bg-secondary focus:bg-secondary">
                Semántica General
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => handleOptionClick("complexArithmetic")} className="hover:bg-secondary focus:bg-secondary">
                Aritmética Compleja
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => handleOptionClick("booleanExpressions")} className="hover:bg-secondary focus:bg-secondary">
                Expresiones Booleanas
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => handleOptionClick("arrayModification")} className="hover:bg-secondary focus:bg-secondary">
                Modificación de Array
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => handleOptionClick("recursiveFunction")} className="hover:bg-secondary focus:bg-secondary">
                Función Recursiva
              </DropdownMenuItem>
            </DropdownMenuSubContent>
          </DropdownMenuSub>
          <DropdownMenuSub>
            <DropdownMenuSubTrigger className="flex justify-between items-center w-full text-left px-4 py-2 hover:bg-secondary-dark focus:bg-secondary group">
              Algoritmos
            </DropdownMenuSubTrigger>
            <DropdownMenuSubContent className="bg-color-gray-800 text-gray-100 border-gray-700">
              <DropdownMenuItem onClick={() => handleOptionClick("areaRectangle")} className="hover:bg-secondary focus:bg-secondary">
                Área del Rectángulo
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => handleOptionClick("averageThreeNumbers")} className="hover:bg-secondary focus:bg-secondary">
                Promedio de Tres Números
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => handleOptionClick("celsiusToFahrenheit")} className="hover:bg-secondary focus:bg-secondary">
                Celsius a Fahrenheit
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => handleOptionClick("hoursToMinutesAndSeconds")} className="hover:bg-secondary focus:bg-secondary">
                Horas a Minutos y Segundos
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => handleOptionClick("ageInDays")} className="hover:bg-secondary focus:bg-secondary">
                Días Vividos
              </DropdownMenuItem>
            </DropdownMenuSubContent>
          </DropdownMenuSub>
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  );
};
