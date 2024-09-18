import React, { useEffect } from "react";

export type CodeOptions = 'reservedWords' | 'controlSyntax' | 'functionSyntax' | 'operationSyntax' | 'semantics' | 'dataTypes';

interface CodeGeneratorProps {
  option: CodeOptions;
  onGenerate: (code: string) => void;
}

export const codeTemplates: Record<CodeOptions, string> = {
  reservedWords: `HuntersDream {
  Hunter a: Maria;
  Hunter isTrue: Blood => true;
  
  Insight (isTrue) {
    Pray("La condición es verdadera.");
  } Madness {
    Pray("La condición es falsa.");
  }
}`,
  controlSyntax: `HuntersDream {
  Hunter a: Maria => 10;
  Hunter b: Maria => 5;

  Insight (a > b) {
    Pray("a es mayor que b");
  } Madness {
    Pray("a no es mayor que b");
  }
}`,
  functionSyntax: `HuntersDream {
  GreatOnes suma(Hunter x: Maria, Hunter y: Maria): Maria {
    Echoes(x + y);
  }

  Hunter resultado: Maria => suma(10, 5);
  Pray("Resultado de la suma: ");
  Pray(resultado);
}`,
  operationSyntax: `HuntersDream {
  Hunter a: Maria => 10;
  Hunter b: Maria => 5;
  Hunter resultado: Maria;

  resultado => a + b * 2;
  Pray("Resultado: ");
  Pray(resultado);
}`,
  semantics: `HuntersDream {
  Hunter x: Maria => 5;
  Pray("x + 3: ");
  Pray(x + 3); 
}`,
  dataTypes: `HuntersDream {
  Hunter entero: Maria => 42;
  Hunter flotante: Gehrman => 3.14;
  Hunter cadena: Eileen => "Hola";
  Hunter booleano: Blood => true;

  Pray("Entero: ");
  Pray(entero);
  
  Pray("Flotante: ");
  Pray(flotante);
  
  Pray("Cadena: ");
  Pray(cadena);
  
  Pray("Booleano: ");
  Pray(booleano);
}`,
};

export const CodeGenerator: React.FC<CodeGeneratorProps> = ({ option, onGenerate }) => {
  useEffect(() => {
    const generatedCode = codeTemplates[option];
    onGenerate(generatedCode);
  }, [option, onGenerate]);

  return null;
};
