import React from "react";
import { Select, SelectTrigger, SelectContent, SelectItem, SelectValue } from "@/components/ui/select";
import type { CodeOptions } from "./CodeGenerator"; 

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
      <span className="text-sm font-medium">Menú de opciones:</span>
        <Select onValueChange={handleValueChange} value={selectedOption}>
        <SelectTrigger className="w-full sm:w-48 bg-gray-700 text-gray-100 border-gray-600">
            <SelectValue placeholder="Opciones" />
        </SelectTrigger>

        <SelectContent className="bg-gray-700 text-gray-100 border-gray-600">
          <SelectItem value="reservedWords">Palabras reservadas</SelectItem>
          <SelectItem value="controlSyntax">Sintaxis - Control</SelectItem>
          <SelectItem value="functionSyntax">Sintaxis - Funciones</SelectItem>
          <SelectItem value="operationSyntax">Sintaxis - Operaciones</SelectItem>
          <SelectItem value="semantics">Semántica</SelectItem>
          <SelectItem value="dataTypes">Tipos de datos</SelectItem>
        </SelectContent>
      </Select>
    </div>
  );
};
