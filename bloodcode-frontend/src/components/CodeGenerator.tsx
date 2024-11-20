import React, { useEffect } from "react";

export type CodeOptions =
  | 'reservedWords'
  | 'controlSyntax'
  | 'functionSyntax'
  | 'operationSyntax'
  | 'semantics'
  | 'dataTypes'
  | 'vectorsSyntax'
  | 'dataEntry'
  | 'arraysSyntax'
  | 'whileSyntax'
  | 'forSyntax'
  | 'logicSyntax'
  | 'conditionalSyntax'
  | 'nestedLoops'
  | 'recursiveFunction'
  | 'switchCaseEmulation'
  | 'stringConcatenation'
  | 'complexArithmetic'
  | 'booleanExpressions'
  | 'arrayModification'
  | 'areaRectangle'
  | 'averageThreeNumbers'
  | 'celsiusToFahrenheit'
  | 'hoursToMinutesAndSeconds'
  | 'ageInDays'
  | 'menu'
  | 'productDotVectors'
  | 'vectorMinValue'
  | 'sumMatrixRows'
  | 'matrixAverage'
  | 'diagonalSum'
  | 'sumMatrixRow'
  | 'matrixMaxValue'
  | 'arrayMaxValue'
  | 'interchangeExtremes'
  | 'diagonalSecondary'
  | 'matrixMinMax'
  | 'diagonalComparison'
  | 'vectorAverage'
  | 'vectorMaxPosition'
  | 'sumMatrixRowsColumns'
  ;

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
    Pray("Hello, hunter");
}

Hunter resultado: Maria;
resultado => suma(10, 10);
hello();
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
    `GreatOnes calcularArea(base: Maria, altura: Maria): Maria {
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
  conditionalSyntax:
    `Hunter num1: Maria => 10;
Hunter num2: Maria => 5;

Insight (num1 > num2 Bloodbond num1 == 10) {
  Pray("num1 es mayor que num2 y es igual a 10.");
} Madness {
  Pray("La condición no se cumple.");
}
`,
  nestedLoops:
    `Hunter matriz: Maria[2].[2];
matriz[0].[0] => 1;
matriz[0].[1] => 2;
matriz[1].[0] => 3;
matriz[1].[1] => 4;

Hunter suma: Maria => 0;

Nightmare (Hunter i: Maria => 0; i < 2; i => i + 1;) {
  Nightmare (Hunter j: Maria => 0; j < 2; j => j + 1;) {
    suma => suma + matriz[i].[j];
  }
}

Pray("La suma de los elementos de la matriz es:");
Pray(suma);
`,
  recursiveFunction:
    `GreatOnes factorial(n: Maria): Maria {
  Insight (n == 1) {
    Echoes 1;
  } Madness {
    Echoes (n * factorial(n - 1));
  }
}

Hunter resultado: Maria;
resultado => factorial(5);
Pray("El factorial de 5 es:");
Pray(resultado);
`,
  switchCaseEmulation:
    `Hunter opcion: Maria => 2;

Insight (opcion == 1) {
  Pray("Opción 1 seleccionada.");
} Madness Insight (opcion == 2) {
  Pray("Opción 2 seleccionada.");
} Madness Insight (opcion == 3) {
  Pray("Opción 3 seleccionada.");
} Madness {
  Pray("Opción no válida.");
}
`,
  stringConcatenation:
    `Hunter nombre: Eileen => "Hunter";
Hunter titulo: Eileen => "el despiadado";

Hunter saludo: Eileen => "Hola, " + nombre + " " + titulo + "!";
Pray(saludo);
`,
  complexArithmetic:
    `Hunter resultado: Maria;
Hunter x: Maria => 10;
Hunter y: Maria => 20;
Hunter z: Maria => 5;
Hunter w: Maria => 8 + (15 / (3 + 2) - 4 * 2) * (6 + 8 / (3 - 1)) - 7 * (9 - 5 / (8 - 6));
Pray(w);

resultado => (x + y) * z - (y / x) + (z * z) - (x - y);
Pray("Resultado de la operación compleja:");
Pray(resultado);
`,
  booleanExpressions:
    `Hunter a: Blood => true;
Hunter b: Blood => false;
Hunter c: Blood => true;
Hunter d: Blood => false;

Hunter resultAnd1: Blood => a Bloodbond b;
Hunter resultAnd2: Blood => a Bloodbond c;
Hunter resultAnd3: Blood => b Bloodbond d;
Hunter resultAnd4: Blood => c Bloodbond d;

Hunter resultOr1: Blood => a OldBlood b;   
Hunter resultOr2: Blood => a OldBlood c;    
Hunter resultOr3: Blood => b OldBlood d;   
Hunter resultOr4: Blood => c OldBlood d;  

Hunter resultNot1: Blood => Vileblood a;   
Hunter resultNot2: Blood => Vileblood b;    
Hunter resultNot3: Blood => Vileblood c;    
Hunter resultNot4: Blood => Vileblood d;    

Pray("Resultado de a AND b:");
Pray(resultAnd1);
Pray("Resultado de a AND c:");
Pray(resultAnd2);
Pray("Resultado de b AND d:");
Pray(resultAnd3);
Pray("Resultado de c AND d:");
Pray(resultAnd4);

Pray("Resultado de a OR b:");
Pray(resultOr1);
Pray("Resultado de a OR c:");
Pray(resultOr2);
Pray("Resultado de b OR d:");
Pray(resultOr3);
Pray("Resultado de c OR d:");
Pray(resultOr4);

Pray("Resultado de NOT a:");
Pray(resultNot1);
Pray("Resultado de NOT b:");
Pray(resultNot2);
Pray("Resultado de NOT c:");
Pray(resultNot3);
Pray("Resultado de NOT d:");
Pray(resultNot4);
`,
  arrayModification:
    `Hunter numeros: Maria[3] => [1, 2, 3];

Pray("Array original:");
Pray(numeros[0]);
Pray(numeros[1]);
Pray(numeros[2]);

numeros[1] => 10;
numeros[2] => 30;
Pray("Array modificado:");
Pray(numeros[0]);
Pray(numeros[1]);
Pray(numeros[2]);
`,
areaRectangle:
`GreatOnes areaRectangulo(base: Maria, altura: Maria): Maria {
Echoes base * altura;
}

Hunter base: Maria => 5;
Hunter altura: Maria => 10;
Hunter area: Maria => areaRectangulo(base, altura);

Pray("El área del rectángulo es:");
Pray(area);
`,

averageThreeNumbers:
`GreatOnes promedio(a: Maria, b: Maria, c: Maria): Gehrman {
Echoes (a + b + c) / 3;
}

Hunter nota1: Maria => 85;
Hunter nota2: Maria => 90;
Hunter nota3: Maria => 88;
Hunter promedioFinal: Gehrman => promedio(nota1, nota2, nota3);

Pray("El promedio de las notas es:");
Pray(promedioFinal);
`,

celsiusToFahrenheit:
`GreatOnes celsiusAFahrenheit(celsius: Maria): Maria {
Echoes (celsius * 9 / 5) + 32;
}

Hunter temperaturaC: Maria => 25;
Hunter temperaturaF: Maria => celsiusAFahrenheit(temperaturaC);

Pray("La temperatura en Fahrenheit es:");
Pray(temperaturaF);
`,

hoursToMinutesAndSeconds:
`GreatOnes convertirAHorasMinutosSegundos(horas: Maria): Maria {
Hunter minutos: Maria => horas * 60;
Hunter segundos: Maria => horas * 3600;

Pray("Minutos:");
Pray(minutos);
Pray("Segundos:");
Pray(segundos);

Echoes minutos;  
}

Hunter horas: Maria => 2;
Hunter minutosResultado: Maria => convertirAHorasMinutosSegundos(horas);

Pray("Total en minutos:");
Pray(minutosResultado);
`,

ageInDays:
`GreatOnes edadEnDias(edad: Maria): Maria {
    Echoes edad * 365;
}

Hunter edad: Maria => 21;
Hunter diasVividos: Maria => edadEnDias(edad);

Pray("Días vividos aproximadamente:");
Pray(diasVividos);

`,
menu:
`Hunter opcion: Maria;

Pray("Ingresa una opción (1-7):");
Eyes(opcion);

Insight (opcion == 1) {
  Pray("Opción 1 seleccionada: Ver detalles del usuario.");
} Madness Insight (opcion == 2) {
  Pray("Opción 2 seleccionada: Configuración del sistema.");
} Madness Insight (opcion == 3) {
  Pray("Opción 3 seleccionada: Ejecutar operación especial.");
} Madness Insight (opcion == 4) {
  Pray("Opción 4 seleccionada: Guardar cambios.");
} Madness Insight (opcion == 5) {
  Pray("Opción 5 seleccionada: Cerrar sesión.");
} Madness Insight (opcion == 6) {
  Pray("Opción 6 seleccionada: Imprimir reporte.");
} Madness Insight (opcion == 7) {
  Pray("Opción 7 seleccionada: Salir del sistema.");
} Madness {
  Pray("Opción no válida: La opción seleccionada está fuera del rango permitido.");
}
`,
arrayMaxValue:
    `Hunter numeros: Maria[5] => [5, 3, 8, 1, 4];
Hunter mayor: Maria => numeros[0];

Nightmare (Hunter i: Maria => 1; i < 5; i => i + 1;) {
  Insight (numeros[i] > mayor) {
    mayor => numeros[i];
  }
}

Pray("El número mayor en el array es:");
Pray(mayor);
`,

  matrixMaxValue:
    `Hunter matriz: Maria[3].[3];
Hunter mayor: Maria => 0;

matriz[0].[0] => 5;
matriz[0].[1] => 12;
matriz[0].[2] => 7;
matriz[1].[0] => 3;
matriz[1].[1] => 15;
matriz[1].[2] => 1;
matriz[2].[0] => 8;
matriz[2].[1] => 4;
matriz[2].[2] => 10;

Nightmare (Hunter i: Maria => 0; i < 3; i => i + 1;) {
  Nightmare (Hunter j: Maria => 0; j < 3; j => j + 1;) {
    Insight (matriz[i].[j] > mayor) {
      mayor => matriz[i].[j];
    }
  }
}

Pray("El número mayor en la matriz es:");
Pray(mayor);
`,
  sumMatrixRow:
    `Hunter matriz: Maria[2].[3];

matriz[0].[0] => 5;
matriz[0].[1] => 10;
matriz[0].[2] => 15;
matriz[1].[0] => 20;
matriz[1].[1] => 25;
matriz[1].[2] => 30;

Hunter sumaFila: Maria => 0;

Nightmare (Hunter j: Maria => 0; j < 3; j => j + 1;) {
  sumaFila => sumaFila + matriz[0].[j];
}

Pray("La suma de los elementos de la primera fila es:");
Pray(sumaFila);
`,

  diagonalSum:
    `Hunter matriz: Maria[3].[3];
matriz[0].[0] => 3;
matriz[0].[1] => 5;
matriz[0].[2] => 7;
matriz[1].[0] => 2;
matriz[1].[1] => 4;
matriz[1].[2] => 6;
matriz[2].[0] => 1;
matriz[2].[1] => 8;
matriz[2].[2] => 9;

Hunter sumaDiagonal: Maria => 0;

Nightmare (Hunter i: Maria => 0; i < 3; i => i + 1;) {
  sumaDiagonal => sumaDiagonal + matriz[i].[i];
}

Pray("La suma de la diagonal principal es:");
Pray(sumaDiagonal);
`,

  matrixAverage:
    `Hunter matriz: Maria[2].[3];
Hunter suma: Maria => 0;
Hunter elementos: Maria => 0;

matriz[0].[0] => 10;
matriz[0].[1] => 20;
matriz[0].[2] => 30;
matriz[1].[0] => 40;
matriz[1].[1] => 50;
matriz[1].[2] => 60;

Nightmare (Hunter i: Maria => 0; i < 2; i => i + 1;) {
  Nightmare (Hunter j: Maria => 0; j < 3; j => j + 1;) {
    suma => suma + matriz[i].[j];
    elementos => elementos + 1;
  }
}

Hunter promedio: Maria => suma / elementos;

Pray("El promedio de los elementos de la matriz es:");
Pray(promedio);
`,

  sumMatrixRows:
    `Hunter matriz: Maria[3].[3];
matriz[0].[0] => 1;
matriz[0].[1] => 2;
matriz[0].[2] => 3;
matriz[1].[0] => 4;
matriz[1].[1] => 5;
matriz[1].[2] => 6;
matriz[2].[0] => 7;
matriz[2].[1] => 8;
matriz[2].[2] => 9;

Nightmare (Hunter i: Maria => 0; i < 3; i => i + 1;) {
  Hunter sumaFila: Maria => 0;
  Nightmare (Hunter j: Maria => 0; j < 3; j => j + 1;) {
    sumaFila => sumaFila + matriz[i].[j];
  }
  Pray("Suma de la fila: ");
  Pray(sumaFila);
}
`,

  vectorMinValue:
    `Hunter vector: Maria[5];
vector[0] => 12;
vector[1] => 7;
vector[2] => 25;
vector[3] => 3;
vector[4] => 18;

Hunter menor: Maria => vector[0];

Nightmare (Hunter i: Maria => 1; i < 5; i => i + 1;) {
  Insight (vector[i] < menor) {
    menor => vector[i];
  }
}

Pray("El menor elemento del vector es:");
Pray(menor);
`,

  productDotVectors:
    `Hunter vectorA: Maria[3];
Hunter vectorB: Maria[3];

vectorA[0] => 2;
vectorA[1] => 4;
vectorA[2] => 6;

vectorB[0] => 1;
vectorB[1] => 3;
vectorB[2] => 5;

Hunter productoPunto: Maria => 0;

Nightmare (Hunter i: Maria => 0; i < 3; i => i + 1;) {
  productoPunto => productoPunto + (vectorA[i] * vectorB[i]);
}

Pray("El producto punto entre los dos vectores es:");
Pray(productoPunto);
`,
interchangeExtremes:
`Hunter vector: Maria[5];
vector[0] => 10;
vector[1] => 20;
vector[2] => 30;
vector[3] => 40;
vector[4] => 50;

Hunter temp: Maria => vector[0];
vector[0] => vector[4];
vector[4] => temp;

Pray("Vector después de intercambiar los extremos:");
Nightmare (Hunter i: Maria => 0; i < 5; i => i + 1;) {
  Pray(vector[i]);
}
`,
diagonalSecondary:
`Hunter matriz: Maria[3].[3];
matriz[0].[0] => 1;
matriz[0].[1] => 2;
matriz[0].[2] => 3;
matriz[1].[0] => 4;
matriz[1].[1] => 5;
matriz[1].[2] => 6;
matriz[2].[0] => 7;
matriz[2].[1] => 8;
matriz[2].[2] => 9;

Pray("Elementos de la diagonal secundaria:");
Nightmare (Hunter i: Maria => 0; i < 3; i => i + 1;) {
  Pray(matriz[i].[2 - i]);
}
`,
matrixMinMax:
`Hunter matriz: Maria[3].[3];
matriz[0].[0] => 12;
matriz[0].[1] => 7;
matriz[0].[2] => 15;
matriz[1].[0] => 9;
matriz[1].[1] => 20;
matriz[1].[2] => 5;
matriz[2].[0] => 3;
matriz[2].[1] => 14;
matriz[2].[2] => 8;

Hunter minimo: Maria => matriz[0].[0];
Hunter maximo: Maria => matriz[0].[0];

Nightmare (Hunter i: Maria => 0; i < 3; i => i + 1;) {
  Nightmare (Hunter j: Maria => 0; j < 3; j => j + 1;) {
    Insight (matriz[i].[j] < minimo) {
      minimo => matriz[i].[j];
    }
    Insight (matriz[i].[j] > maximo) {
      maximo => matriz[i].[j];
    }
  }
}

Pray("El elemento mínimo de la matriz es:");
Pray(minimo);
Pray("El elemento máximo de la matriz es:");
Pray(maximo);
`,
diagonalComparison:
`Hunter matriz: Maria[3].[3];
matriz[0].[0] => 5;
matriz[0].[1] => 2;
matriz[0].[2] => 3;
matriz[1].[0] => 1;
matriz[1].[1] => 6;
matriz[1].[2] => 4;
matriz[2].[0] => 7;
matriz[2].[1] => 8;
matriz[2].[2] => 9;

Hunter sumaPrincipal: Maria => 0;
Hunter sumaSecundaria: Maria => 0;

Nightmare (Hunter i: Maria => 0; i < 3; i => i + 1;) {
  sumaPrincipal => sumaPrincipal + matriz[i].[i];
  sumaSecundaria => sumaSecundaria + matriz[i].[2 - i];
}

Pray("Suma de la diagonal principal:");
Pray(sumaPrincipal);
Pray("Suma de la diagonal secundaria:");
Pray(sumaSecundaria);

Insight (sumaPrincipal > sumaSecundaria) {
  Pray("La diagonal principal es mayor.");
} Madness Insight (sumaSecundaria > sumaPrincipal) {
  Pray("La diagonal secundaria es mayor.");
} Madness {
  Pray("Ambas diagonales son iguales.");
}
`,
vectorAverage:
`Hunter vector: Maria[5];
vector[0] => 10;
vector[1] => 20;
vector[2] => 30;
vector[3] => 40;
vector[4] => 50;

Hunter suma: Maria => 0;

Nightmare (Hunter i: Maria => 0; i < 5; i => i + 1;) {
  suma => suma + vector[i];
}

Hunter promedio: Maria => suma / 5;

Pray("El promedio de los elementos del vector es:");
Pray(promedio);
`,
vectorMaxPosition:
`Hunter vector: Maria[5];
vector[0] => 12;
vector[1] => 7;
vector[2] => 25;
vector[3] => 3;
vector[4] => 18;

Hunter mayor: Maria => vector[0];
Hunter posicionMayor: Maria => 0;

Nightmare (Hunter i: Maria => 1; i < 5; i => i + 1;) {
  Insight (vector[i] > mayor) {
    mayor => vector[i];
    posicionMayor => i;
  }
}

Pray("El mayor elemento está en la posición:");
Pray(posicionMayor);
`,
sumMatrixRowsColumns:
`Hunter matriz: Maria[3].[3];
matriz[0].[0] => 3;
matriz[0].[1] => 5;
matriz[0].[2] => 7;
matriz[1].[0] => 2;
matriz[1].[1] => 4;
matriz[1].[2] => 6;
matriz[2].[0] => 1;
matriz[2].[1] => 8;
matriz[2].[2] => 9;

Nightmare (Hunter i: Maria => 0; i < 3; i => i + 1;) {
  Hunter sumaFila: Maria => 0;
  Hunter sumaColumna: Maria => 0;

  Nightmare (Hunter j: Maria => 0; j < 3; j => j + 1;) {
    sumaFila => sumaFila + matriz[i].[j];
    sumaColumna => sumaColumna + matriz[j].[i];
  }

  Pray("Suma de la fila: ");
  Pray(sumaFila);
  Pray("Suma de la columna: ");
  Pray(sumaColumna);
}
`,
};

export const CodeGenerator: React.FC<CodeGeneratorProps> = ({ option, onGenerate }) => {
  useEffect(() => {
    const generatedCode = codeTemplates[option];
    onGenerate(generatedCode);
  }, [option, onGenerate]);

  return null;
};
