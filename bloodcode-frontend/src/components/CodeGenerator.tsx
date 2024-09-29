import React, { useEffect } from "react";

export type CodeOptions = 'reservedWords' | 'controlSyntax' | 'functionSyntax' | 'operationSyntax' | 'semantics' | 'dataTypes';

interface CodeGeneratorProps {
  option: CodeOptions;
  onGenerate: (code: string) => void;
}

export const codeTemplates: Record<CodeOptions, string> = {
  reservedWords: `HuntersDream {
  Hunter numero: Maria => 10;
  Hunter texto: Eileen => "Hola mundo";
  Hunter esVerdadero: Blood => true;

  Insight (esVerdadero) {
    Pray("La condición es verdadera.");
  } Madness {
    Pray("La condición es falsa.");
  }
}`,
  controlSyntax: `HuntersDream {
  Hunter x: Maria => 20;
  Hunter y: Maria => 10;

  Insight (x > y) {
    Pray("x es mayor que y.");
  } Madness {
    Pray("x no es mayor que y.");
  }
}`,
  functionSyntax: `HuntersDream {
    GreatOnes suma(a: Maria, b: Maria): Maria {
        Echoes (a + b);
    }
    Hunter resultado: Maria;
    resultado => suma(10, 10);
    Pray(resultado);
}`,
  operationSyntax: `HuntersDream {
  Hunter a: Maria => 10;
  Hunter b: Maria => 5;
  Hunter c: Maria => 2;
  Hunter resultado: Maria;

  resultado => a + (b * c);
  Pray("El resultado es:");
  Pray(resultado);
}`,
  semantics: `HuntersDream {
  Hunter x: Maria => 5;
  Hunter resultado: Maria => x + 3;

  Pray("El resultado de x + 3 es:");
  Pray(resultado); 
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
  Insight (booleano) {
    Pray("El valor booleano es verdadero.");
  }
}`,
};

export const CodeGenerator: React.FC<CodeGeneratorProps> = ({ option, onGenerate }) => {
  useEffect(() => {
    const generatedCode = codeTemplates[option];
    onGenerate(generatedCode);
  }, [option, onGenerate]);

  return null;
};
