import React, { useEffect } from "react";

export type CodeOptions = 'reservedWords' | 'controlSyntax' | 'functionSyntax' | 'operationSyntax' | 'semantics' | 'pemdas' | 'dataTypes' | 'vectorsSyntax' | 'dataEntry' | 'arraysSyntax' | 'whileSyntax' | 'forSyntax' | 'logicSyntax';

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

GreatOnes hello(): Rom {
Pray("Hello");
}

Hunter resultado: Maria;
resultado => suma(10, 10);
Pray(resultado);
`,
  operationSyntax: 
`Hunter a: Maria => 10;
Hunter b: Maria => 5;
Hunter c: Maria => 2;
Hunter d: Maria => 8;
Hunter resultado1, resultado2, resultado3: Maria;

resultado1 => a + (b * c);  
resultado2 => (a - b) / c; 
resultado3 => d * (a + b - c); 

Pray("Resultados de las operaciones:");

Pray("Resultado 1 (a + (b * c)):");
Pray(resultado1);

Pray("Resultado 2 ((a - b) / c):");
Pray(resultado2);

Pray("Resultado 3 (d * (a + b - c)):");
Pray(resultado3);
`,
  semantics: 
`
GreatOnes calcularArea(base: Maria, altura: Maria): Maria {
    Echoes (base * altura / 2);
}

GreatOnes saludar(nombre: Eileen): Rom {
    Pray("Hola, " + nombre + "! Bienvenido a BloodCode.");
}

Hunter nombreUsuario: Eileen;
Eyes(nombreUsuario);

Pray("Iniciando cálculos...");

Hunter base: Maria => 5;
Hunter altura: Maria => 10;
Hunter area: Maria;

area => calcularArea(base, altura);
Pray("El área calculada es:");
Pray(area);

saludar(nombreUsuario);

Insight (area > 20) {
    Pray("El área es mayor que 20.");
} Madness {
    Pray("El área es 20 o menor.");
}

Dream (base > 0) {
    Pray("Reduciendo la base en 1.");
    base => base - 1;
}
Pray("El valor final de base es:");
Pray(base);
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
  vectorsSyntax: 
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

Pray("Contenido del array numeros:");
Nightmare (Hunter i: Maria => 0; i < 5; i => i + 1;) {
    Pray(numeros[i]);
}

Hunter suma: Maria => numeros[0] + numeros[1] + numeros[2];
Pray("La suma de los tres primeros números es:");
Pray(suma);  
`,
  dataEntry: 
`Hunter nombre: Eileen;
Eyes(nombre);
Pray("El nombre del usuario es: " + nombre);
`,
  arraysSyntax: 
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
  whileSyntax: 
`Hunter b: Maria => 0;

Dream (b < 10) {
  Pray("Valor de b:");
  Pray(b);
  
  Insight (b == 5) {
    Pray("Se alcanzó el valor 5, terminando el ciclo.");
  }
  
  b => b + 1;
}
Pray("Ciclo terminado.");
`,
forSyntax:
`Hunter a,b: Maria => 0;

Nightmare (a => 0; a<10; a=>a+1;) {
  Pray("Valor de b:");
  Pray(b);
  
  Insight (b == 5) {
    Pray("Se alcanzó el valor 5, terminando el ciclo.");
  }
  
  b => b + 1;
}
Pray("Ciclo terminado.");

Pray("Nuevo ciclo:");
Nightmare(Hunter i: Maria => 0; i<5; i=>i+1;){
Pray(i);
Pray("Fin del ciclo.");
}
`,
logicSyntax:
`Hunter a: Blood => true;
Hunter b: Blood => false;

Pray(a Bloodbond a);
Pray(a Bloodbond b);
Pray(b Bloodbond a);
Pray(b Bloodbond b);

Pray(a OldBlood a);
Pray(a OldBlood b);
Pray(b OldBlood b);
Pray(b OldBlood a);

Pray(Vileblood a);
Pray(Vileblood b);
`,
pemdas:
`Hunter x: Maria => 8 + (15 / (3 + 2) - 4 * 2) * (6 + 8 / (3 - 1)) - 7 * (9 - 5 / (8 - 6));
Pray(x);
`
};

export const CodeGenerator: React.FC<CodeGeneratorProps> = ({ option, onGenerate }) => {
  useEffect(() => {
    const generatedCode = codeTemplates[option];
    onGenerate(generatedCode);
  }, [option, onGenerate]);

  return null;
};
