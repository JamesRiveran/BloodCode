interface OutputDisplayProps {
    output: string;
    isError: boolean;
  }
  
  export const OutputDisplay: React.FC<OutputDisplayProps> = ({ output, isError }) => {
    return (
      <div className="flex flex-col bg-color-gray-800 rounded-lg shadow-md p-6 w-full h-auto max-h-[70vh] space-y-4">
        <div className="flex-grow bg-color-gray-700 rounded-lg shadow-md p-4 overflow-hidden h-[29vh] flex flex-col ">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold text-gray-400">Salida</h2>
          </div>
          <pre
            className={`flex-grow w-full overflow-y-auto bg-color-gray-800 p-5 rounded border border-gray-600 ${
                isError ? "text-danger" : "text-color-gray-600"
            }`}
            >
            {output || "La salida del programa se mostrará aquí"}
        </pre>

        </div>
      </div>
    );
  };
  