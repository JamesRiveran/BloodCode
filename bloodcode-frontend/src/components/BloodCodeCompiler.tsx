"use client";
import React, { useEffect, useState } from "react";
import { CodeEditor } from "./CodeEditor";
import { OutputDisplay } from "./OutputDisplay";
import { ActionButtons } from "./ActionButtons";
import { CodeOptionsComponent } from "./CodeOptions"; 
import { CodeOptions, codeTemplates } from "./CodeGenerator";

export default function BloodCodeCompiler() {
  const [code, setCode] = useState("");  
  const [output, setOutput] = useState("");
  const [isError, setIsError] = useState(false); 
  const [selectedOption, setSelectedOption] = useState<CodeOptions | "">("");  
  const [lineNumbers, setLineNumbers] = useState(["1"]);  

  useEffect(() => {
    const lines = code.split("\n").length;
    setLineNumbers(Array.from({ length: lines }, (_, i) => (i + 1).toString()));
  }, [code]);

  useEffect(() => {
    if (selectedOption) {
      generateCode(selectedOption);  
    }
  }, [selectedOption]);

  const generateCode = (option: CodeOptions) => {
    const generatedCode = codeTemplates[option];
    setCode((prevCode) => prevCode + (prevCode ? "\n" : "") + generatedCode);  
  };

  const compile = async (action: string) => {
    setOutput("Procesando...");
    setIsError(false);

    try {
      const response = await fetch("http://localhost:5000/compile", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ code, action }),  
      });

      const data = await response.json();

      if (response.ok) {
        if (action === 'tokens') {
          setOutput(`Tokens: ${JSON.stringify(data.tokens, null, 2)}`);
        } else if (action === 'ast') {
          setOutput(`AST: ${data.ast}`);
        } else {
          setOutput("Compilación exitosa. Ahora puedes ejecutar el código.");
        }
        setIsError(false);
      } else {
        setOutput(`Error: ${data.error || "Error desconocido"}`);
        setIsError(true);
      }
    } catch (err: any) {
      setOutput(`Error: ${err.message || "No se pudo conectar con el servidor"}`);
      setIsError(true);
    }
  };

  const execute = async () => {
    setOutput("Ejecutando...");
    setIsError(false);

    try {
      const response = await fetch("http://localhost:5000/execute", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ code }),
      });

      const data = await response.json();

      if (response.ok) {
        const resultString = Object.entries(data.result || data.context)
          .map(([key, value]) => `"${key}": ${value}`)
          .join(", ");
        setOutput(resultString);
        setIsError(false);
      } else {
        setOutput(`Error en la ejecución: ${data.error || "Error desconocido"}`);
        setIsError(true);
      }
    } catch (err: any) {
      setOutput(`Error: ${err.message || "No se pudo conectar con el servidor"}`);
      setIsError(true);
    }
  };

  return (
    <div className="flex flex-col min-h-screen bg-color-gray-900 text-gray-100">
      <header className="bg-color-gray-800 p-4 flex flex-col sm:flex-row justify-between items-center w-full">
        <h1 className="text-xl font-bold text-white">Compilador BloodCode</h1>
        <div className="flex flex-col sm:flex-row items-center gap-4">
          <CodeOptionsComponent
            selectedOption={selectedOption}
            setSelectedOption={setSelectedOption}
          />
          <ActionButtons compile={compile} execute={execute} />
        </div>
      </header>

      <main className="flex-grow flex flex-col p-4 space-y-4 w-full">
        <div className="flex-grow h-[500px] max-h-[500px] bg-color-gray-800 rounded-lg shadow-md overflow-hidden w-full flex">
          <div className="flex-grow">
            <CodeEditor code={code} setCode={setCode} lineNumbers={lineNumbers} />
          </div>
        </div>
        <OutputDisplay output={output} isError={isError} />
      </main>
    </div>
  );
}
