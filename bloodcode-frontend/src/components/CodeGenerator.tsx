import React, { useEffect } from "react";
import { Select, SelectTrigger, SelectContent, SelectItem, SelectValue } from "@/components/ui/select";

export type CodeOptions = 'reservedWords' | 'controlSyntax' | 'functionSyntax' | 'operationSyntax' | 'semantics' | 'dataTypes' | 'vectors' | 'dataEntry' | 'arrays';

interface CodeGeneratorProps {
  option: CodeOptions;
  onGenerate: (code: string) => void;
}

export const codeTemplates: Record<CodeOptions, string> = {
  reservedWords: 
`Hunter numero: Maria => 10;
Hunter texto: Eileen => "Hola mundo";
Hunter esVerdadero: Blood => true;

Insight (esVerdadero) {
  Pray("La condición es verdadera.");
} Madness {
  Pray("La condición es falsa.");
}
`,
  controlSyntax: 
`Hunter x: Maria => 20;
Hunter y: Maria => 10;

Insight (x > y) {
  Pray("x es mayor que y.");
} Madness {
  Pray("x no es mayor que y.");
}`,
  functionSyntax: 
`GreatOnes suma(a: Maria, b: Maria): Maria {
  Echoes (a + b);
}
Hunter resultado: Maria;
resultado => suma(10, 10);
Pray(resultado);
`,
  operationSyntax: 
`Hunter a: Maria => 10;
Hunter b: Maria => 5;
Hunter c: Maria => 2;
Hunter resultado: Maria;

resultado => a + (b * c);
Pray("El resultado es:");
Pray(resultado);
`,
  semantics: 
`Hunter x: Maria => 5;
Hunter resultado: Maria => x + 3;

Pray("El resultado de x + 3 es:");
Pray(resultado); 
`,
  dataTypes: 
`Hunter entero: Maria => 42;
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
`,
  vectors: 
`Hunter abc: Maria[5];
abc[0] => 10;
abc[1] => 20;
abc[2] => 30;
abc[3] => 40;
abc[4] => 50;

Pray(abc[1]); 
Pray(abc[2] + abc[3]);  
abc[4] => abc[0] + abc[4]; 

Pray(abc[4]); 

Hunter numeros: Maria[5] => [1, 2, 3, 4, 5];

Pray(numeros[0]);  
Pray(numeros[1]);
Pray(numeros[2]);  
Pray(numeros[3]); 
Pray(numeros[4]); 

Hunter suma: Maria => numeros[0] + numeros[1] + numeros[2];
Pray("La suma de los tres primeros números es:");
Pray(suma);  
`,
  dataEntry: 
`Hunter nombre: Eileen;
Eyes(nombre);
Pray("El nombre del usuario es: ");
Pray(nombre);
`,
  arrays: 
`Hunter matriz: Maria[3].[3];
matriz[0].[0] => 10;
matriz[0].[1] => 20;
matriz[0].[2] => 30;
matriz[1].[0] => 40;
matriz[1].[1] => 50;
matriz[1].[2] => 60;
matriz[2].[0] => 70;
matriz[2].[1] => 80;
matriz[2].[2] => 90;

Pray("Acceso a elementos individuales de la matriz:");
Pray(matriz[0].[0]);
Pray(matriz[1].[1]);
Pray(matriz[2].[2]);

Hunter suma_fila: Maria => matriz[0].[0] + matriz[0].[1] + matriz[0].[2];
Pray("La suma de la primera fila es:");
Pray(suma_fila);

Hunter total_suma: Maria => matriz[0].[0] + matriz[1].[1];
Pray("Suma de elementos específicos:");
Pray(total_suma);
`,
};

export const CodeGenerator: React.FC<CodeGeneratorProps> = ({ option, onGenerate }) => {
  useEffect(() => {
    const generatedCode = codeTemplates[option];
    onGenerate(generatedCode);
  }, [option, onGenerate]);

  return null;
};
