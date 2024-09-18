interface OutputDisplayProps {
    output: string;
    isError: boolean;
  }
  
  export const OutputDisplay: React.FC<OutputDisplayProps> = ({ output, isError }) => {
    return (
      <div className="h-[350px] max-h-[320px] bg-gray-800 rounded-lg shadow-md p-4 overflow-hidden">
        <h2 className="text-lg font-semibold mb-2">Salida</h2>
        <pre
          className={`whitespace-pre-wrap h-[calc(100%-2rem)] overflow-y-auto bg-gray-700 p-2 rounded ${
            isError ? "text-red-500" : "text-gray-100"
          }`}
        >
          {output || "La salida del programa se mostrará aquí"}
        </pre>
      </div>
    );
  };
  