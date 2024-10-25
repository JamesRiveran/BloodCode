import { Select, SelectTrigger, SelectContent, SelectItem, SelectValue } from "@/components/ui/select";
import type { CodeOptions } from "./CodeGenerator";
import React from "react";

interface CodeOptionsProps {
  selectedOption: CodeOptions | "";
  setSelectedOption: React.Dispatch<React.SetStateAction<CodeOptions | "">>;
}

export const CodeOptionsComponent: React.FC<CodeOptionsProps> = ({ selectedOption, setSelectedOption }) => {
  const handleValueChange = (value: CodeOptions) => {
    setSelectedOption(value);
  };

  return (
    <div className="flex items-center gap-2">
      <span className="text-sm font-medium text-color-gray-600">Menú de opciones:</span>
      <Select onValueChange={handleValueChange} value={selectedOption}>
        <SelectTrigger className="w-full sm:w-48 bg-color-gray-800 text-gray-100 border-gray-700 hover:bg-primary focus:outline-none">
          <SelectValue placeholder="Opciones" />
        </SelectTrigger>
        <SelectContent className="bg-color-gray-800 text-gray-100 border-gray-700">
          <SelectItem className="hover:bg-primary" value="reservedWords">Palabras reservadas</SelectItem>
          <SelectItem className="hover:bg-primary" value="controlSyntax">Sintaxis - Control</SelectItem>
          <SelectItem className="hover:bg-primary" value="functionSyntax">Sintaxis - Funciones</SelectItem>
          <SelectItem className="hover:bg-primary" value="operationSyntax">Sintaxis - Operaciones</SelectItem>
          <SelectItem className="hover:bg-primary" value="semantics">Semántica</SelectItem>
          <SelectItem className="hover:bg-primary" value="dataTypes">Tipos de datos</SelectItem>
          <SelectItem className="hover:bg-primary" value="vectors">Vectores</SelectItem>
        </SelectContent>
      </Select>
    </div>
  );
};
